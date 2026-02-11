from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage

from state import AppState


def create_faq_graph():
    model = ChatOpenAI(model="gpt-5-nano")

    def faq_node(state: AppState):
        last_user_message = state["messages"][-1].content

        prompt = f"""
            Responda de forma clara e objetiva à pergunta abaixo.
            Seja direto, conciso e didático.

            Pergunta: "{last_user_message}"
            """

        response = model.invoke(prompt)

        return {
            "messages": [AIMessage(content=response.content)],
            "steps": state.get("steps", 0) + 1,
        }

    graph = StateGraph(AppState)

    graph.add_node("faq", faq_node)
    graph.set_entry_point("faq")
    graph.add_edge("faq", END)

    return graph.compile()
