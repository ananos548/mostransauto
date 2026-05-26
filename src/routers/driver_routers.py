from fastapi import APIRouter, Depends

from src.services.drivers import DriverManager
from src.schemas.driver_schemas import DriverSchema


router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)


# =========================
# CREATE DRIVER
# =========================
@router.post("/")
async def create_driver(
    driver: DriverSchema,
    service: DriverManager = Depends(DriverManager)
):

    result = await service.create_driver(driver)

    return {
        "message": "Driver created",
        "driver": dict(result._mapping)
    }


# =========================
# GET ALL DRIVERS
# =========================
@router.get("/")
async def get_all_drivers(
    service: DriverManager = Depends(DriverManager)
):

    drivers = await service.get_all_drivers()

    return [dict(driver._mapping) for driver in drivers]


# =========================
# GET DRIVER BY ID
# =========================
@router.get("/{driver_id}")
async def get_driver_by_id(
    driver_id: int,
    service: DriverManager = Depends(DriverManager)
):

    driver = await service.get_driver_by_id(driver_id)

    return dict(driver._mapping)


# =========================
# UPDATE DRIVER
# =========================
@router.put("/{driver_id}")
async def update_driver(
    driver_id: int,
    driver: DriverSchema,
    service: DriverManager = Depends(DriverManager)
):

    result = await service.update_driver(driver_id, driver)

    return result


# =========================
# DELETE DRIVER
# =========================
@router.delete("/{driver_id}")
async def delete_driver(
    driver_id: int,
    service: DriverManager = Depends(DriverManager)
):

    result = await service.delete_driver(driver_id)

    return result
