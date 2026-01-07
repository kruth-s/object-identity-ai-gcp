from typing import List
from enum import Enum
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from google.cloud import firestore
from utils.upload import upload_file_to_gcs

# ---------- FIRESTORE ----------
db = firestore.Client()

router = APIRouter(prefix="/items", tags=["Items"])

class ItemStatus(str, Enum):
    LOST = "Lost"
    FOUND = "Found"

@router.post("/upload", status_code=201)
async def create_item(
    name: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    date_time: str = Form(...),
    status: ItemStatus = Form(...),
    street_area: str = Form(...),
    pin_code: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    images: List[UploadFile] = File(...),  # multiple files
):
    try:
        # 1️⃣ Upload files to GCS
        image_uris = []
        for file in images:
            gcs_uri = await upload_file_to_gcs(file)
            image_uris.append(gcs_uri)

        # 2️⃣ Prepare data for Firestore
        data = {
            "name": name,
            "category": category,
            "description": description,
            "date_time": date_time,
            "status": status.value,
            "location": {
                "street_area": street_area,
                "pin_code": pin_code,
                "city": city,
                "state": state,
            },
            "contact": {
                "phone": phone,
                "email": email,
            },
            "images": image_uris,
        }

        doc_ref = db.collection("items").add(data)

        return {"message": "Item created successfully", "id": doc_ref[1].id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))