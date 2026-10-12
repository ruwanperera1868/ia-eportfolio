"""Unit 4: adding a reactive safety layer to the Unit 3 BDI agent.

Same delivery world as Unit 3, plus four hazards (e.g. people or forklifts)
that move one random step each turn. Hitting a hazard counts as a collision
and drains 5 battery. The BDI agent plans as before and ignores hazards.
In the hybrid agent the BDI layer proposes a move and a reactive layer can
override it, vetoing any move onto or next to a hazard and picking the
safest alternative instead. Detours cost battery the plan did not
expect, so the hybrid keeps a larger battery reserve; HybridNoReserve shows
what happens when the layers are combined without that adjustment.
"""
import os
import random
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "unit3"))
from architectures import (BDIAgent, CHARGER, MAX_BATTERY, SIZE, World,  # noqa: E402
                           dist)

N_HAZARDS, COLLISION_COST = 4, 5


def neighbours(pos):
    x, y = pos
    return [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
            if 0 <= x + dx < SIZE and 0 <= y + dy < SIZE]


class HybridAgent(BDIAgent):
    """Deliberative layer: inherited BDI reasoning (what to do).
    Reactive layer: hazard avoidance that can override a single move."""

    RESERVE = 6

    def act(self, pos, battery, sensed, hazards=()):
        planned = super().act(pos, battery, sensed)

        def danger(cell):
            return sum(1 for h in hazards if dist(cell, h) <= 1)

        if danger(planned) == 0:
            return planned
        # reactive override: safest cell, ties broken by progress to the plan
        it = self.intention
        goal = CHARGER if it[0] == "recharge" else it[1]
        return min(neighbours(pos) + [pos],
                   key=lambda c: (c in hazards, danger(c), dist(c, goal)))


class HybridNoReserve(HybridAgent):
    RESERVE = 1


def run(agent_cls, seed, steps=400):
    rng = random.Random(seed)
    world, agent = World(rng), agent_cls(random.Random(seed + 1))
    hazards = [(rng.randrange(2, SIZE), rng.randrange(2, SIZE)) for _ in range(N_HAZARDS)]
    pos, battery, collected, collisions = CHARGER, MAX_BATTERY, 0, 0
    for _ in range(steps):
        if battery <= 0:
            return collected, collisions, True
        if isinstance(agent, HybridAgent):
            new = agent.act(pos, battery, world.sensed(pos), hazards)
        else:
            new = agent.act(pos, battery, world.sensed(pos))
        if new != pos:
            battery -= 1
        pos = new
        hazards = [rng.choice(neighbours(h)) for h in hazards]
        if pos in hazards:
            collisions += 1
            battery -= COLLISION_COST
        if pos == CHARGER:
            battery = MAX_BATTERY
        if world.collect(pos):
            collected += 1
    return collected, collisions, False


if __name__ == "__main__":
    print(f"400 steps per run, 200 runs per agent, {N_HAZARDS} moving hazards")
    for cls in (BDIAgent, HybridNoReserve, HybridAgent):
        results = [run(cls, s) for s in range(200)]
        got = [r[0] for r in results]
        hits = [r[1] for r in results]
        dead = sum(r[2] for r in results)
        print(f"  {cls.__name__:<15} packages: mean {statistics.mean(got):5.1f}; "
              f"collisions: mean {statistics.mean(hits):4.1f}, max {max(hits):2d}; "
              f"ran out of battery: {dead}/200")

    print("\nHybrid agent: effect of the battery reserve")
    for reserve in (1, 4, 6, 10, 15, 20):
        cls = type(f"Hybrid{reserve}", (HybridAgent,), {"RESERVE": reserve})
        results = [run(cls, s) for s in range(200)]
        print(f"  reserve {reserve:2d}: packages mean {statistics.mean(r[0] for r in results):5.1f}; "
              f"ran out of battery: {sum(r[2] for r in results)}/200")
