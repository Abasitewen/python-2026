from flask import Flask, request
from markupsafe import escape
app = Flask(__name__)
values = {"1": 1, "ciao": 2}
@app.route("/user/<user_id>")
def hello_world(user_id):
    value = values[user_id]
    return f"{value}", 200
@app.route("/greet")
def greet():
    name = request.args.get("name")
    return f"Hi, {escape(name)}!", 200
if __name__ == "__main__":
    app.run()
