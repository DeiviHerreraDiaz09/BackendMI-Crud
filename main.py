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
    docs_url=None, 
    redoc_url=None  
)

app.include_router(userRouter.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
