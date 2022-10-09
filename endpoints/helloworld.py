from fastapi import APIRouter
from db import *

router = APIRouter()


@router.get("/")
async def helloworld():
    return {"message": "Hello World"}


@router.get("/newmsg/{text}")
async def newmsg(text: str):
    with db_session:
        msg = TestMessage(text=text)
        msg.flush()
        msgid = msg.msgid
    return {"status": "created", "id": msgid}


@router.get("/getmsg/{id}")
async def getmsg(id: int):
    with db_session:
        msg = TestMessage[id].text
    return {"msg": msg}
