import os
import operator

from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage,AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama

class State(TypedDict):
    msg: Annotated[list[AnyMessage],operator.add]

class SimpleChatAgent():
    def __init__(self):
        ollamaUrl = os.getenv("OLLAMA_BASE_URL","localhost:11434")
        print(f"ollama base_url:{ollamaUrl}")

        graph = StateGraph(State)
        graph.add_node("chat",self.chatNode)

        graph.add_edge(START,"chat")
        graph.add_edge("chat",END)

        memory = MemorySaver()

        self.graph = graph.compile(checkpointer=memory)

        self.model = ChatOllama(
            base_url=ollamaUrl,
            model="gemma3:4b",
            template=0.5,
            verbose=True
        )

    async def chatNode(self,state:State) -> State:
        question = state["msg"][-1]
        print(f"question:{question}")
        answer = ""
        async for chunk in self.model.astream(input=state["msg"]):
            answer = answer + chunk.content
        print(f"answer:{answer}")
        return {"msg":[AIMessage(answer)]}
    
    def astream(self,chatId:str,message:str):
        return self.graph.astream(
            input = {"msg": [{"role": "user", "content": message}]},
            config = {"configurable": {"thread_id": chatId}},
            stream_mode = "messages",
            debug = True
        )
