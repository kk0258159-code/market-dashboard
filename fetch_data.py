import json
import datetime
import yfinance as yf

def get_market_data():
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在向市場 API 抓取最新數據...")
    try:
        # 抓取關鍵市場指標
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

        # 計算大盤氣氛評分 (0 ~ 100 分)
        base_score = 68
        score = int(base_score + (tsmc_chg_pct * 8) - (vix_price - 15) * 3)
        score = max(15, min(95, score))

        # 整理成字典格式
        data = {
            "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "vix": round(float(vix_price), 2),
            "tsmc": round(float(tsmc_price), 2),
            "tsmc_chg": round(float(tsmc_chg_pct), 2),
            "qqq": round(float(qqq_price), 2),
            "fx": round(float(fx_price), 2),
            "sentiment_score": score
        }

        # 寫入 market_data.json 檔案
        with open("market_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"[{data['update_time']}] 數據更新成功並已寫入 JSON！VIX: {data['vix']}, 氣氛評分: {data['sentiment_score']}")

    except Exception as e:
        print(f"抓取資料發生錯誤: {e}")

if __name__ == "__main__":
    # 單次執行（配合 GitHub Actions 排程，由雲端定時觸發）
    get_market_data()
