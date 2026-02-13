from langchain_core.tools import tool


@tool
def generate_structured_plan(objective: str) -> str:
    """
    Gera um plano estruturado com etapas, entregáveis e métricas.
    Use quando o usuário pedir plano, roadmap ou organização de tarefa.
    """
    return f"""
            Plano Estruturado para: {objective}

            1. Definição do Escopo
            - Clarificar objetivos
            - Identificar requisitos

            2. Arquitetura e Estratégia
            - Definir tecnologias
            - Modelar fluxos

            3. Implementação
            - Desenvolvimento incremental
            - Testes contínuos

            4. Validação
            - Revisão técnica
            - Ajustes

            5. Entrega
            - Documentação
            - Deploy
            """
