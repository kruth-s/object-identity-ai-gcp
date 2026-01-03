import numpy as np

def build_void_graph(voids: list, max_edges_per_node: int = 3) -> dict:
    """
    Returns a lightweight graph:
    nodes: {id, area, centroid}
    edges: {src, dst, dist}
    """
    nodes = []
    for i, v in enumerate(voids):
        nodes.append({
            "id": i,
            "area": v["area"],
            "centroid": v["centroid"]
        })

    if len(nodes) < 2:
        return {"nodes": nodes, "edges": []}

    c = np.array([n["centroid"] for n in nodes], dtype=np.float32)
    edges = []
    for i in range(len(nodes)):
        d = np.sqrt(np.sum((c - c[i]) ** 2, axis=1))
        nn = np.argsort(d)[1: max_edges_per_node + 1]
        for j in nn:
            edges.append({
                "src": int(i),
                "dst": int(j),
                "dist": float(d[j])
            })

    return {"nodes": nodes, "edges": edges}
