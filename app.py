from flask import Flask, render_template, flash, redirect, url_for
app = Flask(__name__)
app.secret_key = "dev-aula-1"

@app.route("/")
def index():
    projetos = ["App Mobile da Cantina", "API de Pagamentos", "API de senhas", "Sistema de Gestão de Estoque"]
    return render_template("index.html", projetos=projetos)


@app.route("/ola/<nome>")
def ola(nome):
    return f"Olá, {nome}! Bem-vindo ao TaskFlow."

@app.route("/teste-flash")
def teste_flash():
    flash("Algo deu errado. Esta é uma mensagem de erro.", "error")
    return redirect(url_for("index"))