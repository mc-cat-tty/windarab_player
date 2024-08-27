import re, sys
from typing import Generator

class Parser:
  COMMENT_REGEX = re.compile(r"\w*#.*")
  HEADER_ENTRY_REGEX = re.compile(r".+?]")
  UNIT_OF_MEASUREMENT_REGEX = re.compile("\[.+\]")

  def __init__(self, filename: str):
    self.filename = filename

  @staticmethod
  def is_comment(line: str):
    return bool(Parser.COMMENT_REGEX.match(line))

  @staticmethod  
  def is_empty(line: str):
    return bool(line.strip())
  
  def get_lines(self) -> Generator[str]:
    with open(self.filename, 'r') as file:
      return filter(
        file.readlines(),
        lambda line: not (Parser.is_empty(line) or Parser.is_comment(line))
      )
  
  def get_header(self) -> Generator[str]:
    return map(
      str.strip(),
      Parser.HEADER_ENTRY_REGEX.findall(self.get_lines()[0])
    )

  def get_unit_of_measurements(self) -> dict[str, str]:
    get_signal_um = lambda entry: Parser.UNIT_OF_MEASUREMENT_REGEX.search(entry, 1).group()
    get_signal_name = lambda entry: entry.split(get_signal_um(entry))[0].strip()

    return {
      get_signal_name(entry): get_signal_um(entry)
      for entry in self.get_header()
    }
  
  @staticmethod
  def parse_sample(sample_line: str) -> Generator[str]:
    return map(
      str.strip,
      re.split(r" +", sample_line)[1:]
    )

  def get_samples(self) -> dict[str, str]:
    return 


if __name__ == "__main__":
  p = Parser(sys.argv[1])
  print(p.get_unit_of_measurements())
  print(p.get_samples())
