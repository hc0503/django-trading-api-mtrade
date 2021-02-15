def asdict(o, skip_empty=False):
    return {
        k: v
        for k, v in o.__dict__.items()
        if not (skip_empty and v is None)
    }
