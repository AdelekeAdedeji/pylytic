
from pylytic.extras import validate_type
from pylytic.storage import _stored_values_ctan_dict, Constants


@validate_type
def rad(value: int | float, conv_from: str = "deg") -> int | float:
    """
    Takes two arguments, value: an integer or a floating point number and conv_from : degree or gradians of type string

    :param value: int | float
    :param conv_from: str
    :return: int | float
    """
    if conv_from.lower() == "grad":
        value *= 0.9
    return (value * Constants.PI.value) / 180


@validate_type
def deg(value: int | float, conv_from: str) -> int | float:
    """
    Takes two arguments, value: an integer or a floating point number and conv_from : radians or gradians of type string

    :param value: int | float
    :param conv_from: str
    :return: int | float
    """
    if conv_from.lower() == "rad":
        return (value * 180) / Constants.PI.value
    elif conv_from.lower() == "grad":
        value *= 0.9
        return value


@validate_type
def grad(value: int | float, conv_from: str = "deg") -> int | float:
    """
    Takes two arguments, value: an integer or a floating point and conv_from: degree or radians of type string

    :param value: int | float
    :param conv_from: str
    :return: int | float
    """
    if conv_from.lower() == "rad":
        value = (value * 180) / Constants.PI.value
    return (value * 10) / 9


# Value correction
def _linear_transformation():
    pass


@validate_type
def range_reduction(x: int | float) -> tuple[int, int | float]:
    """
    Reduces a number to a normalized range between 1 and 10 with an exponent.

    :param x: The number to reduce.
    :return: A tuple containing the exponent and the normalized number.
    """

    k = 0
    while x >= 10:
        x /= 10
        k += 1
    else:
        while x < 1:
            x *= 10
            k -= 1

    return k, x


@validate_type
def _cos_angle_correction(angle: int | float, ) -> tuple[int | float, int]:
    """
    Adjusts the input angle for cosine calculation based on quadrant

    :param angle: Requires an input angle (could be an integer or floating point)
    :return: A tuple containing the adjusted angle and the sign of the cosine value
    """
    x = 1
    if Constants.QUARTER_CIRCLE.value <= angle <= Constants.HALF_CIRCLE.value:
        x = -1
        angle = Constants.HALF_CIRCLE.value - angle
    elif Constants.HALF_CIRCLE.value <= angle <= 270:
        x = -1
        angle = angle - Constants.HALF_CIRCLE.value
    elif 270 <= angle <= Constants.TOTAL_CIRCLE.value:
        angle = Constants.TOTAL_CIRCLE.value - angle
    return angle, x


@validate_type
def _sin_angle_correction(angle: int | float) -> int | float:
    """
    Adjusts the input angle for sine calculation based on quadrant.

    :param angle: Requires an input angle (could be an integer or floating point)
    :return: The adjusted angle
    """
    if Constants.QUARTER_CIRCLE.value <= angle <= Constants.HALF_CIRCLE.value:
        angle = Constants.HALF_CIRCLE.value - angle
    elif Constants.HALF_CIRCLE.value <= angle <= 270:
        angle = -(angle - Constants.HALF_CIRCLE.value)
    elif 270 <= angle <= Constants.TOTAL_CIRCLE.value:
        angle = -(Constants.TOTAL_CIRCLE.value - angle)
    return angle


# Algorithms/Mathematical methods: Employing Coordinate rotational digital Algorithm and Newton-Raphson method
@validate_type
def CORDIC(angle: int | float, func: str, mode: str = "deg", factor: int = 1, x: int = Constants.X_.value,
           y: int = Constants.Y_.value, ) -> tuple:
    """
    Performs rotations to achieve the desired angle through binary search, strength reduction and more

    :param angle: angle required could be int or float
    :param func: function required to be evaluated should be str
    :param mode: selects the mode in which the operation is carried out
    :param factor: int
    :param x: initial starting coordinate x, defaults to 1
    :param y: initial starting coordinate y, defaults to 0
    :return: tuple containing final coordinates xn and yn reduced by the scaling factor
    """

    angle = deg(angle, "grad") if mode == "grad" \
        else deg(angle, "rad") if mode == "rad" else angle

    angle = (angle + Constants.TOTAL_CIRCLE.value) % Constants.TOTAL_CIRCLE.value if angle < 0 else (
            angle % Constants.TOTAL_CIRCLE.value)

    sin_angle = _sin_angle_correction(angle)
    cos_angle = _cos_angle_correction(angle)

    angle = sin_angle if func.lower() == "sin" or func.lower() == "sinh" else cos_angle[0]

    if int(factor) == 1:
        for key, value in _stored_values_ctan_dict.items():
            sigma = 1 if angle >= 0 else -1
            xn = x - (sigma * key * y)
            yn = y + (sigma * key * x)
            angle -= (sigma * value)
            x, y = xn, yn

        return Constants.C_SCALING_FACTOR.value * x * cos_angle[1], Constants.C_SCALING_FACTOR.value * y


