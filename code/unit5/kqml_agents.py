"""Unit 5: two agents talking in KQML over a shared ontology.

A buyer agent asks a warehouse agent about stock. Messages are written in
KQML syntax: a performative (the speech act) followed by :keyword value
parameters. The :ontology parameter names the vocabulary both agents must
share for :content to mean the same thing to each of them.
"""
import re

# ---- A tiny ontology: classes, their parents, and properties ----
WAREHOUSE_ONTOLOGY = {
    "name": "warehouse-v1",
    "classes": {"Item": None, "Electronics": "Item", "Laptop": "Electronics",
                "Phone": "Electronics", "Furniture": "Item", "Desk": "Furniture"},
    "properties": {"stock": "Item", "price": "Item"},
}


def is_a(ontology, cls, ancestor):
    while cls is not None:
        if cls == ancestor:
            return True
        cls = ontology["classes"].get(cls)
    return False


# ---- KQML messages ----
def kqml(performative, **params):
    body = " ".join(f":{k.replace('_', '-')} {v}" for k, v in params.items())
    return f"({performative} {body})"


def parse(message):
    m = re.fullmatch(r"\((\S+)\s+(.*)\)", message.strip(), re.S)
    performative, rest = m.group(1), m.group(2)
    params = dict(re.findall(r":(\S+)\s+(\([^)]*\)|\S+)", rest))
    return performative, params


class WarehouseAgent:
    def __init__(self, name, ontology):
        self.name, self.ontology = name, ontology
        self.beliefs = {("stock", "Laptop"): 12, ("stock", "Phone"): 0,
                        ("price", "Laptop"): 899, ("stock", "Desk"): 4}

    def receive(self, message):
        perf, p = parse(message)
        reply = dict(sender=self.name, receiver=p["sender"], in_reply_to=p["reply-with"])
        if p.get("ontology") != self.ontology["name"]:
            return kqml("sorry", **reply, comment='"unknown ontology"')
        prop, cls = p["content"].strip("()").split()
        if prop not in self.ontology["properties"] or cls not in self.ontology["classes"]:
            return kqml("sorry", **reply, comment=f'"{cls} or {prop} not in ontology"')
        if perf == "ask-one":
            if (prop, cls) in self.beliefs:
                return kqml("tell", **reply, language="KIF", ontology=self.ontology["name"],
                            content=f"(= ({prop} {cls}) {self.beliefs[(prop, cls)]})")
            # use the ontology: answer about a class by summing its subclasses
            parts = [v for (pr, c), v in self.beliefs.items()
                     if pr == prop and is_a(self.ontology, c, cls)]
            if parts and prop == "stock":
                return kqml("tell", **reply, language="KIF", ontology=self.ontology["name"],
                            content=f"(= ({prop} {cls}) {sum(parts)})")
            return kqml("sorry", **reply, comment='"no belief"')
        if perf == "achieve" and prop == "stock":
            self.beliefs[(prop, cls)] = self.beliefs.get((prop, cls), 0) + 10
            return kqml("tell", **reply, language="KIF", ontology=self.ontology["name"],
                        content=f"(= ({prop} {cls}) {self.beliefs[(prop, cls)]})")
        return kqml("error", **reply, comment=f'"cannot handle {perf}"')


class BuyerAgent:
    def __init__(self, name, ontology_name):
        self.name, self.ontology_name, self.counter = name, ontology_name, 0

    def ask(self, performative, receiver, content):
        self.counter += 1
        return kqml(performative, sender=self.name, receiver=receiver,
                    reply_with=f"q{self.counter}", language="KIF",
                    ontology=self.ontology_name, content=content)


def converse(buyer, warehouse, performative, content):
    msg = buyer.ask(performative, warehouse.name, content)
    print(f"  {buyer.name} -> {msg}")
    print(f"  {warehouse.name} -> {warehouse.receive(msg)}\n")


if __name__ == "__main__":
    wh = WarehouseAgent("warehouse", WAREHOUSE_ONTOLOGY)
    buyer = BuyerAgent("buyer", "warehouse-v1")
    print("1. Direct query answered from beliefs")
    converse(buyer, wh, "ask-one", "(stock Laptop)")
    print("2. Query about a superclass, answered by reasoning over the ontology")
    converse(buyer, wh, "ask-one", "(stock Electronics)")
    print("3. A term outside the shared ontology")
    converse(buyer, wh, "ask-one", "(stock Tablet)")
    print("4. A request to act (achieve) rather than to inform")
    converse(buyer, wh, "achieve", "(stock Phone)")
    print("5. Same words, different ontology: communication fails")
    converse(BuyerAgent("buyer2", "retail-v2"), wh, "ask-one", "(stock Laptop)")
