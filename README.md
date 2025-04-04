# Carreg_Acucar_app_v1.0

**Guia de Instalação e Uso – Carregamentos de Açúcar – SAP**

Autor: Rander Felipe Miranda de Paula

## 📦 Pré-requisitos

- Python (versão utilizada no projeto: **3.13.1**)
- Internet para download de dependências
- Ambiente Windows com suporte a scripts `.bat`

## 🚀 Instalação

1. **Instalar o Python**  
   O instalador está disponível no diretório do projeto ou você pode baixar em:  
   👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

   > **Importante:** Marque a opção para adicionar Python ao PATH durante a instalação.

2. **Verificar a instalação do Python**  
   Execute o comando:
   ```bash
   python --version
   ```

3. **Instalar dependências do projeto**  
   No terminal (CMD ou PowerShell), navegue até o diretório do projeto e execute:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Execução

4. **Iniciar a aplicação**  
   Execute o arquivo:
   ```
   start.bat
   ```
   > **Atenção:** Não feche a janela do terminal enquanto a aplicação estiver em execução.

5. **Primeira execução**  
   Ao iniciar o programa pela primeira vez, será solicitado um e-mail para logs de erro.  
   - Não é necessário que seja um e-mail autêntico/verificável.

## ⚙️ Uso da Aplicação

### 1. Definir filtros de consulta:
- **Data Inicial** e **Data Final**  
- **Local de Saída**: `Armazém` ou `Usina`

### 2. Executar consulta
Clique no botão **"Consultar SAP"** para obter os dados, que serão exibidos em forma de tabela.

### 3. Funcionalidades da tabela
- **Download (CSV)**: Exportar tabela simplificada
- **Search**: Busca por texto nos registros
- **FullScreen**: Expansão para tela cheia

### 4. Exportação para Excel
Na seção **"Exportar"**, é possível baixar os dados no formato `.xlsx`.

## ❌ Campos de Desenvolvedor
No canto superior direito, os botões **Deploy** e **Configurações (três pontos)** são de uso exclusivo da equipe de desenvolvimento e podem ser ignorados.
