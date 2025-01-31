from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, conlist
import cohere
from cohere import ClassifyExample

import os
from dotenv import load_dotenv

from typing import Union

load_dotenv()

co = cohere.ClientV2(os.getenv('COHERE_API_KEY'))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or whatever port your frontend is running on
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
  
@app.get("/cohere")
def read_cohere():
  res = co.chat(
    model="command-r-plus-08-2024",
    messages=[
        {
            "role": "user",
            "content": "Write a title for a blog post about API design. Only output the title text.",
        }
    ],
  )
  print(res.message.content[0].text) # "The Ultimate Guide to API Design: Best Practices for Building Robust and Scalable APIs"

  return {"res": res.message.content[0].text}


class ChatMessage(BaseModel):
    message: str

@app.post("/cohere/test")
async def read_cohere_test(chat_message: ChatMessage):
  res = co.chat(
    model="command-r-plus-08-2024",
    messages=[
        {
            "role": "user",
            "content": chat_message.message,
        }
    ],
  )

  return {"response": res.message.content[0].text}