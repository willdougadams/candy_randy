def read_config(filename):
  attribute_dict = {}
  with open(filename) as fin:
    lines = fin.readlines()

  for line in lines:
    if (not line.strip()) or line[0] == "#":
      continue

    attribute = line.split(":")[0].strip()
    value = line.split(":")[1].strip()
    attribute_dict[attribute] = (value if len(value.split()) == 1 else value.split())
    if len(attribute_dict[attribute]) == 1:
      attribute_dict[attribute] = attribute_dict[attribute][0]

  return attribute_dict


class colors():
  BLACK = tuple(map(int, [0, 0, 0]))
  WHITE = tuple(map(int, [255, 255, 255]))
  BLUE  = tuple(map(int, [0, 0, 255]))
  GREEN = tuple(map(int, [0, 255, 0]))
  RED = tuple(map(int, [255, 0, 0]))