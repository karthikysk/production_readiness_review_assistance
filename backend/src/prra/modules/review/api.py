"""HTTP routes for the review module."""

from fastapi import APIRouter

router = APIRouter(prefix="/review", tags=["review"])
