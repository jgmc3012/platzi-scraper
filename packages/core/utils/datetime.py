from re import match as find
from logging import getLogger

logger = getLogger('log_print')

def str_to_seg(string: str) -> int:
  """Transform a string with the format 'mm:ss min'  
  Args:
      string (str): 

  Returns:
      int: seconds

  >>> str_to_seg('05:11 min')
  311
  """
  match = find(r'(\d+):(\d+) min', string)
  if not match:
    logger.warn(f'{string} dont match with str_to_seg pattern.')
    return 0

  min, seg = match.groups()
  return min * 60 + seg