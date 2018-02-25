meta:
  id: comparison_1_kaitai
  encoding: utf-8
  endian: le
seq:
  - id: count
    type: u4
  - id: items
    repeat: expr
    repeat-expr: count
    type: item
types:
  item:
    seq:
      - id: num1
        type: u1
      - id: num2_lo
        type: u2
      - id: num2_hi
        type: u1
      - id: flags
        type: flags
      - id: fixedarray1
        repeat: expr
        repeat-expr: 3
        type: u1
      - id: name1
        type: strz
      - id: len_name2
        type: u1
      - id: name2
        type: str
        size: len_name2
    instances:
      num2:
        value: 'num2_hi << 16 | num2_lo'
    types:
      flags:
        seq:
          - id: bool1
            type: b1
          - id: num4
            type: b3
          - id: padding
            type: b4
