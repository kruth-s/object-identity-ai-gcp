from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

@dataclass
class BranchOutput:
    name: str
    p_same_object: float         
    confidence: float             
    saliency_map_uri: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

@dataclass
class FusionResult:
    p_final: float
    confidence_interval: list     # [low, high]
    weights: Dict[str, float]     # dynamic weights
    method: str                   # "tfp_beta_bma"

class ItemStatus(Enum):
    LOST = "Lost"
    FOUND = "Found"

@dataclass
class Location:
    street_area: str
    pin_code: str
    city: str
    state: str
    country: str = "India"


@dataclass
class ContactInfo:
    phone: str
    email: str


@dataclass
class Item:
    name: str
    category: str
    description: str
    date_time: datetime
    status: ItemStatus
    location: Location
    contact: ContactInfo
    images: Optional[List[str]] = None  # URLs (Firebase Storage)