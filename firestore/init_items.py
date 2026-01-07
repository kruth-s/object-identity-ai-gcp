from datetime import datetime
from enum import Enum
from typing import List, Optional

from google.cloud import firestore


# ---------- ENUM ----------
class ItemStatus(Enum):
    LOST = "Lost"
    FOUND = "Found"


# ---------- DATA MODELS ----------
class Location(dict):
    def __init__(self, street_area, pin_code, city, state, country="India"):
        super().__init__(
            street_area=street_area,
            pin_code=pin_code,
            city=city,
            state=state,
            country=country,
        )


class ContactInfo(dict):
    def __init__(self, phone, email):
        super().__init__(phone=phone, email=email)


class Item(dict):
    def __init__(
        self,
        name: str,
        category: str,
        description: str,
        date_time: datetime,
        status: ItemStatus,
        location: Location,
        contact: ContactInfo,
        images: Optional[List[str]] = None,
    ):
        super().__init__(
            name=name,
            category=category,
            description=description,
            date_time=date_time,
            status=status.value,
            location=location,
            contact=contact,
            images=images or [],
        )


# ---------- FIRESTORE CLIENT ----------
db = firestore.Client()  # Uses GCP credentials automatically


def create_items_collection():
    item = Item(
        name="Black Wallet",
        category="Accessories",
        description="Lost near metro station",
        date_time=datetime.utcnow(),
        status=ItemStatus.LOST,
        location=Location(
            street_area="MG Road",
            pin_code="560001",
            city="Bengaluru",
            state="Karnataka",
        ),
        contact=ContactInfo(
            phone="+91XXXXXXXXXX",
            email="user@example.com",
        ),
        images=[],
    )

    doc_ref = db.collection("items").add(item)

    print("✅ Firestore collection 'items' created")
    print("📄 Document ID:", doc_ref[1].id)


if __name__ == "__main__":
    create_items_collection()
