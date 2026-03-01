import sqlite3

conn = sqlite3.connect("database.db")
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

print("Banco criado com sucesso!")
