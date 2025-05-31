import os
import google.generativeai as genai
import datetime 
from dotenv import load_dotenv 
from flask import Flask, render_template, request, redirect, url_for, flash

load_dotenv() 

app = Flask(__name__)
app.secret_key = os.urandom(24)  

# --- Configuração da API do Gemini ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        print("API do Gemini configurada com sucesso.")
    except Exception as e:
        print(f"Erro ao configurar a API do Gemini: {e}")
        model = None 
else:
    print("AVISO: Chave da API do Gemini (GEMINI_API_KEY) não encontrada nas variáveis de ambiente. A funcionalidade de tutoria não funcionará.")

# --- Dicionário de Termos ---
DATA_DIR = "data"
DICIONARIO_FILE = os.path.join(DATA_DIR, "dicionario.txt")

def _ensure_data_dir_exists():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(DICIONARIO_FILE):
        with open(DICIONARIO_FILE, "w", encoding="utf-8") as f:
            # Adicionar alguns termos iniciais como exemplo
            f.write("Algoritmo:Uma sequência finita de instruções bem definidas e não ambíguas, que são executadas para resolver um problema específico.\n")
            f.write("Variável:Um espaço na memória do computador destinado a um dado que é alterado durante a execução de um algoritmo.\n")
            f.write("Loop:Uma estrutura de repetição que executa um bloco de código múltiplas vezes.\n")

_ensure_data_dir_exists()

def carregar_dicionario():
    termos = {}
    try:
        with open(DICIONARIO_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        termos[parts[0].strip()] = parts[1].strip()
                    else:
                        print(f"Aviso: Linha mal formatada no dicionário ignorada: {line}")
    except FileNotFoundError:
        _ensure_data_dir_exists() 
    return termos

def salvar_dicionario(termos):
    _ensure_data_dir_exists()
    with open(DICIONARIO_FILE, "w", encoding="utf-8") as f:
        for termo, definicao in sorted(termos.items()):
            f.write(f"{termo}:{definicao}\n")

# --- Processador de Contexto para injetar o ano atual ---
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.date.today().year}


# --- Rotas ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/equipe")
def equipe():
    equipe_info = [
        {
            "nome": "Demetrios Alejandro Tavares Barbosa",
            "linkedin": "https://www.linkedin.com/in/demetrios-alejandro-168039369/", 
        },
         
        {
             "nome": "Keitel Werner Cavalcanti Costa Hartel Filho",
             "linkedin": "https://www.linkedin.com/in/keitel-werner-738090360?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app"
         } ,
          
         {
             "nome": "Gabriel Mendes Palha",
             "linkedin": "https://www.linkedin.com/in/gabriel-palha-14a06b351/?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app",
         },
    ]
    return render_template("equipe.html", equipe=equipe_info)

@app.route("/python-fundamentos")
def python_fundamentos():
    fundamentos = {
        "estruturas_selecao": {
            "titulo": "Estruturas de Seleção",
            "conceito": "Permitem que o programa escolha entre diferentes caminhos de execução com base em condições (verdadeiro ou falso). As principais são `if`, `elif` (senão se) e `else` (senão).",
            "aplicacao": "Tomada de decisões em um programa, como verificar se um usuário tem permissão, classificar valores, ou controlar o fluxo de execução baseado em entradas.",
            "exemplo": """# Exemplo de if-elif-else
idade = 20
if idade < 12:
    categoria = "Criança"
elif idade < 18:
    categoria = "Adolescente"
else:
    categoria = "Adulto"
print(f"Com {idade} anos, a categoria é: {categoria}")"""
        },
        "estruturas_repeticao": {
            "titulo": "Estruturas de Repetição (Loops)",
            "conceito": "Permitem que um bloco de código seja executado várias vezes. As principais são `for` (para um número conhecido de iterações ou para iterar sobre sequências) e `while` (enquanto uma condição for verdadeira).",
            "aplicacao": "Processar itens em uma lista, ler linhas de um arquivo, repetir uma ação até que uma condição seja satisfeita, realizar cálculos repetitivos.",
            "exemplo": """# Exemplo de for (iterando sobre uma lista)
nomes = ["Ana", "Bruno", "Carlos"]
for nome in nomes:
    print(f"Olá, {nome}!")

# Exemplo de while (contagem regressiva)
contador = 5
while contador > 0:
    print(contador)
    contador -= 1 # Decrementa o contador
print("Fim!")"""
        },
        "vetores_matrizes": {
            "titulo": "Vetores e Matrizes (usando Listas)",
            "conceito": "Em Python, vetores (arrays unidimensionais) e matrizes (arrays bidimensionais ou multidimensionais) são comumente representados usando listas. Um vetor é uma lista simples, e uma matriz é uma lista de listas.",
            "aplicacao": "Armazenar coleções ordenadas de dados, como notas de alunos (vetor), pixels de uma imagem (matriz), ou representar tabuleiros de jogos (matriz).",
            "exemplo": """# Vetor (Lista)
notas = [7.5, 8.0, 6.5, 9.0]
print(f"Primeira nota: {notas[0]}")
notas.append(7.0) # Adiciona um elemento
print(f"Notas atualizadas: {notas}")

# Matriz (Lista de Listas)
matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Elemento na linha 1, coluna 2: {matriz[0][1]}") # (Lembre-se que índices começam em 0)
print(f"Linha central: {matriz[1]}")"""
        },
        "funcoes_procedimentos": {
            "titulo": "Funções e Procedimentos",
            "conceito": "Funções são blocos de código nomeados e reutilizáveis que realizam uma tarefa específica. Podem receber dados de entrada (parâmetros) e retornar um resultado (valor de retorno). Em Python, não há uma distinção formal entre 'função' e 'procedimento'; funções que não retornam um valor explicitamente, retornam `None`.",
            "aplicacao": "Organizar o código em partes menores e gerenciáveis, evitar repetição de código (princípio DRY - Don't Repeat Yourself), tornar o código mais legível e modular.",
            "exemplo": """# Função que calcula a área de um retângulo
def calcular_area_retangulo(largura, altura):
    area = largura * altura
    return area

area1 = calcular_area_retangulo(10, 5)
print(f"A área do retângulo é: {area1}")

# Procedimento (função que realiza uma ação, sem retorno explícito significativo)
def saudar(nome):
    print(f"Olá, {nome}! Bem-vindo(a).")

saudar("Estudante")"""
        },
        "tratamento_excecoes": {
            "titulo": "Tratamento de Exceções",
            "conceito": "Um mecanismo para lidar com erros (exceções) que ocorrem durante a execução de um programa. Usa os blocos `try` (tenta executar o código), `except` (captura e trata o erro), `else` (executa se não houver exceção no `try`) e `finally` (sempre executa, ocorrendo erro ou não).",
            "aplicacao": "Prevenir que o programa pare abruptamente devido a erros previsíveis, como divisão por zero, tentativa de abrir um arquivo inexistente, ou entrada de dados inválida pelo usuário.",
            "exemplo": """# Exemplo de tratamento de exceções
try:
    numerador = int(input("Digite o numerador: "))
    denominador = int(input("Digite o denominador: "))
    resultado = numerador / denominador
except ValueError:
    print("Erro: Entrada inválida. Por favor, digite números inteiros.")
except ZeroDivisionError:
    print("Erro: Não é possível dividir por zero.")
else:
    print(f"O resultado da divisão é: {resultado}")
finally:
    print("Operação de divisão finalizada.")"""
        }
    }
    return render_template("python_fundamentos.html", fundamentos=fundamentos)

