# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from routers import llm_route, text_route
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.include_router(llm_route.router)
app.include_router(text_route.router)

app.mount("/db_vectorial", StaticFiles(directory="db_vectorial"), name="db_vectorial")
app.mount("/binaries_files", StaticFiles(directory="binaries_files"), name="binaries_files")

origins =[
    "http://localhost:8051",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

