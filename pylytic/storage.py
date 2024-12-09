from enum import Enum

_stored_values_ctan_dict = {
    1: 45.0, 0.5: 26.56505117707799,
    0.25: 14.036243467926479, 0.125: 7.125016348901798,
    0.0625: 3.576334374997351, 0.03125: 1.7899106082460694,
    0.015625: 0.8951737102110744, 0.0078125: 0.4476141708605531,
    0.00390625: 0.22381050036853808, 0.001953125: 0.1119056770662069,
    0.0009765625: 0.055952891893803675, 0.00048828125: 0.027976452617003676,
    0.000244140625: 0.013988227142265016, 0.0001220703125: 0.006994113675352919,
    6.103515625e-05: 0.003497056850704011, 3.0517578125e-05: 0.0017485284269804495,
    1.52587890625e-05: 0.0008742642136937803, 7.62939453125e-06: 0.00043713210687233457,
    3.814697265625e-06: 0.00021856605343934784, 1.9073486328125e-06: 0.00010928302672007149,
    9.5367431640625e-07: 5.464151336008544e-05, 4.76837158203125e-07: 2.7320756680048934e-05,
    2.384185791015625e-07: 1.3660378340025243e-05, 1.1920928955078125e-07: 6.830189170012719e-06,
    5.960464477539063e-08: 3.4150945850063712e-06, 2.9802322387695312e-08: 1.7075472925031871e-06,
    1.4901161193847656e-08: 8.537736462515938e-07, 7.450580596923828e-09: 4.2688682312579694e-07,
    3.725290298461914e-09: 2.1344341156289847e-07, 1.862645149230957e-09: 1.0672170578144923e-07,
    9.313225746154785e-10: 5.336085289072462e-08, 4.656612873077393e-10: 2.668042644536231e-08,
    2.3283064365386963e-10: 1.3340213222681154e-08, 1.1641532182693481e-10: 6.670106611340577e-09,
    5.820766091346741e-11: 3.3350533056702886e-09, 2.9103830456733704e-11: 1.6675266528351443e-09,
    1.4551915228366852e-11: 8.337633264175721e-10, 7.275957614183426e-12: 4.1688166320878607e-10,
    3.637978807091713e-12: 2.0844083160439303e-10, 1.8189894035458565e-12: 1.0422041580219652e-10,
    9.094947017729282e-13: 5.211020790109826e-11, 4.547473508864641e-13: 2.605510395054913e-11,
    2.2737367544323206e-13: 1.3027551975274565e-11, 1.1368683772161603e-13: 6.513775987637282e-12,
    5.684341886080802e-14: 3.256887993818641e-12, 2.842170943040401e-14: 1.6284439969093206e-12,
    1.4210854715202004e-14: 8.142219984546603e-13, 7.105427357601002e-15: 4.0711099922733015e-13,
    3.552713678800501e-15: 2.0355549961366507e-13, 1.7763568394002505e-15: 1.0177774980683254e-13,
    8.881784197001252e-16: 5.088887490341627e-14
}


class Constants(Enum):
    """
    class Constants defines the constant variables required by m_eval module
    """
    PI = 3.1415926536
    C_SCALING_FACTOR = 0.6072529350088814
    H_SCALING_FACTOR = 1.207497067763072
    e = 2.718281828459045
    ln2 = 0.69314718056
    ln10 = 2.3025850930
    TOTAL_CIRCLE = 360
    HALF_CIRCLE = 180
    QUARTER_CIRCLE = 90
    X_, Y_ = 1, 0


class EvalConstants(Enum):
    """
    class EvalConstants defines Token_types required for lexical analysis
    """
    SPACES: str = " {}{}".format("\n", "\t")
    NUMBER: str = "0123456789."
    OPERATOR: dict = {"+": "PLUS", "-": "MINUS", "/": "DIV", "*": "MUL", "(": "L_PAREN", ")": "R_PAREN", "^": "POWER"}
    FUNCTION: tuple = ("sin", "cos", "tan", "!", "abs", "p", "c", "asin", "acos", "atan", "sec", "cosec", "cot",
                       "asec", "acosec", "acot", "sinh", "cosh", "tanh", "asinh", "acosh", "atanh", "sech", "cosech",
                       "coth", "asech", "acosech", "acoth", "ln", "log",
                       )
    CONSTANT: dict = {"pi": 3.1415926536, "e": 2.718281828459045}
