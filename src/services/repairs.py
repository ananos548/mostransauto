from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from src.database import get_async_session


class RepairManager:

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    # =========================
    # CREATE REPAIR
    # =========================
    async def create_repair(self, repair_data):

        query = text("""
            INSERT INTO repairs (bus_id, description, cost, status)
            VALUES (:bus_id, :description, :cost, :status)
            RETURNING id, bus_id, description, cost, status, created_at
        """)

        result = await self.session.execute(query, {
            "bus_id": repair_data.bus_id,
            "description": repair_data.description,
            "cost": repair_data.cost,
            "status": repair_data.status
        })

        await self.session.commit()
        return result.fetchone()

    # =========================
    # GET BY ID
    # =========================
    async def get_repair_by_id(self, repair_id: int):

        query = text("""
            SELECT * FROM repairs
            WHERE id = :repair_id
        """)

        result = await self.session.execute(query, {"repair_id": repair_id})
        repair = result.fetchone()

        if not repair:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Repair not found"
            )

        return repair

    # =========================
    # GET ALL
    # =========================
    async def get_repairs(self):

        query = text("""
            SELECT * FROM repairs
            ORDER BY id DESC
        """)

        result = await self.session.execute(query)
        return result.fetchall()

    # =========================
    # GET BY BUS
    # =========================
    async def get_repairs_by_bus(self, bus_id: int):

        query = text("""
            SELECT * FROM repairs
            WHERE bus_id = :bus_id
            ORDER BY created_at DESC
        """)

        result = await self.session.execute(query, {"bus_id": bus_id})
        return result.fetchall()

    # =========================
    # UPDATE REPAIR
    # =========================
    async def update_repair(self, repair_id: int, repair_data):

        query = text("""
            UPDATE repairs
            SET bus_id = :bus_id,
                description = :description,
                cost = :cost,
                status = :status
            WHERE id = :repair_id
            RETURNING id
        """)

        result = await self.session.execute(query, {
            "repair_id": repair_id,
            "bus_id": repair_data.bus_id,
            "description": repair_data.description,
            "cost": repair_data.cost,
            "status": repair_data.status
        })

        await self.session.commit()

        updated = result.fetchone()

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Repair not found"
            )

        return {"message": "Repair updated successfully"}

    # =========================
    # DELETE REPAIR
    # =========================
    async def delete_repair(self, repair_id: int):

        query = text("""
            DELETE FROM repairs
            WHERE id = :repair_id
            RETURNING id
        """)

        result = await self.session.execute(query, {"repair_id": repair_id})
        deleted = result.fetchone()

        await self.session.commit()

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Repair not found"
            )

        return {"message": "Repair deleted successfully"}

    # =========================
    # CHANGE STATUS
    # =========================
    async def change_status(self, repair_id: int, status_value: str):

        query = text("""
            UPDATE repairs
            SET status = :status
            WHERE id = :repair_id
            RETURNING id, status
        """)

        result = await self.session.execute(query, {
            "repair_id": repair_id,
            "status": status_value
        })

        await self.session.commit()

        updated = result.fetchone()

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Repair not found"
            )

        return {
            "id": updated.id,
            "status": updated.status
        }
