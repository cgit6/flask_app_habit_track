from flask import Flask, render_template, request
import datetime
app = Flask(__name__)

# 資料庫
habits = ["Test habit","Test habit2"]

# 以當前日期為基準向前向後三天，共7天
def date_range(start: datetime.date):
    dates = [start + datetime.timedelta(days=diff) for diff in range(-3,4)]
    return dates


@app.route("/")
def index():
    # 檢視當前的url中，取得 ?date= 後面的東西
    date_str = request.args.get("date")
    # print()
    # 如果有 date_str，也就是當前的url中出現年月日
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
    else:
        selected_date = datetime.date.today()

    return render_template("app.html", habits=habits ,title="Habit Tracker - Home", date_range=date_range, selected_date=selected_date)


@app.route("/add", methods=["GET","POST"])
def add_habit():
    if request.method == "POST":
        # 獲取 client 送出的訊息,"habit" 是 textarea 的 name
        habit = request.form.get("habit")
        print("data",habit)
        habits.append(habit)

    return render_template("add_habit.html", title="Habit Tracker - Add Habit")
