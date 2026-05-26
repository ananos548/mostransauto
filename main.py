from fastapi import FastAPI

from src.database import engine
from src.routers.auth_routers import router as auth_router
from src.routers.bus_routers import router as bus_router
from src.routers.repair_routers import router as repair_router 
from src.routers.driver_routers import router as driver_router
from src.routers.bus_router_routers import router as route_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(bus_router)
app.include_router(repair_router)
app.include_router(driver_router)
app.include_router(route_router)
