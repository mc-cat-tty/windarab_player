import ast

def transpose(matrix: list[list]):
  return list(zip(*matrix))

def eval_literal_str(literal: str):
  return ast.literal_eval(literal.title())