

def if_then(if_, then_callback, *then_args, **then_kwargs):
    rv = None
    if if_:
        rv = then_callback(*then_args, **then_kwargs)
    return rv
