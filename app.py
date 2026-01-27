from fastapi import FastAPI
from routes import home, api

app = FastAPI()

app.include_router(home.router)
app.include_router(api.router)
