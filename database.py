import psycopg2
import os

# Conexão com PostgreSQL no Render
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://condominio_db_wyhk_user:jNOIbWlTJIMw8Pluc3yw9m74CISkid6n@dpg-cucpqf9opnds73ak841g-a/condominio_db_wyhk")

def conectar():
    """Conecta ao PostgreSQL e retorna a conexão e o cursor."""
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    return conn, conn.cursor()

def criar_tabelas():
    """Cria as tabelas do banco de dados se não existirem"""
    conn, c = conectar()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pagamentos (
            id SERIAL PRIMARY KEY,
            apartamento TEXT NOT NULL,
            mes TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Banco de dados PostgreSQL configurado com sucesso!")

if __name__ == "__main__":
    criar_tabelas()