@validate_type
def INV_CORDIC(b: int | float, func: str, mode: str = "deg") -> int | float:
    """
    Function to evaluate the inverse of trigonometric functions

    :param b: required value b, could be int or float
    :param func: required function of type str
    :param mode: selects mode of operation (str)
    :return: An integer or floating point value
    """

    r_angle, x, y = 0.0, Constants.C_SCALING_FACTOR.value, 0.0
    if func.lower() == "asin":
        if -1 < b < 1:
            for key, value in _stored_values_ctan_dict.items():
                sigma = 1 if y < b else -1
                xn = x - (sigma * key * y)
                yn = y + (sigma * key * x)
                r_angle += (sigma * value)
                x, y = xn, yn

        elif b == 1:
            r_angle = Constants.QUARTER_CIRCLE.value

        elif b == -1:
            r_angle = -Constants.QUARTER_CIRCLE.value

        else:
            raise ValueError("m_eval domain error\n"
                             "Inverse trigonometric functions (except arctan and arccot)"
                             " can only accept values ranging from -1 to 1"
                             )

    elif func.lower() == "atan":
        r_angle, x, y = 0.0, 1, -b
        for key, value in _stored_values_ctan_dict.items():
            sigma = 1 if y < 0 else -1
            xn = x - (sigma * key * y)
            yn = y + (sigma * key * x)
            r_angle += (sigma * value)
            x, y = xn, yn

    else:
        raise TypeError(
            "INV_CORDIC (func parameter) only accepts two inputs asin or atan"
        )

    r_angle = grad(r_angle, "deg") if mode.lower() == "grad" else (
        rad(r_angle, "deg")) if mode.lower() == "rad" else (
        r_angle)

    return r_angle


@validate_type
def _newton_raphson_model(y: int | float) -> int | float:
    """
    Implements Newton-Raphson method, handles range reduction to ensure accurate computation,
    for this case, it will be used to evaluate natural logarithm

    :param y: The input value for which the natural logarithm is to be calculated.
              Must be a positive integer or float.

    :return: The calculated natural logarithm (ln) of the input value as an integer or float.
    :raises ValueError: If the input value is less than or equal to zero.
    """

    y = range_reduction(y)
    z, zn = 0, 1
    tolerance = 10 ** -5

    while abs(zn-z) > tolerance:
        z = zn
        zn = z - 1 + (y[1] / Constants.e.value ** z)

    return y[0] * Constants.ln10.value + zn


def gaussian_quadrature():
    pass


# Trigonometric functions
@validate_type
def sin(angle: int | float, mode: str = "deg") -> int | float:
    """
     Evaluates sine of angle
    :param angle: Required angle could be int or float
    :param mode: mode required for operation, should be str
    :return:
    """
    return CORDIC(angle, "sin", mode, 1)[1]


@validate_type
def cos(angle: int | float, mode: str = "deg") -> int | float:
    """
    Evaluates cosine of angle
   :param angle: Required angle could be int or float
   :param mode: mode required for operation
   :return:
    """
    return CORDIC(angle, "cos", mode, 1)[0]


@validate_type
def tan(angle: int | float, mode: str = "deg") -> int | float:
    """
    Evaluates the tangent of an angle.

    :param angle: The required angle.
    :param mode: The mode required for operation, defaults to "deg".
    :return: Tangent of the given angle.
    """
    return sin(angle, mode) / cos(angle, mode)


@validate_type
def cot(angle: int | float, mode: str = "deg") -> int | float:
    """
     Evaluates the cotangent of an angle.
.
    :param angle: The required angle.
    :param mode: The mode required for operation, defaults to "deg".
    :return: Cotangent value of the given angle.
    """
    return 1 / tan(angle, mode)


@validate_type
def cosec(angle: int | float, mode: str = "deg") -> int | float:
    """
    Evaluates the cosecant of an angle.

    :param angle: The required angle.
    :param mode: The mode required for operation, defaults to "deg".
    :return: Cosecant value of the given angle.
    """
    return 1 / sin(angle, mode)


@validate_type
def sec(angle: int | float, mode: str = "deg") -> int | float:
    """
    Evaluates the secant of an angle.

    :param angle: The required angle.
    :param mode: The mode required for operation, defaults to "deg".
    :return: Secant value of the given angle.
    """
    return 1 / cos(angle, mode)


@validate_type
def asin(y: int | float, mode: str = "deg") -> int | float:
    """
    Evaluates the arc sine of a value.

    :param y: The input value.
    :param mode: The mode for the angle, default is "deg".
    :return: The arc sine value.
    """
    return INV_CORDIC(y, "ASIN", mode)


