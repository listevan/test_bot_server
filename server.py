from fastapi import FastAPI
from pydantic import BaseModel

import os
import getpass
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

from langchain.chat_models import init_chat_model
model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

from langchain_core.messages import HumanMessage

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
workflow = StateGraph(state_schema=MessagesState)

# Define the function that calls the model
def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": response}

# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
model_app = workflow.compile(checkpointer=memory)

class Request(BaseModel):
    payload: str

app = FastAPI()

@app.post("/")
async def post_root(item: Request):
    # act on payload
    config = {"configurable": {"thread_id": "abc123"}}
    output = model_app.invoke({"messages": [HumanMessage(item.payload)]}, config)
    return output

