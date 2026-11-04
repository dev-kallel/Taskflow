"""Executa um arquivo .sql no banco taskflow.db e mostra o resultado de cada comando.
Uso: python executar.py nome_do_arquivo.sql
"""
import sqlite3
import sys
conn = sqlite3.connect("taskflow.db")
conn.execute("PRAGMA foreign_keys = ON") # liga a checagem de FOREIGN KEY
texto = open(sys.argv[1], encoding="utf-8").read()

# remove linhas de comentário (--) e separa os comandos pelo ;
linhas = [l for l in texto.splitlines() if not l.strip().startswith("--")]
comandos = [c.strip() for c in "\n".join(linhas).split(";") if c.strip()]

for comando in comandos:
    print(">>", comando.splitlines()[0][:70])
    try:
        cur = conn.execute(comando)
        if cur.description: # foi um SELECT: mostra a tabela
            print(" " + " | ".join(col[0] for col in cur.description))
            for linha in cur.fetchall():
                print(" " + " | ".join(str(v) for v in linha))
        else:
            print(f" OK ({cur.rowcount} linha(s) afetada(s))")
    except sqlite3.Error as erro:
        print(f" ERRO: {erro}")
conn.commit()
conn.close()