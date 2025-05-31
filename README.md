Aluno: Demetrios Alejandro Tavares Barbosa - SPI P1 - noite
Aluno: Keitel Werner Cavalcanti Costa Hartel Filho - SPI P1 - noite
Aluno: Gabriel Mendes Palha - SPI P1 - noite

# Projeto Flask - Tutor Interativo de Python com IA Gemini e Dicionário de Termos

Este projeto é uma aplicação web desenvolvida com Flask que serve como uma plataforma educacional para aprender Python. Ele inclui seções sobre fundamentos de Python, um dicionário de termos de programação interativo e um tutor de IA integrado com a API Gemini do Google para responder a perguntas sobre Python.

## 1. Documentação

### a. Estrutura do Site e Conteúdo de Cada Seção

O site é organizado nas seguintes seções principais:

*   **Página Inicial (`/`)**
    *   **Conteúdo:** Página de boas-vindas ou introdução ao site.
    *   **Template:** `index.html`

*   **Equipe (`/equipe`)**
    *   **Conteúdo:** Apresenta informações sobre os membros da equipe do projeto. Os dados são configurados diretamente no arquivo `app.py` e podem ser expandidos.
    *   **Template:** `equipe.html`

*   **Fundamentos de Python (`/python-fundamentos`)**
    *   **Conteúdo:** Explica conceitos fundamentais de Python, como estruturas de seleção (`if/elif/else`), estruturas de repetição (`for`, `while`), vetores/matrizes (usando listas), funções/procedimentos e tratamento de exceções. Cada conceito é acompanhado de uma descrição, aplicação e um exemplo de código Python.
    *   **Template:** `python_fundamentos.html`

*   **Tutor IA Gemini (`/ia_gemini`)**
    *   **Conteúdo:** Uma interface interativa onde o usuário pode fazer perguntas sobre programação Python. As perguntas são enviadas para a API do Google Gemini, que atua como um tutor, e a resposta gerada pela IA é exibida na página.
    *   **Template:** `ia_gemini.html`

*   **Dicionário de Termos (`/dicionario`)**
    *   **Conteúdo:** Exibe uma lista de termos de programação e suas definições. Os dados são armazenados em um arquivo de texto (`data/dicionario.txt`).
    *   **Templates:** `dicionario.html` (para listagem e adição), `editar_termo.html` (para edição).
    *   **Funcionalidades:**
        *   Visualizar todos os termos e suas definições.
        *   Adicionar um novo termo e sua definição através de um formulário (`/dicionario/adicionar` - método POST).
        *   Editar um termo ou definição existente (`/dicionario/editar/<termo_original>` - métodos GET para exibir o formulário e POST para salvar as alterações).
        *   Deletar um termo existente (`/dicionario/deletar/<termo>` - método POST).

### b. Tecnologias Utilizadas

*   **Linguagem de Programação:** Python 3.x
*   **Framework Web:** Flask (utilizado para criar a estrutura da aplicação web, gerenciar rotas e renderizar templates)
*   **API de Inteligência Artificial:** Google Gemini (especificamente o modelo `gemini-1.5-flash-latest` via biblioteca `google-generativeai` para a funcionalidade de tutoria)
*   **Gerenciamento de Variáveis de Ambiente:** `python-dotenv` (para carregar configurações sensíveis, como a chave da API, de um arquivo `.env`)
*   **Motor de Template:** Jinja2 (integrado ao Flask, usado para gerar dinamicamente as páginas HTML)
*   **Frontend:** HTML (para a estrutura das páginas), CSS (para estilização, não detalhado no `app.py` mas implícito para templates)
*   **Armazenamento de Dados (Dicionário):** Arquivo de texto (`data/dicionario.txt`) para persistência simples dos termos do dicionário.
*   **Bibliotecas Python Adicionais:**
    *   `os`: Para interações com o sistema operacional (manipulação de caminhos de arquivo, variáveis de ambiente).
    *   `datetime`: Para obter o ano atual (usado no rodapé das páginas).

### c. Implementação da Integração com a API do Gemini

