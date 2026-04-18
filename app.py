from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage
students = {
    101: {"name": "mani", "dob": "27-10-2005", "marks": None},
    102: {"name": "bharath", "dob": "18-01-2005", "marks": None}
}

# Teacher credentials
TEACHER_ID = 1001
TEACHER_PASS = 1234


@app.route("/")
def home():
    return render_template("index.html")


# ---------------- TEACHER LOGIN ----------------
@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    if request.method == "POST":
        tid = int(request.form["tid"])
        tpass = int(request.form["tpass"])

        if tid == TEACHER_ID and tpass == TEACHER_PASS:
            return redirect(url_for("add_marks"))
        else:
            return "Invalid teacher credentials"

    return render_template("teacher_login.html")


# ---------------- ADD MARKS ----------------
@app.route("/add_marks", methods=["GET", "POST"])
def add_marks():
    if request.method == "POST":
        sid = int(request.form["sid"])

        if sid in students:
            t = int(request.form["tamil"])
            e = int(request.form["english"])
            m = int(request.form["maths"])
            sci = int(request.form["science"])
            soc = int(request.form["social"])

            students[sid]["marks"] = {
                "tamil": t,
                "english": e,
                "maths": m,
                "science": sci,
                "social": soc
            }

            return "Marks updated successfully!"
        else:
            return "Invalid student ID"

    return render_template("add_marks.html")


# ---------------- STUDENT LOGIN ----------------
@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        sid = int(request.form["sid"])
        dob = request.form["dob"]

        if sid in students and students[sid]["dob"] == dob:
            return redirect(url_for("view_marks", sid=sid))
        else:
            return "Invalid details"

    return render_template("student_login.html")


# ---------------- VIEW MARKS ----------------
@app.route("/view/<int:sid>")
def view_marks(sid):
    if sid in students:
        student = students[sid]
        return render_template("view.html", student=student)
    return "Student not found"


# ---------------- HEALTH CHECK ----------------
@app.route("/health")
def health():
    return {"status": "running"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
