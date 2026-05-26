# src/services/route_manager.py

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from src.database import get_async_session


class RouteManager:

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    # =========================
    # CREATE ROUTE
    # =========================
    async def create_route(self, route_data):

        query = text("""
            INSERT INTO routes (name, start_point, end_point)
            VALUES (:name, :start_point, :end_point)
            RETURNING id, name, start_point, end_point
        """)

        result = await self.session.execute(query, {
            "name": route_data.name,
            "start_point": route_data.start_point,
            "end_point": route_data.end_point
        })

        await self.session.commit()

        return result.fetchone()

    # =========================
    # GET ROUTE BY ID
    # =========================
    async def get_route_by_id(self, route_id: int):

        query = text("""
            SELECT * FROM routes
            WHERE id = :route_id
        """)

        result = await self.session.execute(query, {
            "route_id": route_id
        })

        route = result.fetchone()

        if not route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Route not found"
            )

        return route

    # =========================
    # GET ALL ROUTES
    # =========================
    async def get_all_routes(self):

        query = text("""
            SELECT * FROM routes
            ORDER BY id DESC
        """)

        result = await self.session.execute(query)

        return result.fetchall()

    # =========================
    # UPDATE ROUTE
    # =========================
    async def update_route(self, route_id: int, route_data):

        query = text("""
            UPDATE routes
            SET name = :name,
                start_point = :start_point,
                end_point = :end_point
            WHERE id = :route_id
            RETURNING id
        """)

        result = await self.session.execute(query, {
            "route_id": route_id,
            "name": route_data.name,
            "start_point": route_data.start_point,
            "end_point": route_data.end_point
        })

        await self.session.commit()

        updated = result.fetchone()

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Route not found"
            )

        return {
            "message": "Route updated successfully"
        }

    # =========================
    # DELETE ROUTE
    # =========================
    async def delete_route(self, route_id: int):

        query = text("""
            DELETE FROM routes
            WHERE id = :route_id
            RETURNING id
        """)

        result = await self.session.execute(query, {
            "route_id": route_id
        })

        deleted = result.fetchone()

        await self.session.commit()

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Route not found"
            )

        return {
            "message": "Route deleted successfully"
        }
