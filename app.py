from flask import Flask, request
app = Flask(__name__)
trades = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pair = request.form['pair']
        ttype = request.form['type']
        profit = float(request.form['profit'])
        trades.append({'pair':pair, 'type':ttype, 'profit':profit})

    balance = sum(t['profit'] for t in trades)
    total = len(trades)
    wins = len([t for t in trades if t['profit']>0])
    winrate = round((wins/total*100) if total>0 else 0,1)

    trades_html = ""
    for t in trades[::-1]:
        color = "#00ff88" if t['profit']>=0 else "#ff4444"
        trades_html += f"<div style='background:#1e293b;padding:12px;margin:8px 0;border-radius:10px;display:flex;justify-content:space-between;border-left:4px solid {color}'><span><b>{t['pair']}</b> - {t['type']}</span><span style='color:{color};font-weight:bold'>${t['profit']}</span></div>"

    if not trades:
        trades_html = "<p style='opacity:0.6'>No trades yet. Add your first trade</p>"

    return f"""
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font-family:sans-serif;padding:15px;background:#0f172a;color:white;max-width:600px;margin:auto}}
.card{{background:#1e293b;padding:15px;border-radius:12px;text-align:center}}
.grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:15px 0}}
input,select,button{{width:100%;padding:14px;margin:6px 0;border-radius:10px;border:none;font-size:16px;box-sizing:border-box}}
button{{background:#00ff88;color:black;font-weight:bold;cursor:pointer}}
h1{{color:#00ff88;text-align:center}}
</style>
</head>
<body>
<h1>KOBBY FX DASHBOARD</h1>
<div class="grid">
<div class="card"><small>BALANCE</small><h2>${round(balance,2)}</h2></div>
<div class="card"><small>TRADES</small><h2>{total}</h2></div>
<div class="card"><small>WIN RATE</small><h2>{winrate}%</h2></div>
</div>
<div class="card" style="text-align:left">
<form method="POST">
<input name="pair" placeholder="Pair e.g EURUSD" required>
<select name="type"><option>BUY</option><option>SELL</option></select>
<input name="profit" type="number" step="0.01" placeholder="Profit $ e.g 15 or -10" required>
<button type="submit">+ ADD TRADE</button>
</form>
</div>
<h3>Live Trades</h3>
{trades_html}
</body>
</html>
"""

if __name__ == '__main__':
    app.run()
