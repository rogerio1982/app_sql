import sqlite3
import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==========================
# CONFIGURAÇÃO DO BANCO
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

print("Arquivo do banco:", DATABASE)


# ==========================
# CRIAR BANCO AUTOMATICAMENTE
# ==========================
def inicializar_banco():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto TEXT,
        categoria TEXT,
        preco REAL,
        quantidade INTEGER,
        data TEXT
    )
    """)

    # Verifica se já existem dados
    cursor.execute("SELECT COUNT(*) FROM vendas")
    total = cursor.fetchone()[0]

    if total == 0:
        print("[INFO] Inserindo dados iniciais...")
        cursor.execute("""
        INSERT INTO vendas (produto, categoria, preco, quantidade, data)
        VALUES
        ('Notebook', 'Eletrônicos', 3500, 5, '2024-01-10'),
        ('Mouse', 'Eletrônicos', 80, 20, '2024-01-15'),
        ('Cadeira', 'Móveis', 500, 3, '2024-02-01'),
        ('Mesa', 'Móveis', 900, 2, '2024-02-10')
        """)

    conn.commit()
    conn.close()


# ==========================
# GERAR SQL VIA IA
# ==========================
def gerar_sql(pergunta):

    prompt = f"""
Você é um especialista em SQL para SQLite.

REGRAS OBRIGATÓRIAS:
1. Utilize APENAS a tabela chamada 'vendas'.
2. A tabela possui somente as seguintes colunas:
   - id
   - produto
   - categoria
   - preco
   - quantidade
   - data
3. Gere SOMENTE consultas SELECT.
4. NÃO utilize INSERT, UPDATE, DELETE, DROP, ALTER ou qualquer outro comando que modifique dados.
5. NÃO utilize outras tabelas.
6. NÃO invente colunas.
7. Sempre adicione LIMIT 100 ao final da consulta.
8. Retorne APENAS o SQL puro, sem explicações, sem markdown, sem comentários.

Exemplo válido:
SELECT produto, SUM(preco * quantidade) AS total
FROM vendas
GROUP BY produto
LIMIT 100;

Pergunta:
{pergunta}
"""

    print("[DEBUG] Prompt enviado:\n", prompt)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    print("[DEBUG] SQL gerado:", sql)

    return sql


# ==========================
# EXECUTAR SQL COM SEGURANÇA
# ==========================
def executar_sql(sql):

    sql_lower = sql.lower()

    print("[DEBUG] SQL recebido:", sql)

    if not sql_lower.startswith("select"):
        return {"erro": "Apenas consultas SELECT são permitidas."}

    palavras_proibidas = ["insert", "update", "delete", "drop", "alter", "create"]
    for palavra in palavras_proibidas:
        if palavra in sql_lower:
            return {"erro": "Comando não permitido."}

    if "vendas" not in sql_lower:
        return {"erro": "Apenas a tabela vendas pode ser consultada."}

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        colunas = [desc[0] for desc in cursor.description]
        dados = cursor.fetchall()
        resultado = [dict(zip(colunas, linha)) for linha in dados]
    except Exception as e:
        resultado = {"erro": str(e)}
    finally:
        conn.close()

    return resultado


# ==========================
# ROTAS FLASK
# ==========================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/consulta", methods=["POST"])
def consulta():
    try:
        pergunta = request.json.get("pergunta")
        print("[INFO] Pergunta recebida:", pergunta)

        sql = gerar_sql(pergunta)
        resultado = executar_sql(sql)

        return jsonify({
            "pergunta": pergunta,
            "sql_gerado": sql,
            "resultado": resultado
        })

    except Exception as e:
        print("[ERRO]", e)
        return jsonify({"erro": str(e)}), 500


# ==========================
# INICIAR APLICAÇÃO
# ==========================
if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True, host="0.0.0.0", port=8080)