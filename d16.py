# %%
def parse_row(row):
    data = (
        row.replace("Valve ", "")
        .replace(" has flow rate=", ", ")
        .replace("tunnels lead ", "tunnel leads ")
        .replace("valves ", "valve ")
        .replace("; tunnel leads to valve ", ", ")
        .split(", ")
    )
    return data[0], int(data[1]), data[2:]


d = list(
    map(
        parse_row,
        """
Valve VR has flow rate=11; tunnels lead to valves LH, KV, BP
Valve UV has flow rate=0; tunnels lead to valves GH, RO
Valve OH has flow rate=0; tunnels lead to valves AJ, NY
Valve GD has flow rate=0; tunnels lead to valves TX, PW
Valve NS has flow rate=0; tunnels lead to valves AJ, AA
Valve KZ has flow rate=18; tunnels lead to valves KO, VK, PJ
Valve AH has flow rate=0; tunnels lead to valves ZP, DI
Valve SA has flow rate=0; tunnels lead to valves VG, JF
Valve VK has flow rate=0; tunnels lead to valves RO, KZ
Valve GB has flow rate=0; tunnels lead to valves XH, AA
Valve AJ has flow rate=6; tunnels lead to valves IC, OH, ZR, NS, EM
Valve PJ has flow rate=0; tunnels lead to valves KZ, SP
Valve KO has flow rate=0; tunnels lead to valves KZ, LE
Valve AA has flow rate=0; tunnels lead to valves TW, GB, TI, NS, UL
Valve TW has flow rate=0; tunnels lead to valves TU, AA
Valve VG has flow rate=25; tunnel leads to valve SA
Valve BP has flow rate=0; tunnels lead to valves RO, VR
Valve XH has flow rate=0; tunnels lead to valves GB, RI
Valve TX has flow rate=0; tunnels lead to valves RI, GD
Valve IR has flow rate=10; tunnels lead to valves TN, NY, JF
Valve TU has flow rate=0; tunnels lead to valves JD, TW
Valve KC has flow rate=0; tunnels lead to valves SP, RO
Valve LN has flow rate=0; tunnels lead to valves EM, RI
Valve HD has flow rate=0; tunnels lead to valves FE, SC
Valve KE has flow rate=0; tunnels lead to valves OM, RI
Valve VY has flow rate=0; tunnels lead to valves PW, BS
Valve LH has flow rate=0; tunnels lead to valves OM, VR
Valve EM has flow rate=0; tunnels lead to valves AJ, LN
Valve SO has flow rate=22; tunnels lead to valves ZP, FE
Valve EC has flow rate=0; tunnels lead to valves OM, UL
Valve KV has flow rate=0; tunnels lead to valves SP, VR
Valve FE has flow rate=0; tunnels lead to valves SO, HD
Valve TI has flow rate=0; tunnels lead to valves AA, PW
Valve SC has flow rate=14; tunnel leads to valve HD
Valve ZP has flow rate=0; tunnels lead to valves SO, AH
Valve RO has flow rate=19; tunnels lead to valves UV, BP, VK, KC
Valve ZR has flow rate=0; tunnels lead to valves OM, AJ
Valve JL has flow rate=21; tunnels lead to valves GN, TN
Valve PW has flow rate=9; tunnels lead to valves TI, GN, VY, GD, IC
Valve UL has flow rate=0; tunnels lead to valves EC, AA
Valve GN has flow rate=0; tunnels lead to valves JL, PW
Valve TN has flow rate=0; tunnels lead to valves JL, IR
Valve NV has flow rate=0; tunnels lead to valves RI, JD
Valve DI has flow rate=23; tunnels lead to valves LE, AH
Valve IC has flow rate=0; tunnels lead to valves PW, AJ
Valve JF has flow rate=0; tunnels lead to valves SA, IR
Valve LE has flow rate=0; tunnels lead to valves DI, KO
Valve BS has flow rate=0; tunnels lead to valves JD, VY
Valve JD has flow rate=15; tunnels lead to valves NV, TU, BS
Valve SP has flow rate=24; tunnels lead to valves KC, KV, PJ
Valve NY has flow rate=0; tunnels lead to valves IR, OH
Valve OM has flow rate=7; tunnels lead to valves EC, GH, KE, ZR, LH
Valve GH has flow rate=0; tunnels lead to valves OM, UV
Valve RI has flow rate=3; tunnels lead to valves NV, KE, LN, XH, TX
""".strip().splitlines(),
    )
)

values = {row[0]: row[1] for row in d if row[1] > 0}

edges = {row[0]: row[2] for row in d}


def next_step(reachable):
    next_reachable = {}
    for (v, vis), val in reachable.items():
        vis_vals = sum(map(lambda x: values[x], vis))
        for u in edges[v]:
            M = val + vis_vals
            if (u, vis) in next_reachable:
                M = max(M, next_reachable[u, vis])
            next_reachable[u, vis] = M

        if v in values:
            M = val + vis_vals
            if (v, vis | {v}) in next_reachable:
                M = max(M, next_reachable[v, vis | {v}])
            next_reachable[v, vis | {v}] = M
    return next_reachable


start = "AA"
reachable = {(start, frozenset()): 0}

for _ in range(30):
    reachable = next_step(reachable)

p1_res = max(reachable.values())
print(p1_res)


def next_step2(reachable):
    next_reachable = {}
    for ((v0, v1), vis), val in reachable.items():
        vis_vals = sum(map(lambda x: values[x], vis))
        for u0 in edges[v0]:
            for u1 in edges[v1]:
                u = u0, u1
                M = val + vis_vals
                if (u, vis) in next_reachable:
                    M = max(M, next_reachable[u, vis])
                next_reachable[u, vis] = M

        if v1 in values:
            for u0 in edges[v0]:
                M = val + vis_vals
                v = u0, v1
                if (v, vis | {v1}) in next_reachable:
                    M = max(M, next_reachable[v, vis | {v1}])
                next_reachable[v, vis | {v1}] = M

        if v0 in values:
            for u1 in edges[v1]:
                M = val + vis_vals
                v = v0, u1
                if (v, vis | {v0}) in next_reachable:
                    M = max(M, next_reachable[v, vis | {v0}])
                next_reachable[v, vis | {v0}] = M

        if v0 in values and v1 in values:
            v = v0, v1
            M = val + vis_vals
            if (v, vis | {v0, v1}) in next_reachable:
                M = max(M, next_reachable[v, vis | {v0, v1}])
            next_reachable[v, vis | {v0, v1}] = M
    return next_reachable


reachable2 = {((start, start), frozenset()): 0}

for i in range(26):
    reachable2 = next_step2(reachable2)

p2_res = max(reachable2.values())
print(p2_res)
