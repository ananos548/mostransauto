from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.services.buses import BusManager
from src.schemas.bus_schemas import BusSchema

router = APIRouter(
    prefix="/buses",
    tags=["Buses"]
)

# =========================
# CREATE BUS
# =========================
@router.post("/")
async def create_bus(
    bus: BusSchema,
    service: BusManager = Depends(BusManager)
):
    result = await service.create_bus(bus)
    return {
        "message": "Bus created",
        "bus": dict(result._mapping)
    }


# =========================
# GET ALL BUSES
# =========================
@router.get("/")
async def get_all_buses(
    service: BusManager = Depends(BusManager)
):
    buses = await service.get_all_buses()
    return [dict(bus._mapping) for bus in buses]


# =========================
# GET BUS BY ID
# =========================
@router.get("/{bus_id}")
async def get_bus_by_id(
    bus_id: int,
    service: BusManager = Depends(BusManager)
):
    bus = await service.get_bus_by_id(bus_id)
    return dict(bus._mapping)


# =========================
# UPDATE BUS
# =========================
@router.put("/{bus_id}")
async def update_bus(
    bus_id: int,
    bus: BusSchema,
    service: BusManager = Depends(BusManager)
):
    result = await service.update_bus(bus_id, bus)
    return result


# =========================
# DELETE BUS
# =========================
@router.delete("/{bus_id}")
async def delete_bus(
    bus_id: int,
    service: BusManager = Depends(BusManager)
):
    result = await service.delete_bus(bus_id)
    return result


# =========================
# SEARCH BUSES
# ==================

@router.get("/search/")
async def search_buses(
    q: str,
    service: BusManager = Depends(BusManager)
):
    buses = await service.search_buses(q)
    return [dict(bus._mapping) for bus in buses]


# =========================
# CHANGE STATUS
# =========================
@router.patch("/{bus_id}/status")
async def change_status(
    bus_id: int,
    status: str,
    service: BusManager = Depends(BusManager)
):
    result = await service.change_status(bus_id, status)
    return result
