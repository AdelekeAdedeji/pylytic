# pylytic Library
## Description
pylytic is a lightweight and flexible Python library designed to facilitate evaluating mathematical expressions and 
performing calculations efficiently, the pylytic library is focused on the implementation of math methods and evaluation 
of complex arithemetic expressions. It leverages mathematical algorithms such as CORDIC, INV_CORDIC and Newton-Raphson 
methods to perform computations. This library is ideal for developers, researchers, and enthusiasts seeking optimized 
solutions for mathematical operations.

[![PyPI version](https://badge.fury.io/py/pylytic.svg)](https://pypi.org/project/pylytic/)
[![Downloads](https://pepy.tech/badge/pylytic)](https://pepy.tech/project/pylytic)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

### Library Structure
- pylytic

  - evaluation
    - eval.py

  - math_methods 
    - m_eval.py
  
  - storage.py

  - extras.py
    
`eval.py` Evaluates mathematical expressions

`m_eval.py` Contains mathematical functions

`storage.py` Stores Constants required for eval and m_eval

`extras.py` Includes decorator used to validate types passed as arguments to functions

## Installation
To install `pylytic`, simply use pip:
```bash
pip install pylytic
```

Or install directly from this repository
```bash
pip install git+https://github.com/AdelekeAdedeji/pylytic.git
```

## eval.py
`eval`  is a module in the pylytic library used to evaluate mathematical expressions. 

## Feature
- Mathematical expression evaluation: Accurate evaluation of mathematical expressions

## Usage 
Here is a quick example to get started:

```python
from pylytic import eval

expr_result = eval.eval_complex(expr="1.725 * cosech(log(0.784 + atan(0.459)) + 4P(2)C(7) / 3!) + cot(40) * asec(9.5 * 7 - 5) - -(sinh(1.5) + 2 ^ ln(0.75))",
                         mode="deg", logarithmic_base=10)
print(expr_result)
```
`expr:` represents the expression to be evaluated, expression is strictly of type str

`mode:` represents the mode in which the expression to be evaluated, defaults to deg (as in degrees), also supports 
rad (radians) and grad (gradians)

`logarithmic_base:` the base in which the expression is to be evaluated, defaults to base 10


## m_eval.py
`m_eval` is a module in the pylytic library which contains mathematical functions

## Features
- Trigonometric Evaluations: Efficient computation of sine, cosine, tangent, and their inverses using the CORDIC algorithm.
- Square Root Calculation: High-precision square root evaluation leveraging the Newton-Raphson method.
- Robust Error Handling: Gracefully handles invalid inputs and computational errors.

## Usage
Here's a quick example to get started:

### Computing Trigonometric Functions

```python
from pylytic import m_eval

result = m_eval.sin(angle=45, mode="rad")
print("Result: ", result)
```

### Computing Hyperbolic Functions

```python
from pylytic import m_eval

result = m_eval.cosech(1.715)
print("Result:", result)
```

### Computing Logarithmic functions

```python
from pylytic import m_eval

logarithm = m_eval.log(x=0.857, base=2.7182818285)
natural_log = m_eval.ln(value=75.5)
print(logarithm, natural_log)
```

### List of functions supported by m_eval
*sin, cos, tan, sec, cosec, cot, asin, acos, atan, asec, acosec, acot, sinh, cosh, tanh, sech, cosech, coth, asinh, 
acosh, atanh, acosech, asech, acoth, log, ln, log10, power, factorial, perm, comb, abs*

`a:` represents arc 

`perm` represents permutation, the format for writing permutation is 5P(2) not 5P2

`comb` represents combination, the format for writing combination is 5C(2) not 5C2


## Explanation of Core Algorithms

### CORDIC Algorithm
The **CORDIC (Coordinate Rotation Digital Computer)** algorithm is a method used for calculating trigonometric functions, 
hyperbolic functions, and square roots. It operates through iterative rotations to converge on the desired result 
efficiently.

### INV_CORDIC Algorithm
An inverse version of the CORDIC algorithm used for calculating inverse trigonometric functions like arcsine, arccosine....

### Newton-Raphson Method
A root-finding algorithm used here for high-precision computation of square roots and more. The method iteratively refines an 
initial guess to converge on an accurate result.

---
## License
[MIT License](https://opensource.org/licenses/MIT)

Copyright (c) 2024-present, Adeleke Adedeji

## Contributing
Contributions are highly welcomed! If you'd like to add new features or fix bugs, please fork the repository and submit a pull request.

## Author
Adeleke Adedeji

Feel free to reach out with questions or feedback!

Contact details: [aadeleke91618330@gmail.com](mailto:aadeleke91618330@gmail.com).

## Future Plans
- Extend support for additional mathematical functions.
- Improve performance for large-scale computations.
- Extension to evaluate matrix operations and vectors.
- Add visualization tools for computational workflows.

## Acknowledgments
Special thanks to the mathematicians and computer scientists whose work inspired the algorithms used in this library.
