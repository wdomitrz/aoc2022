# %%
from math import prod

d = """
Monkey 0:
  Starting items: 52, 60, 85, 69, 75, 75
  Operation: new = old * 17
  Test: divisible by 13
    If true: throw to monkey 6
    If false: throw to monkey 7

Monkey 1:
  Starting items: 96, 82, 61, 99, 82, 84, 85
  Operation: new = old + 8
  Test: divisible by 7
    If true: throw to monkey 0
    If false: throw to monkey 7

Monkey 2:
  Starting items: 95, 79
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 5
    If false: throw to monkey 3

Monkey 3:
  Starting items: 88, 50, 82, 65, 77
  Operation: new = old * 19
  Test: divisible by 2
    If true: throw to monkey 4
    If false: throw to monkey 1

Monkey 4:
  Starting items: 66, 90, 59, 90, 87, 63, 53, 88
  Operation: new = old + 7
  Test: divisible by 5
    If true: throw to monkey 1
    If false: throw to monkey 0

Monkey 5:
  Starting items: 92, 75, 62
  Operation: new = old * old
  Test: divisible by 3
    If true: throw to monkey 3
    If false: throw to monkey 4

Monkey 6:
  Starting items: 94, 86, 76, 67
  Operation: new = old + 1
  Test: divisible by 11
    If true: throw to monkey 5
    If false: throw to monkey 2

Monkey 7:
  Starting items: 57
  Operation: new = old + 2
  Test: divisible by 17
    If true: throw to monkey 6
    If false: throw to monkey 2
"""


class Monkey:
    def __init__(self, m_str, divide_by_3=True, modulo_by=None):
        m_lines = list(map(lambda x: x.strip(), m_str.splitlines()))
        self.number = int(m_lines[0].replace("Monkey ", "").replace(":", ""))
        self.items = list(
            map(int, m_lines[1].replace("Starting items: ", "").split(", "))
        )
        self.operation = m_lines[2].replace("Operation: new = ", "")
        self.divisible_test = int(m_lines[3].replace("Test: divisible by ", ""))
        self.if_true_direction = int(
            m_lines[4].replace("If true: throw to monkey ", "")
        )
        self.if_false_direction = int(
            m_lines[5].replace("If false: throw to monkey ", "")
        )
        self.inspection_count = 0
        self.divide_by_3 = divide_by_3
        self.modulo_by = modulo_by

    def operation_on_item(self, item_value):
        self.inspection_count += 1
        new_value = int(eval(self.operation, {"old": item_value}))
        if self.divide_by_3:
            new_value //= 3
        if self.modulo_by is not None:
            new_value %= self.modulo_by
        return new_value

    def run_operation(self):
        self.items = list(map(self.operation_on_item, self.items))

    def pass_item_to(self, item_value):
        if item_value % self.divisible_test == 0:
            return self.if_true_direction
        else:
            return self.if_false_direction


def load_monkeys(divide_by_3=True, modulo_by=None):
    return list(
        map(
            lambda x: Monkey(x, divide_by_3=divide_by_3, modulo_by=modulo_by),
            d.strip().split("\n\n"),
        )
    )


monkeys = load_monkeys()

for _ in range(20):
    for m in monkeys:
        m.run_operation()
        for item in m.items:
            to_whom = m.pass_item_to(item)
            monkeys[to_whom].items.append(item)
        m.items = []

p1_res = prod(list(sorted(list(map(lambda m: m.inspection_count, monkeys))))[-2:])
print(p1_res)


monkeys = load_monkeys(
    divide_by_3=False, modulo_by=prod(map(lambda m: m.divisible_test, monkeys))
)
for _ in range(10000):
    for m in monkeys:
        m.run_operation()
        for item in m.items:
            to_whom = m.pass_item_to(item)
            monkeys[to_whom].items.append(item)
        m.items = []

p2_res = prod(list(sorted(list(map(lambda m: m.inspection_count, monkeys))))[-2:])
print(p2_res)

a = 7
