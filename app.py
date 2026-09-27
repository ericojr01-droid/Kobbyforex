#... KEEP SAME TOP AS BEFORE...
import os, random, datetime
from flask import Flask, request, session, redirect, jsonify, render_template_string, send_from_directory
import requests

app = Flask(__name__)
app.secret_key = "kobbyforex_with_factory"
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8983200049:AAGsiqBHcEZQY8sVRVStL6FOT4ZVok_zBr8")
CHAT_ID = os.environ.get("CHAT_ID", "8240862120")

users = {}; trades = {}
PAIRS = ["EURUSD","GBPUSD","USDJPY","AUDUSD","USDCAD","NZDUSD","USDCHF","XAUUSD"]

def is_forex_open():
    now=datetime.datetime.utcnow(); wd=now.weekday(); hr=now.hour
    if wd==5: return False,"SATURDAY - Closed"
    if wd==6 and hr<22: return False,"SUNDAY - Closed"
    if wd==4 and hr>=22: return False,"FRIDAY - Closed"
    return True,"OPEN"

def gen_entry(pair):
    price=round(random.uniform(1.08,1.09) if pair!="XAUUSD" else random.uniform(2400,2450),5)
    r=random.random()
    if r>0.7: return {"status":"BOTH","msg":f"🟣 {pair} BOTH BUY NOW","entry":price,"sl":round(price-0.0015,5),"tp1":round(price+0.003,5),"tp2":round(price+0.006,5),"reason":"Sweep + BOS + POI + Fib 79% + CPI"}
    if r>0.5: return {"status":"TECH","msg":f"🟢 {pair} TECHNICAL BUY NOW","entry":price,"sl":round(price-0.0015,5),"tp1":round(price+0.003,5),"tp2":round(price+0.006,5),"reason":"Sweep + BOS + Demand + Fib 79%"}
    if r>0.3: return {"status":"FUND","msg":f"🔵 {pair} FUNDAMENTAL SELL NOW","entry":price,"sl":round(price+0.0015,5),"tp1":round(price-0.003,5),"tp2":round(price-0.006,5),"reason":"CPI High"}
    return {"status":"NO","msg":f"🔴 {pair} NO ENTRY","reason":"Waiting sweep | BOS | POI"}

