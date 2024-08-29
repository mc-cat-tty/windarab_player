import ast
from struct import pack

def transpose(matrix: list[list]):
  return list(zip(*matrix))

def eval_literal_str(literal: str):
  return ast.literal_eval(literal.title())

def align(data, alignment_bytes: int = 0):
  return data << (alignment_bytes * 8)

def float_to_ecu(format: str, val: float, ratio: int, byte_align: int = 0) -> int:
  return align(
    int.from_bytes(pack(f">{format}", int(val * ratio)), byteorder='big'),
    byte_align
  )

def float_to_ecu_int(val: float, ratio: int, byte_align: int = 0) -> int:
  return float_to_ecu("i", val, ratio, byte_align)

def float_to_ecu_short(val: float, ratio: int, byte_align: int = 0) -> int:
  return float_to_ecu("h", val, ratio, byte_align)
