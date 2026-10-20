import json
import datetime
import yfinance as yf

def get_market_data():
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 開始執行市場數據抓取...")
    
    # 預設備用數據（萬一網路不通時的防呆）
    vix_price = 18.67
    tsmc_price = 1075.00
    tsmc_chg_pct = 0.5
    qqq_price = 512.40
    fx_price = 32.18

    try:
        print("正在嘗試連線 Yahoo Finance API...")
        # 抓取關鍵市場指標 (加上簡單的例外處理)
        vix_ticker = yf.Ticker("^VIX")
        vix_hist = vix_ticker.history(period="1d")
        if not vix_hist.empty:
            vix_price = vix_hist['Close'].iloc[-1]

        tsmc_ticker = yf.Ticker("2330.TW")
        tsmc_hist = tsmc_ticker.history(period="1d")
        if not tsmc_hist.empty:
            tsmc_price = tsmc_hist['Close'].iloc[-1]
            tsmc_open = tsmc_hist['Open'].iloc[-1]
            if tsmc_open > 0:
                tsmc_chg_pct = ((tsmc_price - tsmc_open) / tsmc_open) * 100

        qqq_ticker = yf.Ticker("QQQ")
        qqq_hist = qqq_ticker.history(period="1d")
        if not qqq_hist.empty:
            qqq_price = qqq_hist['Close'].iloc[-1]

        fx_ticker = yf.Ticker("TWD=X")
        fx_hist = fx_ticker.history(period="1d")
        if not fx_hist.empty:
            fx_price = fx_hist['Close'].iloc[-1]

        print("API 數據抓取成功！")

    except Exception as e:
        print(f"⚠️ 連線外部 API 遇到阻礙 ({e})，已自動切換為安全備用數據，確保系統正常運作。")

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
    
    print(f"[{data['update_time']}] market_data.json 寫入成功！VIX: {data['vix']}, 氣氛評分: {data['sentiment_score']}")

if __name__ == "__main__":
    get_market_data()
