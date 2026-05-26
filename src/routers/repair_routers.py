from fastapi import APIRouter, Depends

from src.services.repairs import RepairManager
from src.schemas.repair_schemas import RepairSchema

router = APIRouter(
    prefix="/repairs",
    tags=["Repairs"]
)


# =========================
# CREATE REPAIR
# =========================
@router.post("/")
async def create_repair(
    repair: RepairSchema,
    service: RepairManager = Depends(RepairManager)
):
    result = await service.create_repair(repair)
    return {
        "message": "Repair created",
        "repair": dict(result._mapping)
    }


# =========================
# GET ALL REPAIRS
# =========================
@router.get("/")
async def get_all_repairs(
    service: RepairManager = Depends(RepairManager)
):
    repairs = await service.get_repairs()
    return [dict(r._mapping) for r in repairs]


# =========================
# GET REPAIR BY ID
# =========================
@router.get("/{repair_id}")
async def get_repair_by_id(
    repair_id: int,
    service: RepairManager = Depends(RepairManager)
):
    repair = await service.get_repair_by_id(repair_id)
    return dict(repair._mapping)


# =========================
# GET REPAIRS BY BUS
# =========================
@router.get("/bus/{bus_id}")
async def get_repairs_by_bus(
    bus_id: int,
    service: RepairManager = Depends(RepairManager)
):
    repairs = await service.get_repairs_by_bus(bus_id)
    return [dict(r._mapping) for r in repairs]


# =========================
# UPDATE REPAIR
# =========================
@router.put("/{repair_id}")
async def update_repair(
    repair_id: int,
    repair: RepairSchema,
    service: RepairManager = Depends(RepairManager)
):
    result = await service.update_repair(repair_id, repair)
    return result


# =========================
# DELETE REPAIR
# =========================
@router.delete("/{repair_id}")
async def delete_repair(
    repair_id: int,
    service: RepairManager = Depends(RepairManager)
):
    result = await service.delete_repair(repair_id)
    return result


# =========================
# CHANGE STATUS
# =========================
@router.patch("/{repair_id}/status")
async def change_status(
    repair_id: int,
    status: str,
    service: RepairManager = Depends(RepairManager)
):
    result = await service.change_status(repair_id, status)
    return result
