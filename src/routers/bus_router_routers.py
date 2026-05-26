from fastapi import APIRouter, Depends

from src.services.bus_routes import RouteManager
from src.schemas.route_schemas import RouteSchema



router = APIRouter(
    prefix="/routes",
    tags=["Routes"]
)


# =========================
# CREATE ROUTE
# =========================
@router.post("/")
async def create_route(
    route: RouteSchema,
    service: RouteManager = Depends(RouteManager)
):

    result = await service.create_route(route)

    return {
        "message": "Route created",
        "route": dict(result._mapping)
    }


# =========================
# GET ALL ROUTES
# =========================
@router.get("/")
async def get_all_routes(
    service: RouteManager = Depends(RouteManager)
):

    routes = await service.get_all_routes()

    return [dict(route._mapping) for route in routes]


# =========================
# GET ROUTE BY ID
# =========================
@router.get("/{route_id}")
async def get_route_by_id(
    route_id: int,
    service: RouteManager = Depends(RouteManager)
):

    route = await service.get_route_by_id(route_id)

    return dict(route._mapping)


# =========================
# UPDATE ROUTE
# =========================
@router.put("/{route_id}")
async def update_route(
    route_id: int,
    route: RouteSchema,
    service: RouteManager = Depends(RouteManager)
):

    result = await service.update_route(route_id, route)

    return result


# =========================
# DELETE ROUTE
# =========================
@router.delete("/{route_id}")
async def delete_route(
    route_id: int,
    service: RouteManager = Depends(RouteManager)
):

    result = await service.delete_route(route_id)

    return result
