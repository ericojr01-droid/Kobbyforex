from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KOBBYFOREX</title>
<style>
body{margin:0;font-family:Arial;background:#0a0e13;color:#e8e6e1;display:flex}
.sidebar{width:260px;background:#11161e;border-right:1px solid #2a2f3a;padding:20px;min-height:100vh}
.main{flex:1;padding:30px;background:#0a0e13}
.card{background:#151b26;border:1px solid #2a3441;border-radius:12px;padding:20px;margin:10px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:15px}
.gold{color:#c9a86a} .badge{background:#2a2418;color:#d4b87a;border:1px solid #5a4e32;padding:4px 10px;border-radius:15px;font-size:11px}
h1{font-size:36px}
@media(max-width:700px){.sidebar{display:none}.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="sidebar">
<div style="display:flex;gap:10px;align-items:center"><div style="width:36px;height:36px;border-radius:50%;border:1px solid #c9a86a;display:flex;align-items:center;justify-content:center;color:#c9a86a">KM</div><div><b>Kobby Miller</b><div style="font-size:11px;opacity:0.6">Institutional Trader</div></div></div>
<div style="margin-top:30px;font-size:11px;letter-spacing:2px;opacity:0.5">NAVIGATION</div>
<div style="margin-top:15px;padding:12px;background:#2e281a;color:#e8c88a;border-radius:8px">📈 Market Intelligence</div>
<div style="padding:12px;opacity:0.6">⛏️ Gold Digger</div>
<div style="padding:12px;opacity:0.6">📓 Journal</div>
<div style="padding:12px;opacity:0.6">🎓 Academy</div>
<div style="padding:12px;opacity:0.6">📋 System Log</div>
<div style="margin-top:40px;text-align:center"><div style="font-size:11px;opacity:0.5">SYSTEM STATUS</div><div style="color:#4ade80;font-size:12px;margin-top:5px">● All Systems Online</div></div>
</div>
<div class="main">
<div style="display:flex;justify-content:space-between"><div><span class="gold" style="font-weight:800;letter-spacing:2px">🛡️ KOBBYFOREX</span><br><span style="font-size:10px;letter-spacing:2px" class="gold">INSTITUTIONAL COMMAND CENTER</span></div><div>🔔 ⚙️ KM</div></div>
<h1 style="margin-top:40px">Welcome to Kobbyforex</h1>
<p style="opacity:0.6">Unlock Your trading potential with institutional-grade tools, precision analytics, and expert-driven strategies.</p>
<div style="color:#c9a86a;letter-spacing:3px;font-size:13px;margin:30px 0 15px">INSTITUTIONAL MODULES</div>
<div class="grid">
<div class="card"><div>🏛️</div><h3>Prop Firm</h3><p style="opacity:0.6;font-size:13px">Access exclusive funded trading challenges and evaluation programs. Manage accounts, track metrics, and scale your capital.</p><div class="badge">Active • 3 Evaluations</div></div>
<div class="card"><div>📊</div><h3>Market Intelligence</h3><p style="opacity:0.6;font-size:13px">Real-time market analysis, sentiment trends, and institutional flow data to inform your trades.</p><div class="badge">Live Data • Updated Now</div></div>
<div class="card"><div>⛏️</div><h3>Gold Digger</h3><p style="opacity:0.6;font-size:13px">Our proprietary XAUUSD strategy engine. AI-driven signals with risk-managed entry and exit points.</p><div class="badge">Strategy • Enabled</div></div>
<div class="card"><div>🎓</div><h3>Trading Academy</h3><p style="opacity:0.6;font-size:13px">Professional courses, structured learning paths, and mentorship from institutional traders.</p><div class="badge">12 Courses • 4 Certificates</div></div>
</div>
<div style="margin-top:20px;font-size:10px;opacity:0.3">Version 2.4.1 • Last sync: 14:32 UTC • Secure Connection</div>
</div>
</body>
</html>
"""
