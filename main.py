from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
	'http://localhost:3000'
]

app.add_middleware(
	CORSMiddleware,
	allow_origins = origins,
	allow_credentials = True,
	allow_methods = ['GET'],
	allow_headers = ['Content-Type','application/xml']
)

@app.get('/')
async def main():
	return {'Hello world!'}