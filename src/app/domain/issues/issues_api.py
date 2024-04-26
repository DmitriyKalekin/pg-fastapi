from fastapi import FastAPI, APIRouter, Path, Body
from fastapi.responses import JSONResponse
from .deps import AIssuesUC
from .dto import *

prefix = "/api/v1/issues"
router = APIRouter(prefix=prefix, tags=["issues"])

# TODO: add api functions
