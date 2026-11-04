import os

import click
from flask import Flask, render_template

import db_sql as sql

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-troque-em-producao"),
        SQL_DATABASE=os.environ.get("SQL_DATABASE", "taskflow.db"),
    )

    if test_config:
        app.config.update(test_config)
    app.teardown_appcontext(sql.close_db) # fecha a conexão no fim de cada requisição
    register_cli(app)
    register_html_routes(app)
    return app

def register_cli(app):
    @app.cli.command("init-db")
    def init_db_command():
        """Recria as tabelas do banco SQL (APAGA os dados!)."""
        sql.init_db()
        click.echo("Banco SQL criado.")

def register_html_routes(app):
    @app.route("/")
    def index():
        projetos = ["App Mobile da Cantina", "API de Pagamentos"]
        return render_template("index.html", projetos=projetos)
    
app = create_app()