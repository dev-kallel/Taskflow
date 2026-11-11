import os
import sqlite3
import click
from flask import (Flask, abort, app, flash, redirect, render_template,
request, url_for)
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
        return render_template("index.html", projects=sql.list_projects())
    @app.route("/projects/new", methods=["GET", "POST"])

    def project_new():
        if request.method == "POST":
            key = request.form.get("key", "").strip()
            name = request.form.get("name", "").strip()
            if not key or not name:
                flash("Sigla e nome são obrigatórios.", "error")
            else:
                try:
                    pid = sql.create_project(key, name, request.form.get("description", ""))
                    flash("Projeto criado!", "ok")
                    return redirect(url_for("project_detail", project_id=pid))
                except sqlite3.IntegrityError: # violou o UNIQUE da sigla
                    flash(f"Já existe um projeto com a sigla {key.upper()}.", "error")
        return render_template("project_form.html", project=None)

    @app.route("/projects/<int:project_id>")
    def project_detail(project_id):
        project = sql.get_project(project_id) or abort(404)
        return render_template("project.html", project=project)

    @app.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
    def project_edit(project_id):
        project = sql.get_project(project_id) or abort(404)

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if not name:
                flash("Nome é obrigatório.", "error")
            else:
                sql.update_project(project_id, name, request.form.get("description", ""))
                flash("Projeto atualizado.", "ok")
                return redirect(url_for("project_detail", project_id=project_id))

        return render_template("project_form.html", project=project)

    @app.post("/projects/<int:project_id>/delete")
    def project_delete(project_id):
        sql.delete_project(project_id)
        flash("Projeto excluído.", "ok")
        return redirect(url_for("index"))
app = create_app()