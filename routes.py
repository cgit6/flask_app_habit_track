import datetime
import uuid
from flask import Blueprint, current_app, render_template, request, redirect, url_for

pages = Blueprint("habits", __name__, template_folder="templates", static_folder="static")
# habits = ["Test habit"]
# completions = defaultdict(list)

# 這個函數 today_at_midnight 的作用是獲取當天午夜（零點）的日期和時間。
# 具體來說，它返回一個 datetime 對象，該對象表示當天的日期，
# 但時間部分為午夜（00:00:00）。這在需要處理日期而不關心具體時間的場景中特別有用，
# 例如計算日期差異、日誌記錄等。
def today_at_midnight():
    # 今天
    today = datetime.datetime.today() 
    # 創建當天午夜的日期和時間
    return datetime.datetime(today.year, today.month, today.day) # by default, time, min, sec are e


# 以當前日期為基準向前向後三天，共7天
@pages.context_processor
def add_cal_date_range():
    def date_range(start: datetime.datetime):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3,4)]
        return dates
    return {"date_range": date_range}


@pages.route("/")
def index():
    # 檢視當前的url中，取得 ?date= 後面的東西
    date_str = request.args.get("date")
    # print()
    # 如果有 date_str，也就是當前的url中出現年月日
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        # 如果 url 中沒有date 的話顯示當天訊息
        selected_date = today_at_midnight()

    # 搜尋某一天的資料
    habits_on_date = current_app.db.habits.find({"added": {"$lte":selected_date}})

    completions = [
        habit["habit"]
        for habit in current_app.db.completions.find({"date": selected_date})
    ]
    return render_template("app.html", habits=habits_on_date, selected_date=selected_date, completions=completions, title="Habit Tracker - Home")


@pages.route("/add", methods=["GET","POST"])
def add_habit():
    today = today_at_midnight()
    # 
    if request.method == "POST":
        # # 獲取 client 送出的訊息,"habit" 是 textarea 的 name
        # habit = request.form.get("habit")
        # print("data",habit)
        # habits.append(habit)

        # 新增到數據庫
        current_app.db.habits.insert_one({"_id": uuid.uuid4().hex, "added": today, "name": request.form.get("habit")})



    return render_template("add_habit.html", title="Habit Tracker - Add Habit", selected_date=today,)

# 工作清單
@pages.route("/complete", methods=["POST"])
def complete():
    date_string = request.form.get("date")
    # 
    habit = request.form.get("habitId")
    date = datetime.datetime.fromisoformat(date_string)
    current_app.db.completions.insert_one({"date": date, "habit": habit})
    # 

    return redirect(url_for("habits.index", date=date_string))

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=3000)
