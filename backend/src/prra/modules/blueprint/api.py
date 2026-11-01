"""HTTP routes for the blueprint module."""

from fastapi import APIRouter

router = APIRouter(prefix="/blueprint", tags=["blueprint"])
