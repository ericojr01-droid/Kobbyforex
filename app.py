from flask import Flask, request
app = Flask(__name__)
trades = []

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        pair = request.form['pair']
        ttype = request.form['type']
        profit = float(request.form['profit'])
        trades.append({'pair':pair,'type':ttype,'profit':profit})
    
    balance = sum(t['profit'] for t in trades)
    trades_html = ""
    for t in trades[::-1]:
        color = "profit" if t['profit']>=0 else "loss"
        trades_html += f"<div class='card'><b>{t['pair']} - {t['type']}</b><br><span class='{color}'>${t['profit']}</span></div>"
    
    if not trades:
        trades_html = "<p>No trades yet. Add your first trade!</p>"

    return f"""
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font-family:sans-serif; padding:15px; background:#111; color:white}}
input,select,button{{width:100%; padding:12px; margin:6px 0; border-radius:8px; border:none}}
button{{background:#00ff88; font-weight:bold; font-size:16px}}
.card{{background:#222; padding:12px; margin:8px 0; border-radius:10px; border-left:4px solid #00ff88}}
.profit{{color:#00ff88}} .loss{{color:#ff4444}}
h1{{color:#00ff88; text-align:center}}
</style>
</head>
<body>
<h1>KOBBY FX JOURNAL</h1>
<form method="POST">
<input name="pair" placeholder="Pair (e.g EURUSD)" required>
<select name="type"><option>BUY</option><option>SELL</option></select>
<input name="profit" type="number" step="0.01" placeholder="Profit $ e.g 15 or -10" required>
<button type="submit">ADD TRADE</button>
</form>
<h3>Balance: ${round(balance,2)} | Trades: {len(trades)}</h3>
{trades_html}
</body></html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)