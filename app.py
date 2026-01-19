from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("app.db")

@app.route("/")
def home():
    return render_template("home.html")

# Create disclosure
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        conn = db()
        conn.execute(
            "INSERT INTO disclosures (user_id, diagnosis, medications, therapy_type, notes) VALUES (1, ?, ?, ?, ?)",
            (
                request.form["diagnosis"],
                request.form["medications"],
                request.form["therapy"],
                request.form["notes"]
            )
        )
        conn.commit()
        return redirect("/share")
    return render_template("create.html")

# Add recipient
@app.route("/add-recipient", methods=["GET", "POST"])
def add_recipient():
    if request.method == "POST":
        conn = db()
        conn.execute(
            "INSERT INTO recipients (user_id, name, role, phone) VALUES (1, ?, ?, ?)",
            (request.form["name"], request.form["role"], request.form["phone"])
        )
        conn.commit()
        return redirect("/share")
    return render_template("add_recipient.html")

# Share disclosure
@app.route("/share", methods=["GET", "POST"])
def share():
    conn = db()
    disclosure = conn.execute("SELECT * FROM disclosures ORDER BY id DESC LIMIT 1").fetchone()
    recipients = conn.execute("SELECT * FROM recipients").fetchall()

    if request.method == "POST":
        fields = ",".join(request.form.getlist("fields"))
        conn.execute(
            "INSERT INTO shares (disclosure_id, recipient_id, fields) VALUES (?, ?, ?)",
            (disclosure[0], request.form["recipient"], fields)
        )
        conn.commit()
        return redirect("/sent")

    return render_template("share.html", recipients=recipients)

# Recipient view (simulates text link)
@app.route("/view/<int:share_id>")
def view_share(share_id):
    conn = db()
    share = conn.execute("SELECT * FROM shares WHERE id=?", (share_id,)).fetchone()
    disclosure = conn.execute("SELECT * FROM disclosures WHERE id=?", (share[1],)).fetchone()

    fields = share[3].split(",")
    return render_template("view.html", disclosure=disclosure, fields=fields)

@app.route("/sent")
def sent():
    return "Disclosure sent (link would be texted)."

app.run(debug=True)