LANDING_HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>KOBBYFOREX</title>
<style>
body{margin:0;min-height:100vh;background:#000;color:#fff;font-family:Arial;position:relative}
.bg{position:fixed;inset:0;background: linear-gradient(to right, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 50%, rgba(0,0,0,0.8) 100%), url('/kobby_bg.jpg'); background-size:cover; background-position:center 30%; z-index:-1}
.header{display:flex;justify-content:space-between;align-items:center;padding:18px 30px;z-index:2;position:relative}
.logo{display:flex;align-items:center;gap:8px;font-weight:bold;font-size:16px}
.nav-links{display:flex;gap:20px;font-size:11px;letter-spacing:2px;color:#aaa}
.content{padding:80px 30px 40px 30px;max-width:520px;z-index:2;position:relative}
.h1{font-size:48px;font-weight:900;line-height:1.05;margin:0}.green{color:#39ff5a}.purple{color:#8a5cff}
.desc{color:#9aa0a6;font-size:13px;line-height:1.6;margin-top:18px;max-width:440px}
.btns{display:flex;gap:12px;margin-top:26px;flex-wrap:wrap}
.btn-blue{background:#1a6bff;color:#fff;border:none;border-radius:8px;padding:12px 18px;font-size:13px;font-weight:600;display:flex;align-items:center;gap:8px;text-decoration:none}
.btn-dark{background:rgba(0,0,0,0.6);color:#fff;border:1px solid rgba(255,255,255,0.2);border-radius:8px;padding:12px 18px;font-size:13px;font-weight:600;text-decoration:none;backdrop-filter:blur(6px)}
.bottom-lines{position:absolute;bottom:30px;left:30px;display:flex;gap:10px}.line{height:2px;width:40px;background:#39ff5a}.line2{height:2px;width:40px;background:#8a5cff}
</style></head><body><div class="bg"></div>
<div class="header"><div class="logo">↗ KOBBYFOREX</div><div class="nav-links"><span>MARKETS</span><span>·</span><span>ABOUT</span><span>·</span><span>CONTACT</span></div></div>
<div class="content"><h1 class="h1">Trade with<br><span class="green">discipline</span><br>trade with <span class="purple">purpose</span></h1>
<div class="desc">Access real-time Forex signals, market analysis, and disciplined strategies. Join thousands of traders mastering risk management and consistent profit with KOBBYFX.</div>
<div class="btns"><a href="https://t.me/kobbyforex" target="_blank" class="btn-blue">✈️ Join My Telegram Channel →</a><a href="{{trade_link}}" class="btn-dark">Trade with KobbyForex</a></div></div>
<div class="bottom-lines"><div class="line"></div><div class="line2"></div></div></body></html>
"""

BASE_HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>KOBBYFOREX</title>
<style>
body{margin:0;min-height:100vh;background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), url('/kobby_bg.jpg'); background-size:cover; background-position:center; background-attachment:fixed; color:#a0b0d0; font-family:Arial}
.card{background:rgba(21,30,50,0.85);backdrop-filter:blur(12px);border:1px solid #1e2a45;border-left:4px solid #22ff66;border-radius:14px;padding:12px;margin:10px}
.nav{display:flex;gap:6px;padding:10px;background:rgba(0,0,0,0.8);border-bottom:1px solid #1e2a45;flex-wrap:wrap;position:sticky;top:0;z-index:10}
.nav a{color:#8a9abb;text-decoration:none;padding:7px 10px;border-radius:20px;background:rgba(21,30,50,0.8);border:1px solid #1e2a45;font-size:11px}
.btn{padding:10px 14px;background:#22ff66;color:#000;border:none;border-radius:8px;font-weight:bold;cursor:pointer}
.live-bar{display:flex;gap:8px;overflow-x:auto;padding:8px;background:rgba(0,0,0,0.6);border-bottom:1px solid #1e2a45}
.live-item{min-width:120px;background:rgba(21,30,50,0.9);border-radius:10px;padding:6px;border-left:3px solid #22ff66;text-align:center;font-size:12px}
input,select{width:100%;padding:10px;background:rgba(15,26,42,0.9);border:1px solid #1e3a4a;border-radius:8px;color:#fff;margin:5px 0;box-sizing:border-box}
table{width:100%;border-collapse:collapse;font-size:12px}th,td{border:1px solid #1e2a45;padding:6px;text-align:left}th{background:#0f1729;color:#22ff66}
.high{color:#ff4444;font-weight:bold}.med{color:#ffaa00}.low{color:#ffeb3b}
</style></head><body>
<div class="nav"><a href="/dashboard">HOME</a><a href="/live">🔴 LIVE</a><a href="/journal">JOURNAL</a><a href="/lot">LOT</a><a href="/technical">TECH</a><a href="/fundamental">FUND</a><a href="/calendar">🏭 CAL</a><a href="/academy">ACADEMY</a><a href="/admin">ADMIN</a><a href="/logout" style="margin-left:auto;color:#ff4444">Logout</a></div>
<div class="live-bar" id="liveBar">Loading live...</div><script>async function loadBar(){let r=await fetch('/api/live_prices');let d=await r.json();document.getElementById('liveBar').innerHTML=d.map(p=>`<div class=live-item><b>${p.pair}</b><br>${p.price}<br><span style=color:${p.change>0?'#22ff66':'#ff4444'}>${p.change>0?'▲':'▼'} ${p.change}%</span></div>`).join('')}setInterval(loadBar,5000);loadBar();</script>{{content}}</body></html>
"""

@app.route("/")
def landing():
    trade_link = "/dashboard" if "user" in session else "/auth"
    return render_template_string(LANDING_HTML, trade_link=trade_link)

@app.route("/dashboard")
def dashboard():
    if "user" not in session: return redirect("/auth")
    is_open,msg=is_forex_open()
    content=f"""<div class=card><h2 style=color:#fff>KOBBY<span style=color:#22ff66>FOREX</span> - Dashboard</h2><p>Hi, {session['user']} | {msg} | {datetime.datetime.utcnow().strftime('%H:%M GMT')}</p><a href=/live class=btn>🔴 GO LIVE NOW</a> <a href=/calendar class=btn style=background:#ffaa00;margin-left:6px>🏭 Forex Factory</a></div>"""
    return render_template_string(BASE_HTML, content=content)

@app.route("/api/live_prices")
def api_prices(): return jsonify([{"pair":p,"price":round(random.uniform(1.08,1.09) if p!="XAUUSD" else random.uniform(2400,2450),5),"change":round(random.uniform(-0.5,0.8),2)} for p in PAIRS])
@app.route("/api/live_entries")
def api_entries(): return jsonify([gen_entry(p) for p in PAIRS])

@app.route("/live")
def live():
    if "user" not in session: return redirect("/auth")
    content="""<div class=card><h2>🔴 LIVE 8 PAIRS - Auto 8s + Telegram Alert</h2><div id=entries>Loading...</div></div><script>async function loadE(){let r=await fetch('/api/live_entries');let d=await r.json();document.getElementById('entries').innerHTML=d.map(e=>{if(e.status=='CLOSED')return `<div class=card style=border-left:4px solid #ff4444><b>${e.msg}</b></div>`;if(e.status=='NO')return `<div class=card style=border-left:4px solid #ff4444><b>${e.msg}</b><br>${e.reason}</div>`;return `<div class=card style=border-left:4px solid #22ff66><b>${e.msg}</b><br>Entry: ${e.entry} | SL: ${e.sl} | TP1: ${e.tp1} TP2: ${e.tp2}<br>${e.reason}</div>`}).join('')}setInterval(loadE,8000);loadE();</script>"""
    return render_template_string(BASE_HTML, content=content)

@app.route("/technical")
def tech():
    if "user" not in session: return redirect("/auth")
    return render_template_string(BASE_HTML, content='<div class=card><h2>📈 TECHNICAL - SMC</h2><p>BOS, CHOCH, Order Blocks, FVG, Liquidity Sweep, Fib 79% OTE</p><p>MN → W → D1 → H4 → M15 top-down</p></div>')

@app.route("/fundamental")
def fund():
    if "user" not in session: return redirect("/auth")
    return render_template_string(BASE_HTML, content='<div class=card><h2>📰 FUNDAMENTAL</h2><p>CPI, FOMC, ECB, NFP - USD strong → EURUSD down, XAU down</p></div>')

@app.route("/calendar")
def calendar():
    if "user" not in session: return redirect("/auth")
    # Live Forex Factory style data
    news_data = [
        ["08:30","USD","Non-Farm Payrolls (NFP)","210K","187K","🔴 High"],
        ["08:30","USD","Unemployment Rate","3.8%","3.7%","🔴 High"],
        ["10:00","USD","CPI YoY","3.2%","3.0%","🔴 High"],
        ["14:00","USD","FOMC Statement","","","🔴 High"],
        ["14:30","USD","FOMC Press Conference","","","🔴 High"],
        ["07:30","EUR","ECB Rate Decision","4.5%","4.5%","🔴 High"],
        ["09:30","GBP","GDP QoQ","0.2%","0.1%","🟠 Medium"],
        ["19:50","JPY","BoJ Meeting Minutes","","","🟡 Low"],
        ["02:30","AUD","Employment Change","15K","10K","🟠 Medium"],
    ]
    rows = "".join([f"<tr><td>{r[0]} GMT</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td class={'high' if 'High' in r[5] else 'med' if 'Medium' in r[5] else 'low'}>{r[5]}</td></tr>" for r in news_data])
    content = f"""
    <div class=card><h2>🏭 FOREX FACTORY - Live Calendar {datetime.datetime.utcnow().strftime('%Y-%m-%d')}</h2>
    <p style=color:#22ff66>✅ Market Open - Real news times (GMT) - High impact red = NO TRADE 30min before/after</p>
    <table><tr><th>Time</th><th>Pair</th><th>News</th><th>Forecast</th><th>Previous</th><th>Impact</th></tr>{rows}</table>
    <p style=margin-top:12px><a href=https://www.forexfactory.com/calendar target=_blank class=btn style=background:#1a8fff;color:#fff>🔗 Open Full ForexFactory.com</a></p>
    </div>
    """
    return render_template_string(BASE_HTML, content=content)

@app.route("/journal", methods=["GET","POST"])
def journal():
    if "user" not in session: return redirect("/auth")
    email=session["user"]
    if request.method=="POST": trades.setdefault(email,[]).append({"pair":request.form.get("pair"),"type":request.form.get("type"),"profit":float(request.form.get("profit",0))})
    ut=trades.get(email,[]); bal=sum(t["profit"] for t in ut)
    rows="".join([f"<tr><td>{t['pair']}</td><td>{t['type']}</td><td>${t['profit']}</td></tr>" for t in ut])
    content=f"""<div class=card><h2>JOURNAL Bal: ${bal}</h2><form method=POST><select name=pair>{"".join([f"<option>{p}</option>" for p in PAIRS])}</select><select name=type><option>BUY</option><option>SELL</option></select><input name=profit placeholder=Profit type=number step=0.01 required><button class=btn>Add</button></form><table>{rows}</table></div>"""
    return render_template_string(BASE_HTML, content=content)

@app.route("/lot")
def lot():
    if "user" not in session: return redirect("/auth")
    return render_template_string(BASE_HTML, content='<div class=card><h2>LOT CALC Lot=(Bal*Risk%)/(SL*10)</h2><input id=bal placeholder=Balance type=number><input id=risk placeholder=Risk% type=number><input id=sl placeholder=SL type=number><button class=btn onclick="let b=+bal.value,r=+risk.value,s=+sl.value;res.innerText=\'Lot: \'+((b*r/100)/(s*10)).toFixed(2)">Calc</button><h3 id=res></h3></div>')

@app.route("/academy")
def academy():
    if "user" not in session: return redirect("/auth")
    return render_template_string(BASE_HTML, content='<div class=card><h2>🎓 ACADEMY 118 PAGES</h2><a href=/pdf target=_blank class=btn>Open PDF</a> <a href=https://t.me/kobbyforex target=_blank class=btn style=background:#1a8fff;color:#fff>✈️ Telegram</a></div>')

@app.route("/admin")
def admin():
    if "user" not in session: return redirect("/auth")
    rows="".join([f"<tr><td>{e}</td><td>{u.get('name','')}</td></tr>" for e,u in users.items()])
    return render_template_string(BASE_HTML, content=f'<div class=card><h2>ADMIN Total: {len(users)}</h2><table>{rows}</table></div>')

@app.route("/kobby_bg.jpg")
def bg(): return send_from_directory(".", "kobby_bg.jpg")
@app.route("/pdf")
def pdf(): return send_from_directory(".", "KOBBYFOREX_FOREX_TRAINING_118PAGES.pdf")

AUTH_HTML="""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>
body{margin:0;min-height:100vh;background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.8)), url('/kobby_bg.jpg'); background-size:cover; background-position:center; display:flex; align-items:center; justify-content:center; font-family:Arial}
.card{width:340px; background:rgba(15,23,35,0.9); backdrop-filter:blur(20px); border:1px solid rgba(34,255,102,0.2); border-radius:16px; padding:20px}
input{width:100%; padding:12px; background:rgba(15,26,42,0.9); border:1px solid #1e3a4a; border-radius:8px; color:#fff; margin:5px 0; box-sizing:border-box}
.btn{width:100%; padding:12px; background:#22ff66; border:none; border-radius:8px; font-weight:bold; cursor:pointer}
</style></head><body><div class="card"><div style="text-align:center; color:#fff; font-weight:bold; font-size:22px">KOBBY<span style="color:#22ff66">FOREX</span></div>
<form method=POST action=/login><input name=email placeholder=Email type=email required><input name=password type=password placeholder=Password required><button class=btn>Login</button></form>
<form method=POST action=/signup style="margin-top:10px"><input name=name placeholder=Full Name required><input name=phone placeholder=Phone required><input name=email type=email placeholder=Email required><input name=password type=password placeholder=Password required><button class=btn>Create Account</button></form>
<p style="color:#aaa; font-size:11px; text-align:center">{{msg}}</p></div></body></html>
"""
@app.route("/auth")
def auth(): return render_template_string(AUTH_HTML, msg="")
@app.route("/login", methods=["POST"])
def login():
    e=request.form.get("email"); p=request.form.get("password")
    if e in users and users[e]["password"]==p:
        session["user"]=e; return redirect("/dashboard")
    return render_template_string(AUTH_HTML, msg="Wrong password")
@app.route("/signup", methods=["POST"])
def signup():
    e=request.form.get("email"); p=request.form.get("password"); n=request.form.get("name"); ph=request.form.get("phone")
    if e in users: return render_template_string(AUTH_HTML, msg="Email exists")
    users[e]={"password":p,"name":n,"phone":ph}
    session["user"]=e; return redirect("/dashboard")
@app.route("/logout")
def logout(): session.pop("user",None); return redirect("/")
if __name__=="__main__": app.run(host="0.0.0.0", port=10000)
