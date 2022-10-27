from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile, Response
from endpoints.validation import image_to_string
from db import *
from .functions_jwt import *
from io import BytesIO
from PIL import Image
from starlette.responses import StreamingResponse

router = APIRouter()


@router.get("/lista-robots")
async def listar_robots(user_id: int = Depends(authenticated_user)):
    with db_session:
        lista = [{'id': r.robot_id, 'nombre': r.nombre}
                 for r in Usuario[user_id].robot]
        if lista == []:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='No se encontraron robots')
        return lista


#  Me devuelve el string de la imagen
@router.post("/imagen_funciona")
async def imagen_funciona():
    myPath = image_to_string()
    return myPath


# ANDA- SUBE UNA IMAGEN, ME MUESTRA LA MISMA IMAGEN SUBIDA

# @router.post("/vector_image")
# def image_filter(img: UploadFile = File(...)):
#     original_image = Image.open(img.file)
#     #original_image = original_image.filter(ImageFilter.BLUR)
#     filtered_image = BytesIO()
#     original_image.save(filtered_image, "JPEG")
#     filtered_image.seek(0)
#     return Response(content= filtered_image.getvalue(), media_type="image/jpeg")
#     return StreamingResponse(filtered_image, media_type="image/jpeg")
    