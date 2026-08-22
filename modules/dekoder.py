#!/usr/bin/env python3
"""
KOMBINATOR — MODUL 5: DEKODER
Copyright 2026 Tom Jeziorski. Trade Secret.
Analiza danych, pattern recognition, market decoding, signal detection
"""
import json, random

class Dekoder:
    NAME = "DEKODER"
    ICON = "🔍"
    VERSION = "2.0"
    
    def __init__(self):
        self.patterns_found = 0
        self.signals_decoded = 0
        self.data_processed_kb = 0
    
    def analyze_market(self, prices):
        if len(prices) < 3:
            return {"error": "Za malo danych (min 3 ceny)"}
        avg = sum(prices) / len(prices)
        trend = "UP" if prices[-1] > prices[0] else "DOWN" if prices[-1] < prices[0] else "FLAT"
        vol_pct = (max(prices) - min(prices)) / avg * 100 if avg > 0 else 0
        momentum = (prices[-1] - prices[-3]) / prices[-3] * 100
        sma3 = sum(prices[-3:]) / 3
        signal = "BUY" if sma3 > avg and trend == "UP" else "SELL" if sma3 < avg and trend == "DOWN" else "HOLD"
        self.patterns_found += 1
        self.signals_decoded += 1
        return {"trend": trend, "avg": round(avg, 2), "volatility_pct": round(vol_pct, 2),
                "momentum_pct": round(momentum, 2), "sma3": round(sma3, 2),
                "signal": signal, "confidence": round(min(95, 50 + abs(momentum)*2), 1)}
    
    def detect_arbitrage(self, exchange_prices):
        opportunities = []
        exchanges = list(exchange_prices.keys())
        for i in range(len(exchanges)):
            for j in range(i+1, len(exchanges)):
                e1, e2 = exchanges[i], exchanges[j]
                p1, p2 = exchange_prices[e1], exchange_prices[e2]
                diff = abs(p1 - p2) / min(p1, p2) * 100
                if diff > 0.3:
                    buy_ex = e1 if p1 < p2 else e2
                    sell_ex = e2 if p1 < p2 else e1
                    opportunities.append({"buy": buy_ex, "sell": sell_ex,
                                          "spread_pct": round(diff, 3), "net_pct": round(diff - 0.4, 3)})
                    self.patterns_found += 1
        return {"opportunities": opportunities, "count": len(opportunities)}
    
    def decode_pattern(self, data_series):
        patterns = []
        for i in range(len(data_series) - 2):
            a, b, c = data_series[i], data_series[i+1], data_series[i+2]
            if a < b > c: patterns.append({"type": "PEAK", "index": i+1, "value": b})
            if a > b < c: patterns.append({"type": "VALLEY", "index": i+1, "value": b})
        self.patterns_found += len(patterns)
        return {"patterns": patterns, "count": len(patterns)}
    
    def sentiment_score(self, text):
        pos_words = ["zysk","wzrost","bull","moon","profit","dobry","sukces","bonus"]
        neg_words = ["strata","spadek","bear","crash","loss","ryzyko","krach"]
        words = text.lower().split()
        pos = sum(1 for w in words if any(p in w for p in pos_words))
        neg = sum(1 for w in words if any(n in w for n in neg_words))
        total = pos + neg
        score = ((pos - neg) / total * 100) if total > 0 else 0
        self.signals_decoded += 1
        return {"score": round(score, 1), "positive": pos, "negative": neg,
                "sentiment": "BULLISH" if score > 20 else "BEARISH" if score < -20 else "NEUTRAL"}
    
    def frequency_analysis(self, data):
        from collections import Counter
        counts = Counter(data)
        freq = [{"value": k, "count": v, "pct": round(v/len(data)*100, 2)} for k, v in counts.most_common(10)]
        return {"top_items": freq, "unique": len(counts), "total": len(data)}
    
    def report_to(self, coordinator):
        return {"module": self.NAME, "icon": self.ICON, "patterns": self.patterns_found,
                "signals": self.signals_decoded, "status": "ACTIVE"}

if __name__ == "__main__":
    d = Dekoder()
    print(f"\n{d.ICON} === {d.NAME} v{d.VERSION} ===")
    print(f"Market: {json.dumps(d.analyze_market([100,102,99,105,108,107,112]), indent=2)}")
    print(f"Arbitrage: {json.dumps(d.detect_arbitrage({'Binance':67500,'Kraken':67850,'Coinbase':67200}), indent=2)}")