@validate_type
def acos(x: int | float, mode: str = "deg") -> int | float:
    """
    Evaluates the arc cosine of a value.

    :param x: The input value.
    :param mode: The mode for the angle, default is "deg".
    :return: The arc cosine value.
    """
    quarter_circle = Constants.QUARTER_CIRCLE.value
    return rad(quarter_circle) - asin(x, mode) if mode == "rad" else (
            grad(quarter_circle) - asin(x, mode)) if mode == "grad" else quarter_circle - asin(x, mode)


@validate_type
def atan(a: int | float, mode: str = "deg") -> int | float:
    """
    Evaluates the arc tangent of a value.

    :param a: The input value.
    :param mode: The mode for the angle, default is "deg".
    :return: The arc tangent value.
    """
    return INV_CORDIC(a, "atan", mode)


@validate_type
def acosec(a: int | float, mode: str = "deg") -> int | float:
    """
    Evaluates the arc cosecant of a value.

    :param a: The input value.
    :param mode: The mode for the angle, default is "deg".
    :return: The arc cosecant value.
    :raises: ValueError if input is not ≥ 1 or ≤ -1.
    """

    if a <= -1 or a >= 1:
        return asin(1 / a, mode)
    raise ValueError("Input of acosec must be either be (less than or equal to -1) or (greater than or equal to 1) ")


@validate_type
def asec(a: int | float, mode: str = "deg") -> int | float:
    """
    Evaluates the arc secant of a value.

    :param a: The input value.
    :param mode: The mode for the angle, default is "deg".
    :return: The arc secant value.
    """
    return acos(1 / a, mode)


@validate_type
def acot(a: int | float, mode: str = "deg") -> int | float:
    """
    Evaluates the arc cotangent of a value.

    :param a: The input value.
    :param mode: The mode for the angle, default is "deg".
    :return: The arc cotangent value.
    """
    return atan(1 / a, mode)


# hyperbolic functions
@validate_type
def sinh(angle: int | float) -> int | float:
    """
    Evaluates the hyperbolic sine of an angle.

    :param angle: The angle value.
    :return: Hyperbolic sine value.
    """
    return (Constants.e.value ** angle - Constants.e.value ** -angle) / 2


@validate_type
def cosh(angle: int | float) -> int | float:
    """
    Evaluates the hyperbolic cosine of an angle.

    :param angle: The angle value.
    :return: Hyperbolic cosine value.
    """
    return (Constants.e.value ** angle + Constants.e.value ** -angle) / 2


@validate_type
def tanh(angle: int | float) -> int | float:
    """
    Evaluates the hyperbolic tangent of an angle.

    :param angle: The angle value.
    :return: Hyperbolic tangent value.
    """
    return sinh(angle) / cosh(angle)


@validate_type
def sech(angle: int | float) -> int | float:
    """
    Evaluates the hyperbolic secant of an angle.

    :param angle: The angle value.
    :return: Hyperbolic secant value.
    """
    return 1 / cosh(angle)


@validate_type
def cosech(angle: int | float) -> int | float:
    """
    Evaluates the hyperbolic cosecant of an angle.

    :param angle: The angle value.
    :return: Hyperbolic cosecant value.
    :raises: ValueError if angle is 0.
    """
    if angle != 0:
        return 1 / sinh(angle)
    raise ValueError("angle must not be equal to zero")


@validate_type
def coth(angle: int | float) -> int | float:
    """
    Evaluates the hyperbolic cotangent of an angle.

    :param angle: The angle value.
    :return: Hyperbolic cotangent value.
    :raises: ValueError if angle is 0.
    """
    if angle != 0:
        return 1 / tanh(angle)
    raise ValueError("angle must not be equal to zero")


@validate_type
def asinh(y: int | float) -> int | float:
    """
    Evaluates the arc hyperbolic sine of a value.

    :param y: The input value
    :return: The arc hyperbolic sine value
    """
    return ln(y + (y ** 2 + 1) ** 0.5)


@validate_type
def acosh(x: int | float) -> int | float:
    """
    Evaluates the arc hyperbolic cosine of a value.

    :param x: The input value.
    :return: The arc hyperbolic cosine value.
    :raises: ValueError if input is less than 1
    """
    if x < 1:
        raise ValueError("Values must not be less than 1")
    return ln(x + (x ** 2 - 1) ** 0.5)


@validate_type
def atanh(z: int | float) -> int | float:
    """
    Evaluates the arc hyperbolic tangent of a value.

    :param z: The input value.
    :return: The arc hyperbolic tangent value.'
    :raises: ValueError if input is (less than or equal to -1) or (greater than or equal to 1)
    """
    if z >= 1 or z <= -1:
        raise ValueError(
            "Value must be within the range -1 and 1 with -1 and 1 not included"
        )
    return 0.5 * ln((1 + z) / (1 - z))


