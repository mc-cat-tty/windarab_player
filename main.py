import sys
from lib.parser import ParserTxt

if __name__ == "__main__":
  filename = sys.argv[1]
  p = ParserTxt(filename)
