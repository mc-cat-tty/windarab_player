import re, sys
from typing import Generator
from windarab_player.utils import transpose, eval_literal_str

class ParserTxt:
  COMMENT_REGEX = re.compile(r"\w*#.*")
  HEADER_ENTRY_REGEX = re.compile(r".*?]")
  UNIT_OF_MEASUREMENT_REGEX = re.compile("\[.*\]")

  def __init__(self, filename: str):
    self.filename = filename

  @staticmethod
  def is_comment(line: str) -> bool:
    return bool(ParserTxt.COMMENT_REGEX.match(line))

  @staticmethod  
  def is_empty(line: str) -> bool:
    return not line.strip()
  
  def __get_lines(self) -> Generator[str, None, None]:
    with open(self.filename, 'r', errors="replace") as file:
      return filter(
        lambda line: not (ParserTxt.is_empty(line) or ParserTxt.is_comment(line)),
        file.readlines()
      )
  
  def __get_header(self) -> Generator[str, None, None]:
    lines = list(self.__get_lines())

    return map(
      str.strip,
      ParserTxt.HEADER_ENTRY_REGEX.findall(lines[0])
    )

  def get_unit_of_measurements(self) -> dict[str, str]:
    get_signal_um = lambda entry: ParserTxt.UNIT_OF_MEASUREMENT_REGEX.search(entry, 1).group()
    get_signal_name = lambda entry: entry.split(get_signal_um(entry))[0].strip()

    return {
      get_signal_name(entry): get_signal_um(entry)
      for entry in self.__get_header()
    }
  
  @staticmethod
  def parse_line(sample_line: str) -> Generator[str, None, None]:
    return map(
      eval_literal_str,
      map(
        str.strip,
        re.split("\t *", sample_line)
      )
    )

  def get_samples(self) -> dict[str, str]:
    lines = list(self.__get_lines())

    unlabeled_samples = transpose(
      list(
        map(
          ParserTxt.parse_line,
          lines[1:]  # Discard header line
        )
      )
    )

    return dict(
      zip(self.get_unit_of_measurements().keys(), unlabeled_samples)
    )


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Pass data log filename as first and only argument")
    sys.exit(1)
  
  p = ParserTxt(sys.argv[1])
  print(p.get_unit_of_measurements())
  print(p.get_samples()['xtime'])
