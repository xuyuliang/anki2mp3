import re


def detect_hash_with_spaces(string):
  """Returns True if the string begins with a # character, including spaces."""

  # Compile the regular expression pattern.
  pattern = re.compile(r'^[ \t]*#') 

  # Match the pattern against the string.
  match = pattern.match(string)

  # Return True if there is a match, False otherwise.
  return match is not None

astring ='  	#haha'
rst = detect_hash_with_spaces(astring)
print(rst)