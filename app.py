from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("cannabis_data.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
@app.route("/strains")
def strains():
    conn = get_db()
    rows = conn.execute("SELECT name, terpenes, helps_with FROM strains").fetchall()
    conn.close()
    return render_template("strains.html", strains=rows)

if __name__ == "__main__":
    app.run(debug=True)
