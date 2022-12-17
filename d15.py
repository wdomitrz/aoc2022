# %%
def parse_row(row):
    values = list(
        map(
            int,
            row.replace("Sensor at x=", "")
            .replace(" y=", "")
            .replace(": closest beacon is at x=", ",")
            .split(","),
        )
    )
    return (values[0], values[1]), (values[2], values[3])


d = list(
    map(
        parse_row,
        """
Sensor at x=9450, y=2172986: closest beacon is at x=-657934, y=1258930
Sensor at x=96708, y=1131866: closest beacon is at x=-657934, y=1258930
Sensor at x=1318282, y=3917725: closest beacon is at x=-39403, y=3757521
Sensor at x=3547602, y=1688021: closest beacon is at x=3396374, y=1626026
Sensor at x=3452645, y=2433208: closest beacon is at x=3249864, y=2880665
Sensor at x=46113, y=3689394: closest beacon is at x=-39403, y=3757521
Sensor at x=2291648, y=2980268: closest beacon is at x=2307926, y=3005525
Sensor at x=3127971, y=2022110: closest beacon is at x=3396374, y=1626026
Sensor at x=2301436, y=2996160: closest beacon is at x=2307926, y=3005525
Sensor at x=2989899, y=3239346: closest beacon is at x=3551638, y=3263197
Sensor at x=544144, y=3031363: closest beacon is at x=-39403, y=3757521
Sensor at x=3706626, y=767329: closest beacon is at x=3396374, y=1626026
Sensor at x=2540401, y=2746490: closest beacon is at x=2342391, y=2905242
Sensor at x=2308201, y=2997719: closest beacon is at x=2307926, y=3005525
Sensor at x=782978, y=1855194: closest beacon is at x=1720998, y=2000000
Sensor at x=2317632, y=2942537: closest beacon is at x=2342391, y=2905242
Sensor at x=1902546, y=2461891: closest beacon is at x=1720998, y=2000000
Sensor at x=3967424, y=1779674: closest beacon is at x=3396374, y=1626026
Sensor at x=2970495, y=2586314: closest beacon is at x=3249864, y=2880665
Sensor at x=3560435, y=3957350: closest beacon is at x=3551638, y=3263197
Sensor at x=3932297, y=3578328: closest beacon is at x=3551638, y=3263197
Sensor at x=2819004, y=1125748: closest beacon is at x=3396374, y=1626026
Sensor at x=2793841, y=3805575: closest beacon is at x=3015097, y=4476783
Sensor at x=3096324, y=109036: closest beacon is at x=3396374, y=1626026
Sensor at x=3678551, y=3050855: closest beacon is at x=3551638, y=3263197
Sensor at x=1699186, y=3276187: closest beacon is at x=2307926, y=3005525
Sensor at x=3358443, y=3015038: closest beacon is at x=3249864, y=2880665
Sensor at x=2309805, y=1755792: closest beacon is at x=1720998, y=2000000
Sensor at x=2243001, y=2876549: closest beacon is at x=2342391, y=2905242
Sensor at x=2561955, y=3362969: closest beacon is at x=2307926, y=3005525
Sensor at x=2513546, y=2393940: closest beacon is at x=2638370, y=2329928
Sensor at x=1393638, y=419289: closest beacon is at x=1720998, y=2000000
Sensor at x=2696979, y=2263077: closest beacon is at x=2638370, y=2329928
Sensor at x=3842041, y=2695378: closest beacon is at x=3249864, y=2880665
""".strip().splitlines(),
    )
)

y_line = 2000000
intervals = []

for (sensor_x, sensor_y), (beacon_x, beacon_y) in d:
    dist = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
    dist_y = abs(sensor_y - y_line)
    if dist > dist_y:
        intervals.append((sensor_x - dist + dist_y, sensor_x + dist - dist_y))

intervals = sorted(intervals)
total_length = 0
last_end = intervals[0][0] - 1
for b, e in intervals:
    b = max(b, last_end + 1)
    if e >= b:
        total_length += e - b + 1
    last_end = max(e, last_end)
p1_res = total_length - len(
    set(filter(lambda xy: xy[1] == y_line, map(lambda row: row[1], d)))
)
print(p1_res)

limit2 = 4000000

p2_res = 0
x_mult = 4000000
for y_line in range(limit2 + 1):
    intervals = []
    for (sensor_x, sensor_y), (beacon_x, beacon_y) in d:
        dist = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
        dist_y = abs(sensor_y - y_line)
        if dist > dist_y:
            intervals.append((sensor_x - dist + dist_y, sensor_x + dist - dist_y))

    intervals = sorted(intervals)
    total_length = 0
    if len(intervals) == 0 or len(intervals[0]) == 0:
        continue
    last_end = max(0, intervals[0][0]) - 1
    for b, e in intervals:
        b = max(b, last_end + 1)
        e = min(e, limit2)
        if e >= b:
            total_length += e - b + 1
            last_end = max(e, last_end)
    if total_length < limit2 + 1:
        p2_res += y_line
        break

for y_line in range(limit2 + 1):
    intervals = []
    for (sensor_y, sensor_x), (beacon_y, beacon_x) in d:
        dist = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
        dist_y = abs(sensor_y - y_line)
        if dist > dist_y:
            intervals.append((sensor_x - dist + dist_y, sensor_x + dist - dist_y))

    intervals = sorted(intervals)
    total_length = 0
    if len(intervals) == 0 or len(intervals[0]) == 0:
        continue
    last_end = max(0, intervals[0][0]) - 1
    for b, e in intervals:
        b = max(b, last_end + 1)
        e = min(e, limit2)
        if e >= b:
            total_length += e - b + 1
            last_end = max(e, last_end)
    if total_length < limit2 + 1:
        p2_res += y_line * x_mult
        break

print(p2_res)
