import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import LeadIn, LeadOut

app = FastAPI(title="COVA Digital API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "COVA Digital Backend running"}

@app.get("/test")
def test_database():
    status = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "collections": []
    }
    try:
        if db is not None:
            status["database"] = "✅ Connected"
            status["collections"] = db.list_collection_names()[:10]
        else:
            status["database"] = "❌ db not initialized"
    except Exception as e:
        status["database"] = f"⚠️ {str(e)[:80]}"
    return status

@app.post("/leads", response_model=LeadOut)
def create_lead(lead: LeadIn):
    try:
        inserted_id = create_document("lead", lead)
        doc = db["lead"].find_one({"_id": ObjectId(inserted_id)})
        # Normalize for response
        doc_out = {
            "id": str(doc.get("_id")),
            "name": doc.get("name"),
            "message": doc.get("message"),
            "email": doc.get("email"),
            "phone": doc.get("phone"),
            "business_name": doc.get("business_name"),
            "website": doc.get("website"),
            "need_help_with": doc.get("need_help_with"),
            "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None,
            "updated_at": doc.get("updated_at").isoformat() if doc.get("updated_at") else None,
        }
        return doc_out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/leads", response_model=List[LeadOut])
def list_leads(limit: int = 50):
    try:
        docs = get_documents("lead", limit=limit)
        out = []
        for d in docs:
            out.append({
                "id": str(d.get("_id")),
                "name": d.get("name"),
                "message": d.get("message"),
                "email": d.get("email"),
                "phone": d.get("phone"),
                "business_name": d.get("business_name"),
                "website": d.get("website"),
                "need_help_with": d.get("need_help_with"),
                "created_at": d.get("created_at").isoformat() if d.get("created_at") else None,
                "updated_at": d.get("updated_at").isoformat() if d.get("updated_at") else None,
            })
        return out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
