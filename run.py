import uvicorn
from fastapi import FastAPI

from auth import login_router

app = FastAPI()

app.include_router(router=login_router, prefix='/user', tags=['login'])

if __name__ == '__main__':
    uvicorn.run(
        'run:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        workers=1
    )