import os
import requests
from datetime import datetime, timezone

CMC_API_KEY = os.getenv("CMC_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

CMC_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

def format_money(value):
if value >= 1_000_000_000:
return f"${value / 1_000_000_000:.2f}B"
if value >= 1_000_000:
return f"${value / 1_000_000:.2f}M"
if value >= 1_000:
return f"${value / 1_000:.2f}K"
return f"${value:.2f}"

def format_price(price):
if price >= 1:
return f"${price:,.4f}"
return f"${price:.8f}".rstrip("0").rstrip(".")

def get_top_volume_gainers():
headers = {
"X-CMC_PRO_API_KEY": CMC_API_KEY,
"Accept": "application/json",
}

```
params = {
    "start": "1",
    "limit": "300",
    "convert": "USD",
    "sort": "market_cap",
    "sort_dir": "desc",
}

response = requests.get(CMC_URL, headers=headers, params=params, timeout=30)
response.raise_for_status()

data = response.json()["data"]
coins = []

for coin in data:
    quote = coin["quote"]["USD"]

    volume_change = quote.get("volume_change_24h")
    volume_24h = quote.get("volume_24h", 0)
    market_cap = quote.get("market_cap", 0)

    if volume_change is None:
        continue

    # ФИЛЬТР ОБЪЕМА > $10M
    if volume_24h < 10_000_000:
        continue

    coins.append({
        "symbol": coin["symbol"],
        "name": coin["name"],
        "price": quote["price"],
        "volume_change_24h": volume_change,
        "volume_24h": volume_24h,
        "market_cap": market_cap,
        "price_change_24h": quote.get("percent_change_24h"),
    })

return sorted(
    coins,
    key=lambda x: x["volume_change_24h"],
    reverse=True
)[:5]
```

def build_message(coins):
now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

```
message = (
    "📈 Топ 5 токенов по росту объема торгов\n\n"
    "Топ-300 CoinMarketCap | Объем > $10M\n"
    f"Обновлено: {now}\n\n"
)

for i, coin in enumerate(coins, start=1):
    message += (
        f"{i}. {coin['symbol']} — {coin['name']}\n"
        f"📊 Рост объема: +{coin['volume_change_24h']:.2f}%\n"
        f"💵 Объем 24ч: {format_money(coin['volume_24h'])}\n"
        f"🏦 Market Cap: {format_money(coin['market_cap'])}\n"
        f"💰 Цена: {format_price(coin['price'])}\n"
        f"📈 Изм. цены: {coin['price_change_24h']:.2f}%\n\n"
    )

return message
```

def send_telegram_message(text):
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

```
payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": text
}

response = requests.post(url, json=payload, timeout=30)
response.raise_for_status()
```

def main():
coins = get_top_volume_gainers()
message = build_message(coins)
send_telegram_message(message)

if **name** == "**main**":
main()
