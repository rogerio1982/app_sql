# teste.py
# Script para testar o LLM (Large Language Model)

def testar_llm():
    # Exemplo simples de teste: simula uma chamada ao LLM
    prompt = "Qual é a capital da França?"
    resposta_esperada = "Paris"
    # Aqui você substituiria pela chamada real ao LLM
    resposta_obtida = "Paris"  # Simulação
    assert resposta_obtida == resposta_esperada, f"Esperado: {resposta_esperada}, Obtido: {resposta_obtida}"
    print("Teste do LLM passou com sucesso!")

if __name__ == "__main__":
    testar_llm()