A integração com a API do Google Gemini é um componente chave da seção "Tutor IA Gemini" e é implementada da seguinte forma:

1.  **Configuração da Chave da API:**
    *   A chave da API do Gemini é lida da variável de ambiente `GEMINI_API_KEY`.
    *   Esta chave deve ser definida em um arquivo `.env` na raiz do projeto. O `app.py` utiliza `load_dotenv()` para carregar esta variável.

2.  **Inicialização do Modelo:**
    *   No início da execução do `app.py`, o código tenta configurar a biblioteca `google.generativeai` com a chave da API: `genai.configure(api_key=GEMINI_API_KEY)`.
    *   Se a configuração for bem-sucedida, um modelo generativo é instanciado: `model = genai.GenerativeModel('models/gemini-1.5-flash-latest')`.
    *   O sistema imprime mensagens no console indicando o sucesso ou falha da configuração. Se a chave não for encontrada ou ocorrer um erro, a variável `model` permanece `None`, e a funcionalidade de tutoria é desabilitada com um aviso.

3.  **Interação na Rota `/ia_gemini`:**
    *   Esta rota é acessível via métodos `GET` (para exibir a página com o formulário de pergunta) e `POST` (quando o usuário envia uma pergunta).
    *   Ao receber uma requisição `POST`:
        *   A aplicação verifica se o `model` Gemini foi inicializado. Se não, uma mensagem de erro (`flash`) é exibida ao usuário.
        *   A pergunta do usuário é obtida do formulário (`request.form.get("pergunta")`).
        *   Um prompt é construído para guiar a IA: `f"Você é um tutor de programação Python para iniciantes. Responda a seguinte pergunta de forma clara, didática e com exemplos simples, se aplicável: {pergunta_usuario}"`. Este prompt instrui o modelo a se comportar como um tutor e a fornecer respostas adequadas para iniciantes.
        *   A pergunta (com o prompt) é enviada para a API Gemini usando `response = model.generate_content(prompt_completo)`.
        *   A resposta textual da IA (`response.text`) é extraída e passada para o template para ser exibida ao usuário.
        *   Um bloco `try-except` envolve a chamada à API para capturar e exibir possíveis erros de comunicação ou da própria API.

### d. Como Executar a Aplicação Flask Localmente

Siga os passos abaixo para executar a aplicação em seu ambiente local:

1.  **Clone o Repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO_GIT>
    cd <NOME_DA_PASTA_DO_PROJETO>
    ```

2.  **Crie e Ative um Ambiente Virtual (Recomendado):**
    Isso isola as dependências do projeto.
    ```bash
    # Para Python 3
    python -m venv venv
    ```
    Ative o ambiente:
    ```bash
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as Dependências:**
    Crie um arquivo chamado `requirements.txt` na raiz do projeto com o seguinte conteúdo:
    ```txt
    Flask
    google-generativeai
    python-dotenv
    ```
    Em seguida, instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto. Adicione sua chave da API do Gemini a este arquivo:
    ```env
    GEMINI_API_KEY="SUA_CHAVE_API_GEMINI_AQUI"
    ```
    Substitua `"SUA_CHAVE_API_GEMINI_AQUI"` pela sua chave real.

5.  **Execute a Aplicação:**
    Com o ambiente virtual ativado e as dependências instaladas, execute o script principal:
    ```bash
    python app.py
    ```

6.  **Acesse no Navegador:**
    Abra seu navegador e acesse `http://127.0.0.1:5000/`. A aplicação estará rodando em modo de depuração (`debug=True`), o que é útil para desenvolvimento.

### e. Breve Descrição das Principais Partes do Código Python (`app.py`)

*   **Importações e Configuração Inicial:**
    *   Importa módulos essenciais como `os`, `datetime`, `google.generativeai` (`genai`), `dotenv` (`load_dotenv`), e componentes do `Flask` (`Flask`, `render_template`, `request`, `redirect`, `url_for`, `flash`).
    *   `load_dotenv()`: Carrega variáveis de ambiente do arquivo `.env`.
    *   `app = Flask(__name__)`: Cria a instância da aplicação Flask.
    *   `app.secret_key = os.urandom(24)`: Define uma chave secreta para a aplicação, necessária para usar `flash messages` e sessões.

