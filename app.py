from datetime import timedelta,datetime
import random 

from flask import Flask,jsonify,render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    datas = TimeData.query.all()
    if datas:
        month_dict = {}
        for data in datas:
            if str(data.timestamp.month) not in month_dict:
                month_dict[str(data.timestamp.month)] = data.read_count
            else:
                month_dict[str(data.timestamp.month)] += data.read_count
    monthly_data = [x for x in month_dict.values()]
    return jsonify({"monthly_data":monthly_data})


if __name__ == "__main__":
    app.run(debug=True)
