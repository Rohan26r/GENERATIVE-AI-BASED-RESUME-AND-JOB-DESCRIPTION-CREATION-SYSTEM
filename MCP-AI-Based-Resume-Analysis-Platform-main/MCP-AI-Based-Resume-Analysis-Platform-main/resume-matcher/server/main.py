"""
Resume Matcher — FastAPI application entry point.
Bootstraps MCP tool registry then mounts all routes.
"""

import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load all MCP tools on startup
    from mcp.server import load_tools
    load_tools()
    logger.info("Resume Matcher MCP server ready.")
    yield


app = FastAPI(
    title="Resume Matcher MCP API",
    version="1.0.0",
    description="MCP-first resume analysis platform",
    lifespan=lifespan,
)

# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routes import router  # noqa: E402
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
