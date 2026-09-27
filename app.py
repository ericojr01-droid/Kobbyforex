import os
import requests
from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "kobbyforex_secret_2026"

# === TELEGRAM CONFIG - PUT YOUR OWN HERE ===
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID_HERE")
TELEGRAM_CHANNEL_LINK = "https://t.me/kobbyforex" # Change to your channel link

users = {} # Simple storage: email -> {password, name}

def send_telegram_alert(email, name=""):
    try:
        if "YOUR_BOT_TOKEN" in BOT_TOKEN:
            return # Skip if not set
        msg = f"🎉 NEW USER - KOBBYFOREX!\n\n📧 Email: {email}\n👤 Name: {name}\n🌐 Site: kobbyforex.onrender.com"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except:
        pass

# === HTML TEMPLATE - YOUR BULL & BEAR DESIGN ===
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KOBBYFOREX - Login</title>
<style>
body{
  margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
  background:#0a0e0a; position:relative; overflow:hidden;
  font-family: Arial, sans-serif;
}
body::before{
  content:''; position:absolute; inset:0;
  background: radial-gradient(circle at 20% 50%, rgba(0,255,100,0.25), transparent 40%),
              radial-gradient(circle at 80% 50%, rgba(255,50,50,0.2), transparent 40%),
              linear-gradient(180deg, #0a1210 0%, #000 100%);
  z-index:0;
}
.bull{position:absolute; left:-5%; top:10%; font-size:350px; opacity:0.25; filter: drop-shadow(0 0 30px #00ff88); z-index:0;}
.bear{position:absolute; right:-5%; top:10%; font-size:350px; opacity:0.25; filter: drop-shadow(0 0 30px #ff4444); z-index:0;}
.card{
  position:relative; z-index:2; width:360px; background:rgba(15,23,35,0.85); backdrop-filter:blur(20px);
  border:1px solid rgba(255,255,255,0.1); border-radius:20px; padding:28px; box-shadow:0 20px 60px rgba(0,0,0,0.8);
}
.logo{display:flex; align-items:center; justify-content:center; gap:8px; margin-bottom:18px; color:#fff; font-weight:bold; font-size:22px;}
.logo span{color:#00ff88}
.tabs{display:flex; background:rgba(0,0,0,0.4); border-radius:12px; padding:4px; margin-bottom:20px;}
.tab{flex:1; padding:10px; text-align:center; border-radius:8px; cursor:pointer; color:#888; font-weight:bold;}
.tab.active{background:#1a2a3a; color:#00ff88; border-bottom:2px solid #00ff88;}
label{color:#aaa; font-size:13px; margin:12px 0 6px; display:block;}
input{width:100%; padding:14px; background:#0f1a2a; border:1px solid #1e3a4a; border-radius:10px; color:#fff; outline:none; box-sizing:border-box;}
input::placeholder{color:#556;}
.btn{width:100%; padding:14px; background:#00ff66; border:none; border-radius:10px; font-weight:bold; font-size:16px; margin-top:18px; cursor:pointer; color:#000;}
.forgot{color:#00ff88; font-size:12px; text-align:right; margin-top:8px; display:block; text-decoration:none;}
.divider{display:flex; align-items:center; gap:10px; margin:16px 0; color:#555; font-size:13px;}
.divider::before,.divider::after{content:''; flex:1; height:1px; background:#222;}
.tele{width:100%; padding:12px; background:#1a8fff; border:none; border-radius:10px; color:#fff; font-weight:bold; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px; text-decoration:none;}
</style>
</head>
<body>
<div class="bull">🐂</div>
<div class="bear">🐻</div>
<div class="card">
  <div class="logo">📈 KOBBY<span>FOREX</span></div>

  <div class="tabs">
    <div class="tab active" id="loginTab" onclick="showLogin()">Login</div>
    <div class="tab" id="signupTab" onclick="showSignup()">Sign Up</div>
  </div>

  <form id="loginForm" method="POST" action="/login">
    <label>Email</label>
    <input type="email" name="email" placeholder="you@example.com" required>
    <label>Password</label>
    <input type="password" name="password" placeholder="••••••••" required>
    <a class="forgot" href="#">Forgot password?</a>
    <button class="btn" type="submit">Login</button>
  </form>

  <form id="signupForm" method="POST" action="/signup" style="display:none;">
    <label>Full Name</label>
    <input type="text" name="name" placeholder="Kobby Forex" required>
    <label>Email</label>
    <input type="email" name="email" placeholder="you@example.com" required>
    <label>Password</label>
    <input type="password" name="password" placeholder="••••••••" required>
    <button class="btn" type="submit">Create Account</button>
  </form>

  <div class="divider">or</div>
  <a href="{{channel}}" target="_blank" class="tele">✈️ Join My Telegram Channel →</a>
  <p style="color:#666; font-size:11px; text-align:center; margin-top:12px;">{{msg}}</p>
</div>

<script>
function showLogin(){
  document.getElementById('loginForm').style.display='block';
  document.getElementById('signupForm').style.display='none';
  document.getElementById('loginTab').classList.add('active');
  document.getElementById('signupTab').classList.remove('active');
}
function showSignup(){
  document.getElementById('loginForm').style.display='none';
  document.getElementById('signupForm').style.display='block';
  document.getElementById('signupTab').classList.add('active');
  document.getElementById('loginTab').classList.remove('active');
}
</script>
</body>
</html>
"""

DASH = """
<h2 style="text-align:center; color:#00ff88; margin-top:100px;">Welcome {{email}} 🎉<br><br>KOBBYFOREX Dashboard Live!</h2>
<p style="text-align:center;"><a href="/logout" style="color:red;">Logout</a></p>
"""

@app.route("/")
def home():
    if "user" in session:
        return render_template_string(DASH, email=session["user"])
    return render_template_string(LOGIN_PAGE, channel=TELEGRAM_CHANNEL_LINK, msg="")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    pwd = request.form.get("password")
    if email in users and users[email]["password"] == pwd:
        session["user"] = email
        return redirect("/")
    return render_template_string(LOGIN_PAGE, channel=TELEGRAM_CHANNEL_LINK, msg="❌ Wrong email or password")

@app.route("/signup", methods=["POST"])
def signup():
    email = request.form.get("email")
    pwd = request.form.get("password")
    name = request.form.get("name")
    if email in users:
        return render_template_string(LOGIN_PAGE, channel=TELEGRAM_CHANNEL_LINK, msg="⚠️ Email already exists")
    users[email] = {"password": pwd, "name": name}
    send_telegram_alert(email, name) # <-- THIS IS THE FUNCTION WE TALK
    session["user"] = email
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