*   **Configuração da API do Gemini:**
    *   Obtém a `GEMINI_API_KEY` das variáveis de ambiente.
    *   Tenta configurar `genai` com a chave e inicializar `genai.GenerativeModel`.
    *   Inclui tratamento de erro (`try-except`) e mensagens de log para o status da configuração da API. Se falhar, `model` fica como `None`.

*   **Gerenciamento do Dicionário de Termos:**
    *   `DATA_DIR` e `DICIONARIO_FILE`: Constantes que definem o caminho para o diretório de dados e o arquivo do dicionário (`data/dicionario.txt`).
    *   `_ensure_data_dir_exists()`: Função utilitária que verifica a existência do diretório `data/` e do arquivo `dicionario.txt`. Se não existirem, são criados, e o arquivo do dicionário é populado com alguns termos de exemplo.
    *   `carregar_dicionario()`: Lê o arquivo `dicionario.txt`, onde cada linha tem o formato `Termo:Definição`. Converte essas linhas em um dicionário Python (`{termo: definicao}`). Trata linhas mal formatadas.
    *   `salvar_dicionario(termos)`: Recebe um dicionário de termos e o salva de volta no arquivo `dicionario.txt`, com cada entrada em uma nova linha e os termos ordenados alfabeticamente.

*   **Processador de Contexto (`@app.context_processor`)**:
    *   `inject_current_year()`: Uma função que disponibiliza automaticamente a variável `current_year` (contendo o ano atual) para todos os templates Jinja2. Útil para exibir o ano no rodapé, por exemplo.

*   **Definição de Rotas (`@app.route`)**:
    *   **`/` (`index`)**: Rota principal, renderiza `index.html`.
    *   **`/equipe` (`equipe`)**: Renderiza `equipe.html`, passando uma lista de dicionários com informações dos membros da equipe.
    *   **`/python-fundamentos` (`python_fundamentos`)**: Renderiza `python_fundamentos.html`, passando um dicionário estruturado com os conceitos, descrições e exemplos de fundamentos de Python.
    *   **`/ia_gemini` (`ia_gemini`)**:
        *   Aceita métodos `GET` (para exibir a página) e `POST` (para processar a pergunta do usuário).
        *   Se a API Gemini estiver configurada e uma pergunta for enviada, ela é processada pelo modelo Gemini e a resposta é exibida.
        *   Utiliza `flash()` para exibir mensagens de status (sucesso, erro, aviso) ao usuário.
        *   Passa a flag `GEMINI_API_CONFIGURED` para o template.
    *   **`/dicionario` (`dicionario`)**: Rota `GET` que carrega os termos do `dicionario.txt` e renderiza `dicionario.html`, exibindo-os.
    *   **`/dicionario/adicionar` (`adicionar_termo`)**: Rota `POST` que recebe dados de um formulário (`termo` e `definicao`), adiciona ao dicionário e salva. Redireciona de volta para `/dicionario`.
    *   **`/dicionario/editar/<path:termo_original>` (`editar_termo`)**:
        *   `GET`: Carrega o termo e sua definição e renderiza `editar_termo.html` para edição.
        *   `POST`: Recebe o `novo_termo` e `nova_definicao`, atualiza o dicionário (removendo o antigo e adicionando o novo, se o nome do termo mudar) e salva. Redireciona para `/dicionario`.
    *   **`/dicionario/deletar/<path:termo>` (`deletar_termo`)**: Rota `POST` que remove o termo especificado do dicionário e salva as alterações. Redireciona para `/dicionario`.

*   **Bloco de Execução Principal:**
    *   `if __name__ == "__main__": app.run(debug=True)`: Garante que o servidor de desenvolvimento Flask (`app.run()`) seja iniciado apenas quando o script `app.py` é executado diretamente (não quando importado como módulo). `debug=True` ativa o modo de depuração, que fornece mensagens de erro detalhadas e recarrega automaticamente o servidor após alterações no código.

---

Espero que esta documentação seja útil para o seu projeto!