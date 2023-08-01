from fastapi import FastAPI
from .routers import users, recommendations


app = FastAPI()

app.include_router(users.router)
app.include_router(recommendations.router)


@app.get("/")
async def root():
    return {"message": "root"}
