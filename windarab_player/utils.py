import ast
from struct import pack

def transpose(matrix: list[list]):
  return list(zip(*matrix))

def eval_literal_str(literal: str):
  return ast.literal_eval(literal.title())

def float_to_ecu_int(val: float, ratio: int) -> int:
  return int.from_bytes(pack(">i", int(val * ratio)))