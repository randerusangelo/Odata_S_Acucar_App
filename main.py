import streamlit as st
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import altair as alt
import re
from datetime import datetime, date
import io

ODATA_URL = "https://vhuegperci.sap.usangelo.com:44300/sap/opu/odata/sap/ZODATA_SD_SAIDA_ACUCAR_SRV/SaidaAcucarSet?$format=json"

SAP_USER = st.secrets["SAP_USER"]
SAP_PASS = st.secrets["SAP_PASS"]

def formatar_data_sap(date_str):
    match = re.search(r'/Date\((\d+)\)/', date_str)
    if match:
        timestamp = int(match.group(1)) // 1000
        return datetime.utcfromtimestamp(timestamp,).strftime("%d/%m/%Y")
    return date_str

def formatar_hora(hora_sap):
    match = re.search(r'PT(\d{1,2})H(\d{1,2})M', hora_sap)
    if match:
        return f"{match.group(1).zfill(2)}:{match.group(2).zfill(2)}"
    return hora_sap

st.set_page_config(page_title="Saída de Açúcar", layout="wide")
st.title("📦 CARREGAMENTOS DE AÇÚCAR - SAP - v 1.0.1 ")

if "data_ini" not in st.session_state:
    st.session_state["data_ini"] = date.today().replace(day=1)
if "data_fim" not in st.session_state:
    st.session_state["data_fim"] = date.today()

with st.sidebar:
    st.header("🔍 Filtros")
    data_ini = st.date_input("Data Inicial", value=st.session_state["data_ini"])
    st.caption(f"Selecionado: {data_ini.strftime('%d/%m/%Y')}")
    data_fim = st.date_input("Data FInal" , value=st.session_state["data_fim"])
    st.caption(f"Selecionado: {data_fim.strftime('%d/%m/%Y')}")

    tipo_local = st.selectbox("Local de Saída", options=["USINA","ARMAZEM"])
    st.caption(f"Selecionado: {tipo_local}")

    if st.button("Salvar Filtros"):
        st.session_state["data_ini"] = data_ini
        st.session_state["data_fim"] = data_fim
        st.session_state["tipo_local"] = tipo_local
        st.success("Filtros salvos na sessão.")
st.subheader("📊 Resultado da Consulta")
if st.button("Consultar SAP"):
    with st.spinner("Consultando SAP..."):
        try:
            headers = {
                "Accept": "application/json",
                "data_ini": data_ini.strftime("%Y%m%d"),
                "data_fim": data_fim.strftime("%Y%m%d"),
                "esto_armaz": tipo_local,
                "x-csrf-token": "fetch"
            }
            response = requests.get(
                ODATA_URL,
                auth=HTTPBasicAuth(SAP_USER, SAP_PASS),
                headers=headers,
                verify=False
            )
            if response.status_code == 200:
                json_data = response.json()
                dados = json_data.get("d", {}).get("results", [])
                if not dados:
                    st.warning("Nenhum registro retornado pelo SAP.")
                    st.stop()  
                if dados:
                    df = pd.DataFrame(dados)
                    df.columns = [col.upper() for col in df.columns] 
                    df = df.drop(columns=[col for col in df.columns if "__metadata" in col or col.startswith("__")], errors="ignore")
                    if "DATA" in df.columns:
                        df["DATA"] = df["DATA"].apply(formatar_data_sap)
                    if "HORA" in df.columns:
                        df["HORA"] = df["HORA"].apply(formatar_hora)
                    if "QUANTIDADE" in df.columns:
                        df.rename(columns={"QUANTIDADE": "QUANTIDADE (KG)"}, inplace=True)
                    st.success(f"{len(df)} registros encontrados.")
                    st.dataframe(df)
                    if "QUANTIDADE (KG)" in df.columns:
                        try:
                            total = pd.to_numeric(df["QUANTIDADE (KG)"], errors="coerce").sum()
                            st.info(f"📦 **Carga total no intervalo:** {int(total):,} kg")
                        except Exception as e:
                            st.warning("Erro ao calcular o total de quantidade.")
                with st.expander("📥 Exportar"):
                    try:
                        df_export = df.copy()
                        if "QUANTIDADE (KG)" in df_export.columns:
                            df_export["QUANTIDADE (KG)"] = pd.to_numeric(df_export["QUANTIDADE (KG)"], errors="coerce")
                            total = df_export["QUANTIDADE (KG)"].sum()
                            total_row = {col: "" for col in df_export.columns}
                            primeira_coluna = df_export.columns[0]
                            total_row[primeira_coluna] = "TOTAL"
                            total_row["QUANTIDADE (KG)"] = total
                            df_export.loc[len(df_export)] = total_row
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine="openpyxl") as writer:
                            df_export.to_excel(writer, index=False, sheet_name="SaidaAcucar")
                        output.seek(0)
                        st.download_button(
                            label="📤 Baixar Excel (.xlsx)",
                            data=output.getvalue(),
                            file_name="saida_acucar.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    except Exception as e:
                        st.error("Erro ao gerar o arquivo Excel.")
                        st.exception(e)                                           
            else:
                st.error(f"Erro {response.status_code} ao consultar SAP")
                st.text(response.text)
        except Exception as e:
            st.error("Erro ao conectar no serviço.")
            st.exception(e)
