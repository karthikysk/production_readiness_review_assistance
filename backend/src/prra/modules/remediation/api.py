"""HTTP routes for the remediation module."""

from fastapi import APIRouter

router = APIRouter(prefix="/remediation", tags=["remediation"])
