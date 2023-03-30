import uvicorn

# from database.models.user import User
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# from crudgenerator import generate
from api.user import router as user_router
from api.role import router as role_router

app = FastAPI(title="Authentication Sevice")
# router = generate(User, "entities.user")
# app.include_router(router)

app.include_router(user_router)
app.include_router(role_router)


@app.get("/")
def root():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
