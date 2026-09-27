from flask import render_template

def register_all(app):
    @app.route("/")
    def home():
        return "<h1 style='color:gold;background:black;padding:50px;text-align:center'>KOBBYFOREX Modular Loading... Step 2 Done!</h1>"

    @app.route("/kobby_bg.jpg")
    def bg():
        from flask import send_from_directory
        import os
        return send_from_directory("static", "kobby_bg.jpg") if os.path.exists("static/kobby_bg.jpg") else ("",404)