@validate_type
def asech(x: int | float) -> int | float:
    """
    Evaluates the arc hyperbolic secant of a value.

    :param x: The input value.
    :return: The arc hyperbolic secant value.
    :raises: ValueError if input is (less than or equal to zero) or (greater than 1)
    """
    if 0 < x <= 1:
        return ln((1 / x) + ((1 / x ** 2) - 1) ** 0.5)
    raise ValueError(
        "Value must be must range from 0 to 1 excluding 0 and including 1"
    )


@validate_type
def acosech(y: int | float) -> int | float:
    """
    Evaluates the arc hyperbolic co-sectant of the input y
    raises an error if y equals zero
    :param y: required input could be an integer or floating point
    :return: an integer or a floating point value.
    """
    print(type(y))
    if y == 0:
        raise ValueError("Value must not be equal to 0")
    return ln((1 / y) + ((1 / y ** 2) + 1) ** 0.5)


@validate_type
def acoth(z: int | float) -> int | float:
    """
    Evaluates the arc hyperbolic cotangent of a value.

    :param z: The input value.
    :return: The arc hyperbolic cotangent value.
    :raises: ValueError if input is within [-1, 1].
    """
    if -1 <= z <= 1:
        raise ValueError(
            "Value must not be within the range -1 and 1 including -1 and 1"
        )
    return 0.5 * ln((z + 1) / (z - 1))


# logarithmic functions
@validate_type
def log10(x: int | float) -> int | float:
    """
    Evaluates the base-10 logarithm of a value.

    :param x: The input value.
    :return: Logarithm base 10 value.
    :raises: ValueError if input ≤ 0.
    """
    if x > 0:
        return ln(x) / Constants.ln10.value
    raise ValueError("Values of x must be greater than 0")


@validate_type
def log(x: int | float, base: int | float = 10) -> int | float:
    """
    Evaluates the logarithm of a value to a specified base.

    :param x: The input value.
    :param base: The base for the logarithm, default is 10.
    :return: Logarithm value
    :raises: ValueError if input ≤ 0.
    """
    if x > 0:
        return ln(x) / ln(base)
    raise ValueError("values of x must be greater than 0")


@validate_type
def ln(value: int | float) -> int | float:
    """
    Evaluates the natural logarithm (base e) of a given positive value.

    :param value: int | float. The number for which the natural logarithm is to be calculated. Must be greater than 0.
    :return: int | float. The natural logarithm of the input value.
    :raises ValueError: If the input value is less than or equal to 0.
    """

    if value <= 0:
        raise ValueError("Value must be greater than 0")
    return _newton_raphson_model(value)


# exponential functions
@validate_type
def power(value: int | float, val_power: int | float) -> int | float:
    """
    Evaluates the result of raising a number to a given power.

    :param value:
    :param val_power:
    :return:
    """
    return value ** val_power


@validate_type
def factorial(value: int) -> int:
    """
    Evaluates the factorial of a non-negative integer.

    :param value: int - The number for which the factorial is to be calculated. Must be between 0 and 1000.
    :return: int - The factorial of the input value.
    :raises ValueError:
        if the input is not an integer,
        if the input is negative,
        if the input exceeds 1000.
    """
    if isinstance(value, int):
        if 0 < value <= 1000:
            n_val = value - 1
            while n_val > 0:
                value *= n_val
                n_val -= 1
            return value

        elif value > 1000:
            raise ValueError("Value cannot exceed 1000")

        elif value == 0:
            return 1

        raise ValueError("Value must be greater than or equal to zero")

    raise ValueError("Value must be an integer, not a floating point or any other data type")


def gamma(value: int | float) -> int | float:
    pass


@validate_type
def perm(n: int, r: int) -> int:
    """
    Evaluates the number of permutations of n items taken r at a time.

    :param n: int - The total number of items.
    :param r: int - The number of items to select.
    :return: int - The number of permutations.
    :raises ValueError: If n or r are not integers
    """
    return int(factorial(n) / factorial(n-r))


@validate_type
def comb(n: int, r: int) -> int:
    """
    Evaluates the number of combinations of n items taken r at a time.

    :param n: int - The total number of items.
    :param r: int - The number of items to select.
    :return: int - The number of combinations.
    :raises ValueError: - If n or r are not integers.
    """
    return int(factorial(n) / (factorial(r) * factorial(n-r)))


# other functions
@validate_type
def abs(x: int | float) -> int | float:
    """
    Evaluates the absolute value of a number.

    :param x: int | float - The number for which the absolute value is to be calculated.
    :return: int | float - The absolute value of the input.
    """
    return -x if x < 0 else x
