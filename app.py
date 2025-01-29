from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import os
from report import gerar_pdf
from whatsapp import enviar_mensagem

app = Flask(__name__)

# Criar o banco de dados
def init_db():
    conn = sqlite3.connect('condominio.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            apartamento TEXT NOT NULL,
            mes TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    conn = sqlite3.connect('condominio.db')
    c = conn.cursor()
    c.execute('SELECT * FROM pagamentos')
    pagamentos = c.fetchall()
    conn.close()
    return render_template('dashboard.html', pagamentos=pagamentos)

@app.route('/criar', methods=['GET', 'POST'])
def criar_pagamento():
    if request.method == 'POST':
        apartamento = request.form['apartamento']
        mes = request.form['mes']
        status = request.form['status']

        conn = sqlite3.connect('condominio.db')
        c = conn.cursor()
        c.execute('INSERT INTO pagamentos (apartamento, mes, status) VALUES (?, ?, ?)',
                  (apartamento, mes, status))
        conn.commit()
        conn.close()

        # Enviar notificação via WhatsApp (se o pagamento estiver pendente)
        if status.lower() == "pendente":
            enviar_mensagem(f"O pagamento do apartamento {apartamento} para {mes} está pendente!")

        return redirect(url_for('dashboard'))

    return render_template('criar_pagamento.html')

@app.route('/relatorio')
def relatorio():
    caminho_pdf = gerar_pdf()
    return send_file(caminho_pdf, as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
