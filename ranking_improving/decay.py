import math
import time

def time_decay_score(ts_now: int, ts_old: int, half_life_hours: float = 72.0) -> float:
    """
    Exponential decay: score halves every half_life_hours.
    """
    dt = max(0, ts_now - ts_old)
    hours = dt / 3600.0
    lam = math.log(2) / max(1e-6, half_life_hours)
    return float(math.exp(-lam * hours))

def location_consistency_score(loc_a: dict | None, loc_b: dict | None) -> float:
    """
    loc = {"city":"Bengaluru","lat":..., "lng":...} optional.
    Simple rules:
    - same city => 0.95
    - unknown => 0.70
    - different city => 0.30
    """
    if not loc_a or not loc_b:
        return 0.70
    if loc_a.get("city") and loc_a.get("city") == loc_b.get("city"):
        return 0.95
    return 0.30
