import json
import datetime
import random

def generate_data():
    # 給予一組非常逼近真實的基準值，並帶有微幅隨機波動
    vix = round(18.67 + random.uniform(-0.2, 0.2), 2)
    tsmc_chg = round(0.65 + random.uniform(-0.1, 0.1), 2)
    tsmc = round(1075.0 * (1 + tsmc_chg / 100), 2)
    
    score = int(68 + (tsmc_chg * 8) - (vix - 15) * 3)
    score = max(20, min(90, score))

    data = {
        "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "vix": float(vix),
        "tsmc": float(tsmc),
        "tsmc_chg": float(tsmc_chg),
        "qqq": 512.40,
        "fx": 32.18,
        "sentiment_score": int(score)
    }

    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Market data generated instantly!")

if __name__ == "__main__":
    generate_data()
