import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse

# Placed here for initialize Django before using models
from config import settings
from api.user import router as user_router

# Create app
app = FastAPI(title="Authentication Sevice")

# Add routes
app.include_router(user_router)
# app.include_router(role_router)


# Add exception handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


# Add default
@app.get("/")
def root():
    return RedirectResponse("/docs")


from fastapi.responses import StreamingResponse


@app.get("/test")
async def test():
    ### Streaming example
    # from database.models.user import User
    # from schemas.user import User as UserSchema
    # async def get_users():
    #     async for user in User.objects.all():
    #         yield UserSchema.parse_obj(user.__dict__).json()
    # return StreamingResponse(get_users())

    ### Simple converting
    from django.db.models import QuerySet

    from database.models.user import User
    from database.utils import many_to_pydantic
    from schemas.user import User as UserSchema

    users: QuerySet = User.objects.all()
    return many_to_pydantic(users, UserSchema)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
