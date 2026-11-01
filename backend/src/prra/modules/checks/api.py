"""HTTP routes for the checks module."""

from fastapi import APIRouter

router = APIRouter(prefix="/checks", tags=["checks"])
