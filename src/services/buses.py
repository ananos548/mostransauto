from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from src.database import get_async_session


class BusManager:

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    # =========================
    # CREATE BUS
    # =========================
    async def create_bus(self, bus_data):

        query = text("""
            INSERT INTO buses (number, model, brand, year, mileage, status, vin, depot_id)
            VALUES (:number, :model, :brand, :year, :mileage, :status, :vin, :depot_id)
            RETURNING id, number, model, brand, year, mileage, status, vin, depot_id
        """)

        result = await self.session.execute(query, {
            "number": bus_data.number,
            "model": bus_data.model,
            "brand": bus_data.brand,
            "year": bus_data.year,
            "mileage": bus_data.mileage,
            "status": bus_data.status,
            "vin": bus_data.vin,
            "depot_id": bus_data.depot_id
        })

        await self.session.commit()
        return result.fetchone()

    # =========================
    # GET BY ID
    # =========================
    async def get_bus_by_id(self, bus_id: int):

        query = text("""
            SELECT * FROM buses
            WHERE id = :bus_id
        """)

        result = await self.session.execute(query, {"bus_id": bus_id})
        bus = result.fetchone()

        if not bus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bus not found"
            )

        return bus

    # =========================
    # GET ALL
    # =========================
    async def get_all_buses(self):

        query = text("""
            SELECT * FROM buses
            ORDER BY id DESC
        """)

        result = await self.session.execute(query)
        return result.fetchall()

    # =========================
    # UPDATE BUS
    # =========================
    async def update_bus(self, bus_id: int, bus_data):

        query = text("""
            UPDATE buses
            SET number = :number,
                model = :model,
                brand = :brand,
                year = :year,
                mileage = :mileage,
                status = :status,
                vin = :vin,
                depot_id = :depot_id
            WHERE id = :bus_id
            RETURNING id
        """)

        result = await self.session.execute(query, {
            "bus_id": bus_id,
            "number": bus_data.number,
            "model": bus_data.model,
            "brand": bus_data.brand,
            "year": bus_data.year,
            "mileage": bus_data.mileage,
            "status": bus_data.status,
            "vin": bus_data.vin,
            "depot_id": bus_data.depot_id
        })

        await self.session.commit()

        updated = result.fetchone()

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bus not found"
            )

        return {"message": "Bus updated successfully"}

    # =========================
    # DELETE BUS
    # =========================
    async def delete_bus(self, bus_id: int):

        query = text("""
            DELETE FROM buses
            WHERE id = :bus_id
            RETURNING id
        """)

        result = await self.session.execute(query, {"bus_id": bus_id})
        deleted = result.fetchone()

        await self.session.commit()

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bus not found"
            )

        return {"message": "Bus deleted successfully"}

    # =========================
    # SEARCH BUS
    # =========================
    async def search_buses(self, query_str: str):

        query = text("""
            SELECT * FROM buses
            WHERE number ILIKE :q
               OR model ILIKE :q
               OR brand ILIKE :q
               OR vin ILIKE :q
        """)

        result = await self.session.execute(query, {
            "q": f"%{query_str}%"
        })

        return result.fetchall()

    # =========================
    # CHANGE STATUS
    # =========================
    async def change_status(self, bus_id: int, status_value: str):

        query = text("""
            UPDATE buses
            SET status = :status
            WHERE id = :bus_id
            RETURNING id, status
        """)

        result = await self.session.execute(query, {
            "bus_id": bus_id,
            "status": status_value
        })

        await self.session.commit()

        updated = result.fetchone()

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bus not found"
            )

        return {
            "id": updated.id,
            "status": updated.status
        }
