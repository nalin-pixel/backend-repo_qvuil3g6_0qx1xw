from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from schemas import LeadIn, LeadOut
from database import create_document, get_documents, get_db

app = FastAPI(title="COVA Digital API", version="1.0.0")

# Allow all origins during development; in production restrict to your domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"]) 
async def root():
    return {"status": "ok", "service": "COVA Digital API"}


@app.get("/test", tags=["health"]) 
async def test_db():
    try:
        db = get_db()
        # run a lightweight command
        await db.command("ping")
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/leads", response_model=LeadOut, tags=["leads"]) 
async def create_lead(lead: LeadIn):
    try:
        saved = await create_document("lead", lead.model_dump())
        return LeadOut(**saved)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save lead: {e}")


@app.get("/leads", response_model=List[LeadOut], tags=["leads"]) 
async def list_leads(limit: int = 50):
    try:
        items = await get_documents("lead", limit=limit)
        return [LeadOut(**it) for it in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch leads: {e}")
