from math import prod

from pulp import LpMaximize, LpProblem, LpVariable, lpSum
from pulp.apis import PULP_CBC_CMD

d_base = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 14 clay. Each geode robot costs 2 ore and 16 obsidian.
Blueprint 2: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 19 clay. Each geode robot costs 3 ore and 17 obsidian.
Blueprint 3: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 19 clay. Each geode robot costs 3 ore and 10 obsidian.
Blueprint 4: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 12 clay. Each geode robot costs 2 ore and 10 obsidian.
Blueprint 5: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 11 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 6: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 17 clay. Each geode robot costs 3 ore and 8 obsidian.
Blueprint 7: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 14 clay. Each geode robot costs 4 ore and 19 obsidian.
Blueprint 8: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 7 clay. Each geode robot costs 4 ore and 20 obsidian.
Blueprint 9: Each ore robot costs 2 ore. Each clay robot costs 2 ore. Each obsidian robot costs 2 ore and 10 clay. Each geode robot costs 2 ore and 11 obsidian.
Blueprint 10: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 4 ore and 17 obsidian.
Blueprint 11: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 3 ore and 8 obsidian.
Blueprint 12: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 16 clay. Each geode robot costs 2 ore and 15 obsidian.
Blueprint 13: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 6 clay. Each geode robot costs 3 ore and 16 obsidian.
Blueprint 14: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 5 clay. Each geode robot costs 4 ore and 11 obsidian.
Blueprint 15: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 20 clay. Each geode robot costs 3 ore and 18 obsidian.
Blueprint 16: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 17 clay. Each geode robot costs 4 ore and 20 obsidian.
Blueprint 17: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 7 clay. Each geode robot costs 2 ore and 16 obsidian.
Blueprint 18: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 18 clay. Each geode robot costs 4 ore and 12 obsidian.
Blueprint 19: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 5 clay. Each geode robot costs 2 ore and 10 obsidian.
Blueprint 20: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 4 ore and 9 obsidian.
Blueprint 21: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 16 clay. Each geode robot costs 3 ore and 20 obsidian.
Blueprint 22: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 23: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 20 clay. Each geode robot costs 2 ore and 19 obsidian.
Blueprint 24: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 20 clay. Each geode robot costs 4 ore and 18 obsidian.
Blueprint 25: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 10 clay. Each geode robot costs 4 ore and 8 obsidian.
Blueprint 26: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 8 clay. Each geode robot costs 3 ore and 9 obsidian.
Blueprint 27: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 15 clay. Each geode robot costs 2 ore and 13 obsidian.
Blueprint 28: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 15 clay. Each geode robot costs 4 ore and 20 obsidian.
Blueprint 29: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 6 clay. Each geode robot costs 4 ore and 11 obsidian.
Blueprint 30: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 20 clay. Each geode robot costs 2 ore and 20 obsidian.
""".strip()


ores = ("ore", "clay", "obsidian", "geode")


def get_ints(s: str) -> list[int]:
    return list(map(int, filter(lambda x: x.isdigit(), s.split())))


def parse_line(line: str):
    _, rest = line.split(": ")
    description = list(map(get_ints, rest.split(". ")))
    transitions = {
        ("ore", "robot"): {"ore": description[0][0]},
        ("clay", "robot"): {"ore": description[1][0]},
        ("obsidian", "robot"): {"ore": description[2][0], "clay": description[2][1]},
        ("geode", "robot"): {
            "ore": description[3][0],
            "obsidian": description[3][1],
        },
    }
    return transitions


d = list(
    map(
        lambda x: parse_line(x.replace("\n ", "")),
        d_base.split("\n\n" if "\n\n" in d_base else "\n"),
    )
)


def get_res(productions, number_of_steps=24):
    model = LpProblem(name="this blueprint".replace(" ", "_"), sense=LpMaximize)

    # All variables
    variables = []
    for step_number in range(number_of_steps + 1):
        variables.append({})
        for r in ores:
            variables[-1][r] = LpVariable(
                name=f"{step_number:02d} step {r}".replace(" ", "_"),
                lowBound=0,
                cat="Integer",
            )
            variables[-1][(r, "robot")] = LpVariable(
                name=f"{step_number:02d} step robot {r}".replace(" ", "_"),
                lowBound=0,
                cat="Integer",
            )
            if step_number > 0:
                variables[-1][(r, "robot_production")] = LpVariable(
                    name=f"{step_number:02d} step robot_production {r}".replace(
                        " ", "_"
                    ),
                    lowBound=0,
                    upBound=1,
                    cat="Integer",
                )

    model += lpSum([variables[-1]["geode"]])

    # Initial values
    for n, variable in variables[0].items():
        value = 0 if n != ("ore", "robot") else 1
        model += (variable == value, f"{n} initial value {value}")

    for step_number in range(number_of_steps):

        # At most one robot is produced
        model += (
            variables[step_number + 1][("ore", "robot_production")]
            + variables[step_number + 1][("clay", "robot_production")]
            + variables[step_number + 1][("obsidian", "robot_production")]
            + variables[step_number + 1][("geode", "robot_production")]
            <= 1,
            f"{step_number:02d} step total robots production".replace(" ", "_"),
        )

        # Robot production
        for r in ores:
            model += (
                variables[step_number + 1][(r, "robot_production")]
                == variables[step_number + 1][(r, "robot")]
                - variables[step_number][(r, "robot")],
                f"{step_number:02d} step {r} robot count after".replace(" ", "_"),
            )

        # Resource production
        r = "ore"
        model += (
            variables[step_number + 1][r]
            == variables[step_number][r]
            + variables[step_number][(r, "robot")]
            - productions[("ore", "robot")][r]
            * variables[step_number + 1][("ore", "robot_production")]
            - productions[("clay", "robot")][r]
            * variables[step_number + 1][("clay", "robot_production")]
            - productions[("obsidian", "robot")][r]
            * variables[step_number + 1][("obsidian", "robot_production")]
            - productions[("geode", "robot")][r]
            * variables[step_number + 1][("geode", "robot_production")],
            f"{step_number:02d} step {r} production and usage".replace(" ", "_"),
        )
        model += (
            variables[step_number][r]
            >= productions[("ore", "robot")][r]
            * variables[step_number + 1][("ore", "robot_production")]
            + productions[("clay", "robot")][r]
            * variables[step_number + 1][("clay", "robot_production")]
            + productions[("obsidian", "robot")][r]
            * variables[step_number + 1][("obsidian", "robot_production")]
            + productions[("geode", "robot")][r]
            * variables[step_number + 1][("geode", "robot_production")],
            f"{step_number:02d} step {r} usage".replace(" ", "_"),
        )

        r = "clay"
        model += (
            variables[step_number + 1][r]
            == variables[step_number][r]
            + variables[step_number][(r, "robot")]
            - productions[("obsidian", "robot")][r]
            * variables[step_number + 1][("obsidian", "robot_production")],
            f"{step_number:02d} step {r} production and usage".replace(" ", "_"),
        )
        model += (
            variables[step_number][r]
            >= productions[("obsidian", "robot")][r]
            * variables[step_number + 1][("obsidian", "robot_production")],
            f"{step_number:02d} step {r} usage".replace(" ", "_"),
        )

        r = "obsidian"
        model += (
            variables[step_number + 1][r]
            == variables[step_number][r]
            + variables[step_number][(r, "robot")]
            - productions[("geode", "robot")][r]
            * variables[step_number + 1][("geode", "robot_production")],
            f"{step_number:02d} step {r} production and usage".replace(" ", "_"),
        )
        model += (
            variables[step_number][r]
            >= productions[("geode", "robot")][r]
            * variables[step_number + 1][("geode", "robot_production")],
            f"{step_number:02d} step {r} usage".replace(" ", "_"),
        )

        r = "geode"
        model += (
            variables[step_number + 1][r]
            == variables[step_number][r] + variables[step_number][(r, "robot")],
            f"{step_number:02d} step {r} production and usage".replace(" ", "_"),
        )

    model.solve(PULP_CBC_CMD(msg=False))

    return int(model.objective.value())


results = list(map(get_res, d))
p1_res = sum(map(lambda ix: (ix[0] + 1) * ix[1], enumerate(results)))
print(p1_res)


results_p2 = list(map(lambda x: get_res(x, number_of_steps=32), d[:3]))
p2_res = prod(results_p2)
print(p2_res)
