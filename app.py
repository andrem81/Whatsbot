from fastapi import FastAPI, Request

from evolution_api import send_whats_message
from chains import get_conversational_rag_chain

app = FastAPI()

conversation_rag_chain = get_conversational_rag_chain()


@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()

    data = payload.get("data", {})
    key = data.get("key", {})
    message_data = data.get("message", {})

    chat_id = key.get("remoteJid")
    message = message_data.get("conversation")

    if key.get("fromMe"):
        return {"status": "ignored"}

    if chat_id and message and not chat_id.endswith("@g.us"):
        ai_response = conversation_rag_chain.invoke(
            input={'input':message},
            config={'configurable': {'session_id': chat_id}},
        )['answer']
        send_whats_message(
            number=chat_id,
            text=ai_response,
        )
        return {"status": "ignored"}
    return {"status": "ok"}
