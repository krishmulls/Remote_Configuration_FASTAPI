"""Defining Pm100d APIs."""

import asyncio
import time

import fastapi

import schemas
from dependencies import get_current_user
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class DeviceValues(BaseModel):
    """Defining base model for input request."""

    deviceID: int = None
    wavelength: float = None


@router.get("/pm100d")
async def pm100d():
    await asyncio.sleep(10)
    return {"status": "ok"}


@router.get("/pm100d/{deviceID}/getwavelength")
async def get_wavelength(
    deviceID, user: schemas.UserBase = fastapi.Depends(get_current_user)
):
    """Returns wavelength of the power meter."""
    return {deviceID: "123"}  # dummy return


@router.get("/pm100d/{deviceID}/info")
async def info(deviceID,
               user: schemas.UserBase = fastapi.Depends(get_current_user)):
    """Print Information of powermeter."""
    await time.sleep(5)
    return {"Device Id": deviceID}  # dummy return


@router.get("/pm100d/{deviceID}/getvalue")
async def get_value(
    deviceID,
    averaging_samples=4,
    user: schemas.UserBase = fastapi.Depends(get_current_user),
):
    """Measure and return current power.

    Per measurement avergaing_samples no. of samples (each takes ca. 3ms)
    will be taken and averaged over.

    Args:
        averaging_samples (int): the average sampling.

    Returns:
        (float):the current power.

    """
    return {deviceID: "12.3"}  # dummy return


@router.post("/pm100d/start")
async def start(
    device_value: DeviceValues,
    user: schemas.UserBase = fastapi.Depends(get_current_user),
):
    """Start device."""
    return {"Device Id": device_value.deviceID}  # dummy return


@router.post("/pm100d/stop")
async def stop(
    device_value: DeviceValues,
    user: schemas.UserBase = fastapi.Depends(get_current_user),
):
    """Stop device."""
    return {"status": "ok"}


@router.post("/pm100d/zero")
async def zero(
    device_value: DeviceValues,
    user: schemas.UserBase = fastapi.Depends(get_current_user),
):
    """Zeroes the powermeter."""
    return {device_value.deviceID: "Setted to zero"}  # dummy return


@router.post("/pm100d/setwavelength")
async def set_wavelength(
    device_value: DeviceValues,
    user: schemas.UserBase = fastapi.Depends(get_current_user),
):
    """Set wavelength of the power meter."""
    return {device_value.deviceID: "123"}  # dummy return
