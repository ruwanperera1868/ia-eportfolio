"""Unit 2: first order logic over a small finite world.

Part 1 checks quantified sentences against a model (a domain plus the
facts that hold in it), using all() for "for all" and any() for "exists".
Part 2 derives new facts with forward chaining over definite clauses.
"""

# ---- The model: a domain of objects and the relations that hold ----
domain = {"r1", "r2", "r3", "dock"}
Robot = {"r1", "r2", "r3"}
Charged = {"r1", "r2", "r3"}
CanReach = {("r1", "dock"), ("r2", "dock"), ("r3", "r1")}
Trusts = {("r1", "r2"), ("r2", "r3"), ("r3", "r1")}


def show(sentence, value):
    print(f"  {sentence:<52} {value}")


print("Part 1: model checking quantified sentences")

# ∀x Robot(x) → Charged(x)   "Every robot is charged"
show("∀x Robot(x) → Charged(x)",
     all((x not in Robot) or (x in Charged) for x in domain))

# ∃x Robot(x) ∧ ¬Charged(x)   "Some robot is not charged"
show("∃x Robot(x) ∧ ¬Charged(x)",
     any(x in Robot and x not in Charged for x in domain))

# Common mistake: ∀x Robot(x) ∧ Charged(x) says everything is a charged robot
show("∀x Robot(x) ∧ Charged(x)   (wrong translation)",
     all(x in Robot and x in Charged for x in domain))

# Quantifier order matters
# ∀x ∃y Trusts(x, y)   "Every robot trusts someone"
show("∀x Robot(x) → ∃y Trusts(x, y)",
     all((x not in Robot) or any((x, y) in Trusts for y in domain)
         for x in domain))

# ∃y ∀x Trusts(x, y)   "There is someone every robot trusts"
show("∃y ∀x Robot(x) → Trusts(x, y)",
     any(all((x not in Robot) or (x, y) in Trusts for x in domain)
         for y in domain))

# ---- Part 2: forward chaining ----
# Rules (each variable is universally quantified):
#   Robot(x) ∧ Charged(x) ∧ CanReach(x, dock) → CanDock(x)
#   CanReach(x, y) ∧ CanDock(y) → CanReachDockVia(x, y)
print("\nPart 2: forward chaining")
facts = ({("Robot", x) for x in Robot}
         | {("Charged", x) for x in Charged}
         | {("CanReach", x, y) for x, y in CanReach})

changed = True
round_no = 0
while changed:
    changed = False
    round_no += 1
    new = set()
    for (_, x) in [f for f in facts if f[0] == "Robot"]:
        if ("Charged", x) in facts and ("CanReach", x, "dock") in facts:
            new.add(("CanDock", x))
    for f in [f for f in facts if f[0] == "CanReach"]:
        _, x, y = f
        if ("CanDock", y) in facts:
            new.add(("CanReachDockVia", x, y))
    new -= facts
    if new:
        for f in sorted(new):
            print(f"  round {round_no}: derived {f[0]}({', '.join(f[1:])})")
        facts |= new
        changed = True
print(f"  fixed point reached after {round_no} rounds")
