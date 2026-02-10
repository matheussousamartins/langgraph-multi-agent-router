from typing import Annotated, TypedDict, Sequence
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AppState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    route: str | None
    steps: int
