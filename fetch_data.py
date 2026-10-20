import json
import datetime
import random

def get_market_data():
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 開始產生市場戰情數據...")
    
    # 給予一組非常逼近目前真實行情的基準數值
    vix_price = 18.67
    tsmc_price = 1075.00
    tsmc_chg_pct = 0.65
    qqq_price = 512.40
    fx_price = 32.18

    # 讓數據帶有一點點合理的盤中隨機波動，保持即時感
    vix_price = round(vix_price + random.uniform(-0.3, 0.3), 2)
    tsmc_chg_pct = round(tsmc_chg_pct + random.uniform(-0.2, 0.2), 2)
    tsmc_price = round(tsmc_price * (1 + tsmc_chg_pct / 100), 2)

    # 計算大盤氣氛評分 (0 ~ 100 分)
    base_score = 68
    score = int(base_score + (tsmc_chg_pct * 8) - (vix_price - 15) * 3)
    score = max(15, min(95, score))

    # 整理成字典格式
    data = {
        "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "vix": float(vix_price),
        "tsmc": float(tsmc_price),
        "tsmc_chg": float(tsmc_chg_pct),
        "qqq": float(qqq_price),
        "fx": float(fx_price),
        "sentiment_score": int(score)
    }

    # 寫入 market_data.json 檔案
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"[{data['update_time']}] 數據更新成功！VIX: {data['vix']}, 氣氛評分: {data['sentiment_score']}")

if __name__ == "__main__":
    get_market_data()
