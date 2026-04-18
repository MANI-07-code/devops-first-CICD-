from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# ---------------- DATA ----------------
students = {
    101: {"name": "mani", "dob": "27-10-2005", "marks": None},
    102: {"name": "bharath", "dob": "18-01-2005", "marks": None}
}

TEACHER_ID = 1001
TEACHER_PASS = 1234


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- TEACHER LOGIN ----------------
@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    if request.method == "POST":
        try:
            tid = int(request.form["tid"])
            tpass = int(request.form["tpass"])
        except:
            return "Invalid input"

        if tid == TEACHER_ID and tpass == TEACHER_PASS:
            return redirect(url_for("add_marks"))
        else:
            return "Invalid teacher credentials"

    return render_template("teacher_login.html")


# ---------------- ADD MARKS ----------------
@app.route("/add_marks", methods=["GET", "POST"])
def add_marks():
    if request.method == "POST":
        try:
            sid = int(request.form["sid"])
            t = int(request.form["tamil"])
            e = int(request.form["english"])
            m = int(request.form["maths"])
            sci = int(request.form["science"])
            soc = int(request.form["social"])
        except:
            return "Invalid input"

        if sid in students:
            students[sid]["marks"] = {
                "tamil": t,
                "english": e,
                "maths": m,
                "science": sci,
                "social": soc
            }
            return render_template("result.html", msg="Marks updated successfully!")
        else:
            return render_template("result.html", msg="Invalid student ID")

    return render_template("add_marks.html")


# ---------------- STUDENT LOGIN ----------------
@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        try:
            sid = int(request.form["sid"])
            dob = request.form["dob"]
        except:
            return "Invalid input"

        if sid in students and students[sid]["dob"] == dob:
            return redirect(url_for("view_marks", sid=sid))
        else:
            return render_template("result.html", msg="Invalid student details")

    return render_template("student_login.html")


# ---------------- VIEW MARKS ----------------
@app.route("/view/<int:sid>")
def view_marks(sid):
    if sid in students:
        student = students[sid]
        return render_template("view.html", student=student)
    return render_template("result.html", msg="Student not found")


# ---------------- HEALTH CHECK ----------------
@app.route("/health")
def health():
    return jsonify({"status": "running"}), 200


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
