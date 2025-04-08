from flask import Flask, render_template, request, redirect, url_for
import json
import os
from Models.Aluno import Aluno

app = Flask(__name__)

CAMINHO_JSON = os.path.join("dados", "registro_de_alunos.json")

@app.route("/")
def index():
    return "Bem-vindo ao Sistema de Gerenciamento de Boletins!"

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        frequencia = int(request.form["frequencia"])
        notas = {}

        for materia in ["portugues", "matematica", "ingles", "fisica", "geografia", "quimica"]:
            notas[materia] = []
            for i in range(1, 5):
                campo = f"{materia}_nota{i}"
                notas[materia].append(float(request.form[campo]))

        novo_aluno = Aluno(nome=nome, frequencia=frequencia, notas=notas)
        salvar_aluno(novo_aluno)

        return redirect(url_for("index"))

    return render_template("cadastro.html")

def salvar_aluno(aluno):
    if os.path.exists(CAMINHO_JSON):
        with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
            dados = json.load(f)
    else:
        dados = []

    dados.append(aluno.to_dict())

    with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
        