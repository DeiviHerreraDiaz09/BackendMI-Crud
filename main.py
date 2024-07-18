from fastapi import FastAPI
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


app.include_router(userRouter.router)
