# %%
d = list(
    map(
        lambda x: x.split(),
        """
noop
noop
addx 6
addx -1
noop
addx 5
addx 3
noop
addx 3
addx -1
addx -13
addx 17
addx 3
addx 3
noop
noop
noop
addx 5
addx 1
noop
addx 4
addx 1
noop
addx -38
addx 5
noop
addx 2
addx 3
noop
addx 2
addx 2
addx 3
addx -2
addx 5
addx 2
addx -18
addx 6
addx 15
addx 5
addx 2
addx -22
noop
noop
addx 30
noop
noop
addx -39
addx 1
addx 19
addx -16
addx 35
addx -28
addx -1
addx 12
addx -8
noop
addx 3
addx 4
noop
addx -3
addx 6
addx 5
addx 2
noop
noop
noop
noop
noop
addx 7
addx -39
noop
noop
addx 5
addx 2
addx 2
addx -1
addx 2
addx 2
addx 5
addx 1
noop
addx 4
addx -13
addx 18
noop
noop
noop
addx 12
addx -9
addx 8
noop
noop
addx -2
addx -36
noop
noop
addx 5
addx 2
addx 3
addx -2
addx 2
addx 2
noop
addx 3
addx 5
addx 2
addx 19
addx -14
noop
addx 2
addx 3
noop
addx -29
addx 34
noop
addx -35
noop
addx -2
addx 2
noop
addx 6
noop
noop
noop
noop
addx 2
noop
addx 3
addx 2
addx 5
addx 2
addx 1
noop
addx 4
addx -17
addx 18
addx 4
noop
addx 1
addx 4
noop
addx 1
noop
noop
""".strip().splitlines(),
    )
)

reg_values = [1, 1]

for instr_value in d:
    if instr_value == ["noop"]:
        reg_values.append(reg_values[-1])
    else:
        _addx, val_str = instr_value
        val = int(val_str)
        reg_values.append(reg_values[-1])
        reg_values.append(reg_values[-1] + val)

p1_res = sum(map(lambda i: i * reg_values[i], [20, 60, 100, 140, 180, 220]))
print(p1_res)

picture_tape = []
for cycle, pos in enumerate(reg_values[1:]):
    cycle_modulo = cycle % 40
    if abs(cycle_modulo - pos) <= 1:
        picture_tape.append("#")
    else:
        picture_tape.append(".")
    if cycle_modulo == 40 - 1:
        picture_tape.append("\n")

p2_res = "".join(picture_tape)
print(p2_res)
