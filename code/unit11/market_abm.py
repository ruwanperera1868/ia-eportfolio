"""Unit 11: an agent-based model of a financial market.

Traders set the price of one asset using one of two strategies:
  - fundamentalist: buy when the price is below its fundamental value and
    sell when it is above (pulls the price back);
  - chartist: follow the recent trend (pushes the price further).
In the adaptive version each trader may switch to whichever strategy has
earned more recently, so traders herd. The comparison shows a core idea
of agent-based finance: market-wide booms and busts can emerge from
traders copying whatever strategy is working, with no outside shock
(Lux and Marchesi, 1999; Brock and Hommes, 1998). The model is a toy:
once trend-followers take over, nothing stops the bubble.
"""
import numpy as np

FUNDAMENTAL, STEPS, N = 100.0, 3000, 200


def simulate(adaptive, seed=0, intensity=10_000.0):
    rng = np.random.default_rng(seed)
    is_chartist = rng.random(N) < 0.3
    prices = [FUNDAMENTAL, FUNDAMENTAL]
    profit = np.zeros(2)                     # smoothed profit: [fund, chart]
    shares = []
    for _ in range(STEPS):
        p, p_prev = prices[-1], prices[-2]
        d_fund = 0.05 * (np.log(FUNDAMENTAL) - np.log(p))
        d_chart = 0.02 * np.tanh(100 * (np.log(p) - np.log(p_prev)))   # bounded trend-following
        demand = np.where(is_chartist, d_chart, d_fund) + rng.normal(0, 0.01, N)
        new_p = p * np.exp(demand.mean() + rng.normal(0, 0.002))
        r = np.log(new_p) - np.log(p)
        profit = 0.9 * profit + 0.1 * np.array([d_fund * r, d_chart * r])
        if adaptive:
            # logit switching: chance of being a chartist rises with its edge
            edge = np.clip(intensity * (profit[1] - profit[0]), -50, 50)
            p_chart = 1 / (1 + np.exp(-edge))
            p_chart = min(max(p_chart, 0.05), 0.95)
            switch = rng.random(N) < 0.05    # 5% of traders reconsider each step
            is_chartist[switch] = rng.random(switch.sum()) < p_chart
        shares.append(is_chartist.mean())
        prices.append(new_p)
    prices, shares = np.array(prices[502:]), np.array(shares[500:])   # drop warm-up
    returns = np.diff(np.log(prices))
    a = np.abs(returns)
    clustering = np.corrcoef(a[:-1], a[1:])[0, 1]
    deviation = np.max(np.abs(prices - FUNDAMENTAL)) / FUNDAMENTAL
    chartist_led = np.mean(shares > 0.5)
    return returns.std(), clustering, deviation, chartist_led


if __name__ == "__main__":
    print(f"{'traders':<22} | {'volatility':>10} | {'clustering':>10} | "
          f"{'largest deviation':>17} | time chartist-led")
    for label, adaptive in (("fixed 30% chartists", False), ("adaptive (switching)", True)):
        runs = [simulate(adaptive, seed) for seed in range(20)]
        vol, clus, dev, led = (np.mean(x) for x in zip(*runs))
        print(f"{label:<22} | {vol:>10.4f} | {clus:>10.2f} | {dev:>17.0%} | {led:>17.0%}")
    print("\nMeans of 20 runs. Volatility = standard deviation of log returns per step.")
    print("Clustering = correlation of the size of one return with the next.")
    print("Largest deviation = furthest the price strayed from fundamental value.")
