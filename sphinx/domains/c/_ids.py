from __future__ import annotations
import re
_keywords = ['auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'inline', 'int', 'long', 'register', 'restrict', 'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while', '_Alignas', '_Alignof', '_Atomic', '_Bool', '_Complex', '_Decimal32', '_Decimal64', '_Decimal128', '_Generic', '_Imaginary', '_Noreturn', '_Static_assert', '_Thread_local']
_macroKeywords = ['alignas', 'alignof', 'bool', 'complex', 'imaginary', 'noreturn', 'static_assert', 'thread_local']
_expression_bin_ops = [['||', 'or'], ['&&', 'and'], ['|', 'bitor'], ['^', 'xor'], ['&', 'bitand'], ['==', '!=', 'not_eq'], ['<=', '>=', '<', '>'], ['<<', '>>'], ['+', '-'], ['*', '/', '%'], ['.*', '->*']]
_expression_unary_ops = ['++', '--', '*', '&', '+', '-', '!', 'not', '~', 'compl']
_expression_assignment_ops = ['=', '*=', '/=', '%=', '+=', '-=', '>>=', '<<=', '&=', 'and_eq', '^=', 'xor_eq', '|=', 'or_eq']
_max_id = 1
_id_prefix = [None, 'c.', 'Cv2.']
_string_re = re.compile('[LuU8]?(\'([^\'\\\\]*(?:\\\\.[^\'\\\\]*)*)\'|"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)")', re.DOTALL)
_simple_type_specifiers_re = re.compile('\n    \\b(\n    void|_Bool\n    |signed|unsigned\n    |short|long\n    |char\n    |int\n    |__uint128|__int128\n    |__int(8|16|32|64|128)  # extension\n    |float|double\n    |_Decimal(32|64|128)\n    |_Complex|_Imaginary\n    |__float80|_Float64x|__float128|_Float128|__ibm128  # extension\n    |__fp16  # extension\n    |_Sat|_Fract|fract|_Accum|accum  # extension\n    )\\b\n', re.VERBOSE)