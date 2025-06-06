import requests
import json

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import os
import getpass
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

if not os.environ.get("BOT_WEBHOOK"):
    os.environ["BOT_WEBHOOK"] = getpass.getpass("Enter BOT Webhook: ")

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

app = FastAPI()

@app.post("/")
async def post_root(request: Request):
    # act on payload
    body = await request.json()

    if "challenge" in body:
        # Required for Feishu verification
        return JSONResponse(content={"challenge": body["challenge"]})

    # Normal event
    text = ' '.join(json.loads(body['event']['message']['content'])['text'].split()[1:])
    sender_openid = body['event']['sender']['sender_id']['open_id']
    print("Received Message:", text)

    config = {"configurable": {"thread_id": "123456"}}
    output = model_app.invoke({"messages": [HumanMessage(text)]}, config)

    # Post back to Feishu
    headers = {
        "Content-Type": "application/json"
    }
    output_text: str = output['messages'][-1].content
    print(output_text)
    content={"receive_id": sender_openid,
            "msg_type": "text",
            "content": "{\"text\":\""+output_text+"\"}"}
    response = requests.post(os.environ["BOT_WEBHOOK"], json=content, headers=headers)
    print(response.status_code)

    return JSONResponse(content={"code": 0})

