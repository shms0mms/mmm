
from fastapi import FastAPI
from src.auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS

origins = [
	"http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware	,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)



# роутеры
app.include_router(router=auth_router)