#!/usr/bin/env python3
"""
KOMBINATOR — MODUL 1: MATEMATYK
Copyright 2026 Tom Jeziorski. Trade Secret.
Probabilistyka, optymalizacja, Kelly Criterion, Monte Carlo
"""
import random, math, json

class Matematyk:
    NAME = "MATEMATYK"
    ICON = "🧮"
    VERSION = "2.0"
    
    def __init__(self):
        self.calculations = 0
    
    def kelly_criterion(self, win_prob, win_ratio, loss_ratio=1.0):
        q = 1 - win_prob
        b = win_ratio / loss_ratio
        f = (b * win_prob - q) / b
        self.calculations += 1
        return {"kelly_fraction": round(max(0, f), 4), "half_kelly": round(max(0, f/2), 4),
                "expected_value": round(win_prob * win_ratio - q * loss_ratio, 4),
                "action": "INWESTUJ" if f > 0 else "NIE_INWESTUJ", "edge_pct": round(f * 100, 2)}
    
    def monte_carlo(self, capital, strategies, iterations=10000):
        results = []
        for _ in range(iterations):
            c = capital
            for s in strategies:
                if random.random() < s.get("win_prob", 0.5):
                    c += c * s.get("win_pct", 0.05) * s.get("kelly", 0.1)
                else:
                    c -= c * s.get("loss_pct", 0.03) * s.get("kelly", 0.1)
            results.append(c)
        results.sort()
        self.calculations += iterations
        return {"median": round(results[len(results)//2], 2), "mean": round(sum(results)/len(results), 2),
                "p5_worst": round(results[int(len(results)*0.05)], 2),
                "p95_best": round(results[int(len(results)*0.95)], 2),
                "profit_prob_pct": round(len([r for r in results if r > capital])/len(results)*100, 1),
                "ruin_prob_pct": round(len([r for r in results if r < capital*0.1])/len(results)*100, 2)}
    
    def compound_growth(self, capital, monthly_rate, months, contrib=0):
        timeline = []
        c = capital
        for m in range(1, months+1):
            c = (c + contrib) * (1 + monthly_rate)
            timeline.append({"month": m, "capital": round(c, 2)})
        return timeline
    
    def arbitrage_calc(self, buy_price, sell_price, fee_pct=0.2):
        fee = (buy_price + sell_price) * fee_pct / 100
        net = sell_price - buy_price - fee
        roi = (net / buy_price) * 100 if buy_price > 0 else 0
        return {"buy": buy_price, "sell": sell_price, "fees": round(fee, 4),
                "net_profit": round(net, 4), "roi_pct": round(roi, 4), "profitable": net > 0}
    
    def optimize_portfolio(self, assets):
        total_ev = sum(a.get("ev", 0) for a in assets)
        if total_ev <= 0:
            return {"allocation": [], "status": "NO_POSITIVE_EV"}
        alloc = [{"asset": a["name"], "weight_pct": round(max(0, a.get("ev",0)/total_ev)*100, 2),
                  "ev": a.get("ev", 0)} for a in assets]
        alloc.sort(key=lambda x: x["weight_pct"], reverse=True)
        return {"allocation": alloc, "total_ev": round(total_ev, 4)}
    
    def risk_matrix(self, strategies):
        matrix = []
        for s in strategies:
            ev = s.get("win_prob",0.5)*s.get("win_amt",0) - (1-s.get("win_prob",0.5))*s.get("loss_amt",0)
            sharpe = ev / max(s.get("vol", 1), 0.01)
            matrix.append({"strategy": s["name"], "ev": round(ev, 2), "sharpe": round(sharpe, 3),
                          "risk": "LOW" if sharpe > 1 else "MED" if sharpe > 0.3 else "HIGH",
                          "recommend": sharpe > 0.3})
        matrix.sort(key=lambda x: x["sharpe"], reverse=True)
        return matrix
    
    def report_to(self, coordinator):
        return {"module": self.NAME, "icon": self.ICON, "calculations": self.calculations, "status": "ACTIVE"}

if __name__ == "__main__":
    m = Matematyk()
    print(f"\n{m.ICON} === {m.NAME} v{m.VERSION} ===")
    print(f"Kelly: {m.kelly_criterion(0.6, 2.0)}")
    print(f"Monte Carlo: {json.dumps(m.monte_carlo(1000, [{'win_prob':0.55,'win_pct':0.08,'loss_pct':0.04,'kelly':0.15}], 5000), indent=2)}")
    print(f"Arbitraz: {m.arbitrage_calc(100.0, 103.5)}")
    print(f"Obliczenia: {m.calculations}")
