from flask import Flask, render_template, request
app = Flask(__name__)

# 資料庫
habits = ["Test habit","Test habit2"]

@app.route("/")
def index():
    return render_template("app.html", habits=habits ,title="Habit Tracker - Home")


@app.route("/add", methods=["GET","POST"])
def add_habit():
    if request.method == "POST":
        # 獲取 client 送出的訊息,"habit" 是 textarea 的 name
        habit = request.form.get("habit")
        print("data",habit)
        habits.append(habit)

    return render_template("add_habit.html", title="Habit Tracker - Add Habit")
