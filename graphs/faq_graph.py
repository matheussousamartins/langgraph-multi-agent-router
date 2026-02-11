from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from state import AppState


#Node do FAQ
def faq_node(state: AppState):
    model = ChatOpenAI(model="gpt-5-nano")

    system_prompt = SystemMessage(
        content="""
            Você é um assistente especialista no framework LangGraph da LangChain.
            Sempre responda considerando LangGraph como biblioteca de agentes.
            Não confunda com grafos linguísticos.
            Seja técnico e objetivo.
            """
                )

    last_user_message = state["messages"][-1]
    response = model.invoke([system_prompt, last_user_message])

    return {
        "messages": [response],
        "steps": state.get("steps", 0) + 1,
    }


#Função que cria o subgrafo
def create_faq_graph():
    graph = StateGraph(AppState)

    graph.add_node("faq", faq_node)
    graph.set_entry_point("faq")
    graph.add_edge("faq", END)


    return graph.compile()
