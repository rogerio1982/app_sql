# Agente de IA para Consultas SQL

Este projeto é um agente inteligente que converte perguntas em linguagem natural em consultas SQL, executa essas consultas em um banco de dados SQLite e retorna os resultados de forma amigável via interface web.

## Funcionalidades
- Interface web simples para enviar perguntas sobre os dados.
- Conversão automática de perguntas em SQL usando LLM (OpenAI GPT-4o-mini).
- Execução segura de consultas (apenas SELECT permitido).
- Exibição do SQL gerado e do resultado da consulta.

## Estrutura do Projeto
- `app.py`: Backend Flask, integra com o LLM e executa as consultas.
- `init_db.py`: Script para criar e popular o banco de dados SQLite.
- `templates/index.html`: Interface web para interação com o agente.
- `requirements.txt`: Dependências do projeto.
- `.env`: Chave de API da OpenAI.

## Como usar
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure sua chave OpenAI em `.env`.
3. Inicialize o banco de dados:
   ```bash
   python init_db.py
   ```
4. Rode o servidor Flask:
   ```bash
   python app.py
   ```
5. Acesse `http://localhost:8080` no navegador.

## Observações
- Apenas comandos SELECT são permitidos por segurança.
- O modelo LLM gera o SQL com base no schema do banco.
- O projeto pode ser expandido para outros bancos ou comandos.

## Exemplo de uso
Pergunta: "Liste os produtos cadastrados"

SQL Gerado:
```sql
SELECT * FROM produtos;
```

Resultado: (lista dos produtos, se a tabela existir)

---

Desenvolvido por Roger, 2026.
