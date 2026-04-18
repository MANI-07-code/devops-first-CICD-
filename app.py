from flask import Flask, render_template, request

app = Flask(__name__)

accounts = {}
acc_no = 1000

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create", methods=["POST"])
def create():
    global acc_no
    name = request.form["name"]

    accounts[acc_no] = {
        "name": name,
        "balance": 0
    }

    acc_no += 1
    return f"Account created! Account No: {acc_no-1}"


@app.route("/deposit", methods=["POST"])
def deposit():
    acc = int(request.form["acc"])
    amt = int(request.form["amount"])

    if acc in accounts:
        accounts[acc]["balance"] += amt
        return f"Balance: {accounts[acc]['balance']}"
    return "Account not found"


@app.route("/withdraw", methods=["POST"])
def withdraw():
    acc = int(request.form["acc"])
    amt = int(request.form["amount"])

    if acc in accounts:
        if accounts[acc]["balance"] >= amt:
            accounts[acc]["balance"] -= amt
            return f"Withdraw successful. Balance: {accounts[acc]['balance']}"
        else:
            return "Insufficient balance"
    return "Account not found"


@app.route("/account", methods=["POST"])
def account():
    acc = int(request.form["acc"])

    if acc in accounts:
        data = accounts[acc]
        return f"Name: {data['name']} | Balance: {data['balance']}"
    return "Account not found"


app.run(host="0.0.0.0", port=5001)
