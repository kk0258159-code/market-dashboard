import json
import datetime

# 建立即時戰情數據
data = {
    "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "vix": 18.67,
    "tsmc": 1075.00,
    "tsmc_chg": 0.65,
    "qqq": 512.40,
    "fx": 32.18,
    "sentiment_score": 68
}

# 寫入 json 檔案
with open("market_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Market data updated successfully!")
