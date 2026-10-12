"""Unit 3: a reactive (subsumption) agent versus a BDI agent.

World: a 10x10 grid with a charger at (0, 0) and three packages at a time.
Collecting a package (stepping on it) spawns a new one elsewhere. Each move
costs 1 battery; standing on the charger refills it. At 0 battery the agent
stops for good. Both agents sense packages within 2 cells and always know
where the charger is.
"""
import random
import statistics

SIZE, CHARGER, MAX_BATTERY, SENSE = 10, (0, 0), 40, 2


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def step_towards(pos, target):
    (x, y), (tx, ty) = pos, target
    if x != tx:
        return (x + (1 if tx > x else -1), y)
    if y != ty:
        return (x, y + (1 if ty > y else -1))
    return pos


class World:
    def __init__(self, rng):
        self.rng = rng
        self.packages = set()
        while len(self.packages) < 3:
            self._spawn()

    def _spawn(self):
        while True:
            p = (self.rng.randrange(SIZE), self.rng.randrange(SIZE))
            if p != CHARGER and p not in self.packages:
                self.packages.add(p)
                return

    def sensed(self, pos):
        return {p for p in self.packages if dist(p, pos) <= SENSE}

    def collect(self, pos):
        if pos in self.packages:
            self.packages.remove(pos)
            self._spawn()
            return True
        return False


class SubsumptionAgent:
    """Brooks-style layers; a higher layer suppresses the ones below it.
    No memory and no planning: each step is a fresh reaction."""

    def __init__(self, rng):
        self.rng = rng

    def act(self, pos, battery, sensed):
        if battery <= dist(pos, CHARGER) + 2:        # layer 1: survive
            return step_towards(pos, CHARGER)
        if sensed:                                   # layer 2: collect
            return step_towards(pos, min(sensed, key=lambda p: dist(p, pos)))
        x, y = pos                                   # layer 3: wander
        moves = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                 if 0 <= x + dx < SIZE and 0 <= y + dy < SIZE]
        return self.rng.choice(moves)


class BDIAgent:
    """Beliefs: remembered package locations and battery level.
    Desires: every known package, plus staying charged.
    Intention: the one desire it has committed to; it keeps it until it is
    achieved or believed impossible, re-deliberating only then."""

    RESERVE = 1                     # spare battery kept for the trip home

    def __init__(self, rng):
        self.rng = rng
        self.known = set()          # beliefs about where packages are
        self.intention = None       # ("collect", p) | ("recharge",) | ("explore", p)

    def deliberate(self, pos, battery):
        options = [p for p in self.known
                   if battery >= dist(pos, p) + dist(p, CHARGER) + self.RESERVE]
        if options:
            return ("collect", min(options, key=lambda p: dist(p, pos)))
        if (self.known and battery < MAX_BATTERY) or battery <= dist(pos, CHARGER) + 6:
            return ("recharge",)
        target = (self.rng.randrange(SIZE), self.rng.randrange(SIZE))
        return ("explore", target)

    def act(self, pos, battery, sensed):
        # belief revision: add what is seen, drop packages seen to be gone
        self.known |= sensed
        self.known -= {p for p in self.known if dist(p, pos) <= SENSE and p not in sensed}
        it = self.intention
        achieved = (it is None
                    or (it[0] == "recharge" and battery == MAX_BATTERY)
                    or (it[0] == "collect" and it[1] not in self.known)
                    or (it[0] == "explore" and pos == it[1]))
        unsafe = it is not None and it[0] != "recharge" and battery <= dist(pos, CHARGER) + self.RESERVE
        if achieved or unsafe:
            self.intention = ("recharge",) if unsafe else self.deliberate(pos, battery)
        it = self.intention
        target = CHARGER if it[0] == "recharge" else it[1]
        return step_towards(pos, target)


def run(agent_cls, seed, steps=400):
    rng = random.Random(seed)
    world, agent = World(rng), agent_cls(random.Random(seed + 1))
    pos, battery, collected = CHARGER, MAX_BATTERY, 0
    for _ in range(steps):
        if battery == 0:
            return collected, True
        new = agent.act(pos, battery, world.sensed(pos))
        if new != pos:
            battery -= 1
        pos = new
        if pos == CHARGER:
            battery = MAX_BATTERY
        if world.collect(pos):
            collected += 1
    return collected, False


if __name__ == "__main__":
    print("400 steps per run, 200 runs per agent")
    for cls in (SubsumptionAgent, BDIAgent):
        results = [run(cls, s) for s in range(200)]
        got = [c for c, _ in results]
        dead = sum(d for _, d in results)
        print(f"  {cls.__name__:<17} packages: mean {statistics.mean(got):5.1f}, "
              f"min {min(got):3d}, max {max(got):3d}; ran out of battery: {dead}/200")
