from fpdf import FPDF
import sqlite3

def gerar_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, "Relatório de Pagamentos", ln=True, align='C')
    pdf.ln(10)

    conn = sqlite3.connect('condominio.db')
    c = conn.cursor()
    c.execute('SELECT * FROM pagamentos')
    pagamentos = c.fetchall()
    conn.close()

    for pagamento in pagamentos:
        pdf.cell(200, 10, f"Apartamento: {pagamento[1]}, Mês: {pagamento[2]}, Status: {pagamento[3]}", ln=True)

    caminho_pdf = "relatorio_pagamentos.pdf"
    pdf.output(caminho_pdf)
    return caminho_pdf
