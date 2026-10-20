import json
import datetime
import time  # 1. 引入 time 模組
import yfinance as yf

def get_market_data():
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在向市場 API 抓取最新數據...")
    try:
        vix_ticker = yf.Ticker("^VIX")
        tsmc_ticker = yf.Ticker("2330.TW")
        qqq_ticker = yf.Ticker("QQQ")
        fx_ticker = yf.Ticker("TWD=X")

        vix_price = vix_ticker.history(period="1d")['Close'].iloc[-1]
        tsmc_data = tsmc_ticker.history(period="1d")
        tsmc_price = tsmc_data['Close'].iloc[-1]
        tsmc_open = tsmc_data['Open'].iloc[-1]
        tsmc_chg_pct = ((tsmc_price - tsmc_open) / tsmc_open) * 100

        qqq_price = qqq_ticker.history(period="1d")['Close'].iloc[-1]
        fx_price = fx_ticker.history(period="1d")['Close'].iloc[-1]

        base_score = 68
        score = int(base_score + (tsmc_chg_pct * 8) - (vix_price - 15) * 3)
        score = max(15, min(95, score))

        data = {
            "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "vix": round(float(vix_price), 2),
            "tsmc": round(float(tsmc_price), 2),
            "tsmc_chg": round(float(tsmc_chg_pct), 2),
            "qqq": round(float(qqq_price), 2),
            "fx": round(float(fx_price), 2),
            "sentiment_score": score
        }

        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"[{data['update_time']}] 數據更新成功！VIX: {data['vix']}, 氣氛評分: {data['sentiment_score']}\n")

    except Exception as e:
        print(f"抓取資料發生錯誤: {e}\n")

if __name__ == "__main__":
    print("==================================================")
    print(" 已啟動自動監控排程：每 5 分鐘自動抓取一次市場數據")
    print(" 提示：若要關閉程式，請隨時在終端機按 [Ctrl + C]")
    print("==================================================\n")
    
    # 2. 用 while True 讓程式持續運行
    while True:
        get_market_data()
        print("等待 5 分鐘後進行下一次更新...")
        time.sleep(300)  # 暫停 300 秒（5 分鐘）