from datetime import timedelta,datetime,date
import random 

from flask import Flask,jsonify,render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)


#@app.before_first_request
def init():
    db.create_all()

    #populating the database
    start = datetime(2020,1,1)
    end = datetime(2020,12,31,hour=23,minute=59)
    delta = timedelta(minutes=5)
    while (start < end):
        entry = TimeData(timestamp = start , read_count=random.randint(0,5))
        db.session.add(entry)
        start = start + delta
    db.session.commit()

class TimeData(db.Model):
    timestamp = db.Column(db.DateTime,unique=True,primary_key=True)
    read_count = db.Column(db.Integer,nullable=False)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/year")
def monthly_data():
    dat = db.engine.execute("select sum(read_count) from time_data group by strftime('%m',timestamp)")
    monthly_data = [x[0] for x in dat]
    #datas = TimeData.query.all()
    #if datas:
    #    month_dict = {}
    #    for data in datas:
    #        if str(data.timestamp.month) not in month_dict:
    #            month_dict[str(data.timestamp.month)] = data.read_count
    #        else:
    #            month_dict[str(data.timestamp.month)] += data.read_count
    #monthly_data = [x for x in month_dict.values()]
    return jsonify({"monthly_data":monthly_data})

@app.route("/api/weekly")
def weekly_data():
    curr = date.today()
    start_of_week = curr - timedelta(days=curr.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    dat = db.engine.execute(f"select sum(read_count) from time_data where date(timestamp) \
            between '{start_of_week}' and '{end_of_week}' group by strftime('%w',timestamp)")
    datas = [x[0] for x in dat]
    datas[0],datas[1]  = datas[1],datas[0]
    weekly_data = datas
    #datas = TimeData.query.all()
    #if datas:
    #    weekly_dict = {}
    #    curr = date.today()
    #    start_of_week = curr - timedelta(days=curr.weekday())
    #    end_of_week = start_of_week + timedelta(days=6)
    #    for data in datas:
    #        if start_of_week <= data.timestamp.date() <= end_of_week : 
    #            if data.timestamp.weekday() not in weekly_dict:
    #                weekly_dict[data.timestamp.weekday()] = data.read_count
    #            else:
    #                weekly_dict[data.timestamp.weekday()] += data.read_count
    #    weekly_data = [x for x in weekly_dict.values()]
    return jsonify({"weekly_data":weekly_data})

@app.route("/api/daily")
def daily_data():
    datas = db.engine.execute("select sum(read_count) from time_data where date(timestamp) = date('now') group by strftime('%H',timestamp)")    
    daily_data = [x[0] for x in datas]
    #daily_dict = {}
    #if datas:   
    #    curr = date.today()
    #    for data in datas:
    #        if data.timestamp.date() == curr :
    #            if data.timestamp.hour not in daily_dict:
    #                daily_dict[data.timestamp.hour] = data.read_count
    #            else:
    #                daily_dict[data.timestamp.hour] += data.read_count
    #daily_data = [x for x in daily_dict.values()]
    return jsonify({"daily_data":daily_data})

@app.route("/viz")
def viz():
    return render_template("viz.html")


@app.route("/viz2")
def viz2():
    return render_template("viz2.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
