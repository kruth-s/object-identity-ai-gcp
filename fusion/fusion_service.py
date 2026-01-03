from fusion.schema import BranchOutput
from fusion.tfp_fusion import fuse_branch_outputs

def run_fusion(branches_dict: dict) -> dict:
    """
    branches_dict = your existing JSON branch outputs.
    Expects each branch has 'confidence' and optionally 'p_same_object'.
    If p_same_object missing, use confidence as proxy.
    """
    outputs = []
    for name, payload in branches_dict.items():
        conf = float(payload.get("confidence", 0.5))
        p = float(payload.get("p_same_object", conf))  # if branch doesn't compute p yet
        outputs.append(BranchOutput(name=name, p_same_object=p, confidence=conf))

    result = fuse_branch_outputs(outputs, n_samples=256)

    return {
        "probability_same_object": result.p_final,
        "confidence_score": result.p_final,
        "confidence_interval": result.confidence_interval,
        "branch_weights": result.weights,
        "uncertainty_level": "low" if (result.confidence_interval[1] - result.confidence_interval[0]) < 0.2 else "high",
        "method": result.method,
    }
