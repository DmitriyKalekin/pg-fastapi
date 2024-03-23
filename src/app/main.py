from fastapi import FastAPI
from app.domain import routers

app = FastAPI()

for router in routers:
    app.include_router(router)
