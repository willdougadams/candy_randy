def read_config(filename):
  attribute_dict = {}
  with open(filename) as fin:
    lines = fin.readlines()

  for line in lines:
    if (not line.strip()) or line[0] == "#":
      continue

    attribute = line.split(":")[0]
    value = line.split(":")[1]
    attribute_dict[attribute] = (value if len(value.split()) == 1 else value.split())
    if len(attribute_dict[attribute]) == 1:
      attribute_dict[attribute] = attribute_dict[attribute][0]

  return attribute_dict
