"""Unit 1: comparing a simple reflex agent with a model-based reflex agent.

Environment: a corridor of N cells, some dirty. The agent perceives only its
own cell (location, dirty?) and can Suck, move Left or move Right.
Agent types follow Russell and Norvig (2021, ch. 2).
"""
import random
import statistics


class Corridor:
    def __init__(self, n_cells, dirt_prob, rng):
        self.dirty = [rng.random() < dirt_prob for _ in range(n_cells)]
        self.pos = rng.randrange(n_cells)

    def percept(self):
        return self.pos, self.dirty[self.pos]

    def act(self, action):
        if action == "Suck":
            self.dirty[self.pos] = False
        elif action == "Left":
            self.pos = max(0, self.pos - 1)
        elif action == "Right":
            self.pos = min(len(self.dirty) - 1, self.pos + 1)

    def clean(self):
        return not any(self.dirty)


class SimpleReflexAgent:
    """Condition-action rules on the current percept only; no memory."""

    def __init__(self, rng):
        self.rng = rng

    def __call__(self, percept):
        _, dirty = percept
        if dirty:
            return "Suck"
        return self.rng.choice(["Left", "Right"])


class ModelBasedAgent:
    """Keeps an internal model of which cells it has seen clean,
    and heads for the nearest cell it has not yet visited."""

    def __init__(self, n_cells):
        self.unvisited = set(range(n_cells))

    def __call__(self, percept):
        pos, dirty = percept
        self.unvisited.discard(pos)
        if dirty:
            return "Suck"
        if not self.unvisited:
            return "NoOp"
        target = min(self.unvisited, key=lambda c: abs(c - pos))
        return "Left" if target < pos else "Right"


def run(make_agent, n_cells, seed, max_steps=1000):
    rng = random.Random(seed)
    env = Corridor(n_cells, dirt_prob=0.5, rng=rng)
    agent = make_agent(rng, n_cells)
    for step in range(max_steps):
        if env.clean():
            return step
        env.act(agent(env.percept()))
    return max_steps


if __name__ == "__main__":
    agents = {
        "Simple reflex": lambda rng, n: SimpleReflexAgent(rng),
        "Model-based reflex": lambda rng, n: ModelBasedAgent(n),
    }
    for n_cells in (5, 10, 20):
        print(f"Corridor of {n_cells} cells, 200 trials")
        for name, factory in agents.items():
            steps = [run(factory, n_cells, seed) for seed in range(200)]
            print(f"  {name:<20} mean steps to clean: {statistics.mean(steps):6.1f}"
                  f"  worst: {max(steps)}")
