import functools

import flask


def requires_request_params(required_params: list[str]):
    """
    Checks for each member of *required_params* to be present in the request body before
    executing the view function.
    """

    def decorator_requires_request_params(func):
        @functools.wraps(func)
        def wrapper_requires_request_params(*args, **kwargs):
            for arg in required_params:
                if arg not in flask.request.json or not flask.request.json.get(arg):
                    return f"Missing {arg}\n"
            return func(*args, **kwargs)

        return wrapper_requires_request_params

    return decorator_requires_request_params
