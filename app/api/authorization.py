

def check_authorization(resolve_function):
    """
    Performs authorization checks for type fields.

    Checks to see if info.context.user.is_authenticated
    is true. If so, the resolve function is called. If
    false, an exception is raised.
    """
    def wrapper(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')
        return resolve_function(self, info, **kwargs)
    return wrapper
