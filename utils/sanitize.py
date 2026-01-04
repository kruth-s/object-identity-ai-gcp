def sanitize_for_logs(obj):
    if isinstance(obj, dict):
        clean = {}
        for k, v in obj.items():
            if isinstance(v, list) and len(v) > 50:
                clean[k] = f"<vector len={len(v)}>"
            elif isinstance(v, dict):
                clean[k] = sanitize_for_logs(v)
            else:
                clean[k] = v
        return clean
    if isinstance(obj, list):
        return f"<list len={len(obj)}>"
    return obj
