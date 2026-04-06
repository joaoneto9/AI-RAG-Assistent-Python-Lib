from src.vector_database_embagge import get_collection

database = get_collection()

print("loading the vector database")

def prompt_to_ai_assistant(question: str) -> str:
    documentation = database.query(
        query_texts=[
            question
        ],
        n_results=5
    )

    if not documentation["documents"]:
        return "ERRO na busca pela documentacao, tente novamente"

    documentation = ["\n".join(d) for d in documentation["documents"]]
    
    prompt = f"""
    Voce e um assistente em python, especificamente na lib Langgraph.
    Diante dessas Documentacoes, responda a Pergunta:

    Documentacoes: {documentation}

    Pergunta: {question}

    [INFIRA QUAL DAS INFORMACOES PASSADAS E RELEVANTE PARA A PERGUNTA]
    """

    return prompt


