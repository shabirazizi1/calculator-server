from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import calculator, history

app = FastAPI(title="OOP Calculator Server")

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount APIRouters
app.include_router(calculator.router)
app.include_router(history.router)