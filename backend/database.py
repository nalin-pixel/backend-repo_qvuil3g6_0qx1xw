from __future__ import annotations

import os
from typing import Any, Dict, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app_db")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
    return _client


def get_db() -> AsyncIOMotorDatabase:
    global _db
    if _db is None:
        _db = get_client()[DATABASE_NAME]
    return _db


async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    from datetime import datetime

    db = get_db()
    payload = {**data, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
    result = await db[collection_name].insert_one(payload)
    inserted = await db[collection_name].find_one({"_id": result.inserted_id})
    if inserted is None:
        raise RuntimeError("Failed to fetch inserted document")
    inserted["id"] = str(inserted.pop("_id"))
    return inserted


async def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 100):
    db = get_db()
    cursor = db[collection_name].find(filter_dict or {}).limit(limit).sort("created_at", -1)
    items = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        items.append(doc)
    return items
