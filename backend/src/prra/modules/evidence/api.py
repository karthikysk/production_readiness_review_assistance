"""HTTP routes for the evidence module."""

from fastapi import APIRouter

router = APIRouter(prefix="/evidence", tags=["evidence"])
