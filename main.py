from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import userRouter

app = FastAPI(
    title="Motoring Innovation",
    version="1.0",
    summary="Api consumible Crud Usuarios",
    contact={
        "name": "Motoring Innovation",
        "url": "https://monitoringinnovation.com/",
        "email": "desarrollo@gpscontrol.co",
    },
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(userRouter.router)
