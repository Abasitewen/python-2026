from flask import Flask, request

app = Flask(__name__)

crazy_database = {
    "names": ("Jacopo", "Bill", "Anna"),
    "surnames": ("Salvalaggio", "Clinton", "Karenina")
}

@app.route("/name/<user_id>")
def get_name(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return "Ivalid used ID, must be an integer.\n", 400
    try:
        name = crazy_database["names"][user_id]
        surname = crazy_database["surnames"][user_id]
    except IndexError:
        return "User ID not found\n", 404
    else:
        return_string = f"{name} {surname}\n"
        return return_string, 200

@app.route("/double", methods=["GET", "POST"])
def multiply_by_two():
    if request.method == "GET":
        number = request.args.get("number")
    elif request.method == "POST":
        number = request.form["number"]
    return_number = f"{2 * float(number)}\n"
    return return_number, 200

if __name__ == "__main__":
    app.run()
