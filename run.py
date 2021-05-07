import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import login_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:9528",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=login_router, prefix='/user', tags=['login'])

if __name__ == '__main__':
    uvicorn.run(
        'run:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        workers=1
    )