@app.route("/ia_gemini", methods=["GET", "POST"])
def ia_gemini():
    resposta_gemini = None
    pergunta_usuario = ""
    if request.method == "POST":
        pergunta_usuario = request.form.get("pergunta")
        if not model:
            flash("A API do Gemini não está configurada. Por favor, defina a variável de ambiente GEMINI_API_KEY.", "error")
        elif pergunta_usuario:
            try:
                prompt_completo = f"Você é um tutor de programação Python para iniciantes. Responda a seguinte pergunta de forma clara, didática e com exemplos simples, se aplicável: {pergunta_usuario}"
                response = model.generate_content(prompt_completo)
                resposta_gemini = response.text
            except Exception as e:
                resposta_gemini = f"Ocorreu um erro ao contatar a API do Gemini: {e}"
                flash(f"Erro na API do Gemini: {e}", "error")
        else:
            flash("Por favor, digite uma pergunta.", "warning")

    return render_template("ia_gemini.html", 
                           pergunta_usuario=pergunta_usuario, 
                           resposta_gemini=resposta_gemini,
                           GEMINI_API_CONFIGURED=bool(model)) 

@app.route("/dicionario", methods=["GET"])
def dicionario():
    termos = carregar_dicionario()
    return render_template("dicionario.html", termos=termos)

@app.route("/dicionario/adicionar", methods=["POST"])
def adicionar_termo():
    termo = request.form.get("termo", "").strip()
    definicao = request.form.get("definicao", "").strip()

    if not termo or not definicao:
        flash("Termo e definição são obrigatórios.", "error")
    else:
        termos = carregar_dicionario()
        if termo in termos:
            flash(f"O termo '{termo}' já existe no dicionário.", "warning")
        else:
            termos[termo] = definicao
            salvar_dicionario(termos)
            flash(f"Termo '{termo}' adicionado com sucesso!", "success")
    return redirect(url_for("dicionario"))

@app.route("/dicionario/editar/<path:termo_original>", methods=["GET", "POST"])
def editar_termo(termo_original):
    termos = carregar_dicionario()
    if termo_original not in termos:
        flash(f"Termo '{termo_original}' não encontrado.", "error")
        return redirect(url_for("dicionario"))

    if request.method == "POST":
        novo_termo = request.form.get("novo_termo", "").strip()
        nova_definicao = request.form.get("nova_definicao", "").strip()

        if not novo_termo or not nova_definicao:
            flash("Novo termo e nova definição são obrigatórios.", "error")
            return render_template("editar_termo.html", termo_original=termo_original, definicao_original=termos[termo_original], novo_termo=novo_termo, nova_definicao=nova_definicao)

        if novo_termo != termo_original and novo_termo in termos:
            flash(f"O novo termo '{novo_termo}' já existe no dicionário.", "warning")
            return render_template("editar_termo.html", termo_original=termo_original, definicao_original=termos[termo_original], novo_termo=novo_termo, nova_definicao=nova_definicao)

        del termos[termo_original]
        termos[novo_termo] = nova_definicao
        salvar_dicionario(termos)
        flash(f"Termo '{novo_termo}' atualizado com sucesso!", "success")
        return redirect(url_for("dicionario"))

    return render_template("editar_termo.html", termo_original=termo_original, definicao_original=termos[termo_original])

@app.route("/dicionario/deletar/<path:termo>", methods=["POST"])
def deletar_termo(termo):
    termos = carregar_dicionario()
    if termo in termos:
        del termos[termo]
        salvar_dicionario(termos)
        flash(f"Termo '{termo}' deletado com sucesso!", "success")
    else:
        flash(f"Termo '{termo}' não encontrado.", "error")
    return redirect(url_for("dicionario"))

if __name__ == "__main__":
    app.run(debug=True)