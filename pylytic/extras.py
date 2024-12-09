import functools


def validate_type(func):
    """
    A decorator that validates the types of arguments passed to a function based on its type annotations

    :param func: The function whose arguments needs type validation.
    :return: The decorated function with type validation.
    :raises: `TypeError` if any argument does not match the expected type required by the function.
    """
    func_types = func.__annotations__

    @functools.wraps(func)
    def check_type(*args, **kwargs):
        if args:
            for argument, parameter, required_type in zip(args, func_types.keys(), func_types.values()):
                if not isinstance(argument, required_type):
                    raise TypeError(f"Error: {parameter} must be of type {required_type}")

        elif kwargs:
            for argument, parameter, required_type in zip(kwargs.values(), func_types.keys(), func_types.values()):
                if not isinstance(argument, required_type):
                    raise TypeError(f"Error: {parameter} must be of type {required_type}")

        return func(*args, **kwargs)

    return check_type
