from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class BranchOutput:
    name: str
    p_same_object: float          # probability in [0,1]
    confidence: float             # confidence in [0,1]
    saliency_map_uri: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

@dataclass
class FusionResult:
    p_final: float
    confidence_interval: list     # [low, high]
    weights: Dict[str, float]     # dynamic weights
    method: str                   # "tfp_beta_bma"
