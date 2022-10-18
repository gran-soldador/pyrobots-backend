from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def helloworld():
    return {"message": "Hello World"}
