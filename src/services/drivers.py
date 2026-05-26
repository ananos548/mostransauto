from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from src.database import get_async_session


class DriverManager:

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    # =========================
    # CREATE DRIVER
    # =========================
    async def create_driver(self, driver_data):

        query = text("""
            INSERT INTO drivers (full_name, phone, category, experience)
            VALUES (:full_name, :phone, :category, :experience)
            RETURNING id, full_name, phone, category, experience
        """)

        result = await self.session.execute(query, {
            "full_name": driver_data.full_name,
            "phone": driver_data.phone,
            "category": driver_data.category,
            "experience": driver_data.experience
        })

        await self.session.commit()
        return result.fetchone()

    # =========================
    # GET DRIVER BY ID
    # =========================
    async def get_driver_by_id(self, driver_id: int):

        query = text("""
            SELECT * FROM drivers
            WHERE id = :driver_id
        """)

        result = await self.session.execute(query, {
            "driver_id": driver_id
        })

        driver = result.fetchone()

        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )

        return driver

    # =========================
    # GET ALL DRIVERS
    # =========================
    async def get_all_drivers(self):

        query = text("""
            SELECT * FROM drivers
            ORDER BY id DESC
        """)

        result = await self.session.execute(query)

        return result.fetchall()

    # =========================
    # UPDATE DRIVER
    # =========================
    async def update_driver(self, driver_id: int, driver_data):

        query = text("""
            UPDATE drivers
            SET full_name = :full_name,
                phone = :phone,
                category = :category,
                experience = :experience
            WHERE id = :driver_id
            RETURNING id
        """)

        result = await self.session.execute(query, {
            "driver_id": driver_id,
            "full_name": driver_data.full_name,
            "phone": driver_data.phone,
            "category": driver_data.category,
            "experience": driver_data.experience
        })

        await self.session.commit()

        updated = result.fetchone()

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )

        return {
            "message": "Driver updated successfully"
        }

    # =========================
    # DELETE DRIVER
    # =========================
    async def delete_driver(self, driver_id: int):

        query = text("""
            DELETE FROM drivers
            WHERE id = :driver_id
            RETURNING id
        """)

        result = await self.session.execute(query, {
            "driver_id": driver_id
        })

        deleted = result.fetchone()

        await self.session.commit()

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )

        return {
            "message": "Driver deleted successfully"
        }
