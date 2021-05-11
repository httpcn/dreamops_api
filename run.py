import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import login_router
from api import zbx_router, ansible_router, cloud_router, jenkins_router

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

app.include_router(router=login_router, prefix='/user', tags=['login api'])
app.include_router(router=zbx_router, prefix='/zabbix', tags=['zabbix api'])
app.include_router(router=ansible_router, prefix='/ansible', tags=['ansible_api'])
app.include_router(router=cloud_router, prefix='/cloud', tags=['cloud_api'])
app.include_router(router=jenkins_router, prefix='/jenkins', tags=['jenkins_api'])

if __name__ == '__main__':
    uvicorn.run(
        'run:app',
        host='192.168.3.25',
        port=8000,
        reload=True,
        workers=1
    )