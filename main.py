import json
import random
import os

from flask import Flask, request, jsonify
from flask import render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form.get("nome")
    email = request.form.get("email")

    if not nome or not email:
        return "Preencha todos os campos!", 400

    # Gerar matrícula: 2025XXXXX25
    numeros_aleatorios = str(random.randint(10000, 99999))
    matricula = f"2025{numeros_aleatorios}25"

    novo_aluno = {
        "matricula": matricula,
        "nome": nome,
        "email": email,
        "materias": {
            "portugues": [],
            "matematica": [],
            "ingles": [],
            "fisica": [],
            "geografia": [],
            "quimica": []
        },
        "frequencia": None,
        "status_final": None
    }

    caminho_arquivo = os.path.join(os.path.dirname(__file__), "registro_de_alunos.json")

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = []

    dados.append(novo_aluno)

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

    return f"Aluno {nome} cadastrado com sucesso! Matrícula: {matricula}"

@app.route("/boletim")
def boletim():
    return render_template("boletim.html")


@app.route("/cadastrar_boletim", methods=["POST"])
def cadastrar_boletim():
    nome = request.form.get("nome")
    nota1 = request.form.get("nota1")
    nota2 = request.form.get("nota2")
    nota3 = request.form.get("nota3")
    nota4 = request.form.get("nota4")

    if not nome or not nota1 or not nota2 or not nota3 or not nota4:
        return "Preencha todos os campos!", 400

    try:
        notas = list(map(float, [nota1, nota2, nota3, nota4]))
    except ValueError:
        return "As notas devem ser números válidos.", 400

    media = sum(notas) / 4
    status = "Aprovado" if media >= 6 else "Reprovado"

    return f"Aluno {nome} - Média: {media:.2f} - Status: {status}"
