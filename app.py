from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "secret123"  # needed for session

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
        tid = request.form.get("tid")
        tpass = request.form.get("tpass")

        if tid == str(TEACHER_ID) and tpass == str(TEACHER_PASS):
            session["teacher"] = True
            return redirect(url_for("add_marks"))
        else:
            flash("Invalid teacher credentials")

    return render_template("teacher_login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ---------------- ADD MARKS ----------------
@app.route("/add_marks", methods=["GET", "POST"])
def add_marks():
    if not session.get("teacher"):
        return redirect(url_for("teacher"))

    if request.method == "POST":
        try:
            sid = int(request.form["sid"])
            marks = {
                "tamil": int(request.form["tamil"]),
                "english": int(request.form["english"]),
                "maths": int(request.form["maths"]),
                "science": int(request.form["science"]),
                "social": int(request.form["social"])
            }
        except:
            flash("Invalid input")
            return redirect(url_for("add_marks"))

        if sid in students:
            students[sid]["marks"] = marks
            flash("Marks updated successfully!")
        else:
            flash("Student not found")

    return render_template("add_marks.html")


# ---------------- STUDENT LOGIN ----------------
@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        try:
            sid = int(request.form["sid"])
            dob = request.form["dob"].strip()
        except:
            flash("Invalid input")
            return redirect(url_for("home"))

        if sid not in students:
            flash("Student not found")
            return redirect(url_for("home"))

        if students[sid]["dob"] != dob:
            flash("Wrong DOB")
            return redirect(url_for("home"))

        return redirect(url_for("view_marks", sid=sid))

    return render_template("student_login.html")


# ---------------- VIEW MARKS ----------------
@app.route("/view/<int:sid>")
def view_marks(sid):
    student = students.get(sid)

    if not student:
        return "Student not found"

    marks = student["marks"]

    total = sum(marks.values()) if marks else 0
    avg = total / 5 if marks else 0

    grade = "N/A"
    if avg >= 90:
        grade = "A"
    elif avg >= 75:
        grade = "B"
    elif avg >= 50:
        grade = "C"
    else:
        grade = "Fail"

    return render_template("view.html", student=student, total=total, avg=avg, grade=grade)


# ---------------- HEALTH ----------------
@app.route("/health")
def health():
    return {"status": "running"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
