import pyodbc
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
server = 'assignmentservershruthaja.database.windows.net'
database = 'quiz2'
username = 'shruthaja'
password = ''
driver = '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')

cursor = conn.cursor()


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    result = []
    r=""
    if request.method == "POST":
        cname = request.form['cityname']
        query = "select * from dbo.city where City=?"
        cursor.execute(query, cname)
        result = cursor.fetchall()
        query = " select lat , lon from dbo.city where City=? "
        cursor.execute(query, cname)
        lr = cursor.fetchone()
        query =  "SELECT * FROM [dbo].[city] WHERE ( 6371 * ACOS(COS(RADIANS(lat)) * COS(RADIANS(?)) * COS(RADIANS(lon) - RADIANS(?)) + SIN(RADIANS(lat)) * SIN(RADIANS(?)) ))< 100"
        cursor.execute(query,lr[0], lr[1], lr[0])
        r = cursor.fetchall()
    return render_template("index.html", result=result, r=r)

@app.route('/page2.html', methods=['GET', 'POST'])
def page2():
    result=[]
    if request.method=="POST":
        minlat=request.form['lat']
        minlon=request.form['lon']
        maxlat=request.form['mlat']
        maxlon=request.form['mlon']
        query="select * from dbo.city where lat between ? and ? and lon between ? and ?"
        cursor.execute(query,minlat,maxlat,minlon,maxlon)
        result=cursor.fetchall()
    return render_template("page2.html",result=result)

@app.route('/page3.html', methods=['GET', 'POST'])
def page3():
    result=[]
    cnames=[]
    minlat=""
    minlon=''
    maxlat=''
    maxlon=''
    state=''
    if request.method=="POST":
        minlat = request.form['lat']
        minlon = request.form['lon']
        maxlat = request.form['mlat']
        maxlon = request.form['mlon']
        state=request.form['state']
        min=request.form['min']
        max=request.form['max']
        inc=request.form['inc']
        if(state!=""):
            query="select * from dbo.city where population>? and population<? and state=?"
            cursor.execute(query,min,max,state)
            cnames=cursor.fetchall()
            query="update city set population=population+? where City in (select City from dbo.city where population>? and population<? and state=?)"
            cursor.execute(query,inc,min,max,state)
            cursor.commit()
        else:
            query="select * from dbo.city where lat between ? and ? and lon between ? and ? and  population>? and population<?"
            cursor.execute(query,minlat,maxlat,minlon,maxlon,min,max)
            cnames = cursor.fetchall()
            query = "update city set population=population+? where City in (select City from dbo.city where lat between ? and ? and lon between ? and ? and  population>? and population<?)"
            cursor.execute(query, inc, minlat,maxlat,minlon,maxlon,min,max)
            cursor.commit()
    return render_template("page3.html",cnames=cnames)

@app.route('/page4.html', methods=['GET', 'POST'])
def page4():
    result = []
    r=""
    city=''
    state=""
    if request.method == "POST":
        city=request.form['cityname']
        state=request.form['statename']
        if(city!=""):
            query="delete from city where City=?"
            cursor.execute(query,city)
            cursor.commit()
        else:
            query = "delete from city where state=?"
            cursor.execute(query, state)
            cursor.commit()
    return render_template("page4.html", result=result, r=r)
@app.route('/page42.html', methods=['GET', 'POST'])
def page42():
    if request.method == "POST":
        city=request.form['cityname1']
        state=request.form['statename1']
        lat=request.form['lat']
        lon=request.form['lon']
        pop=request.form['pop']
        query="insert into city values(?,?,?,?,?)"
        cursor.execute(query,city,state,pop,lat,lon)
        cursor.commit()
    return render_template("page4.html")
if __name__ == '__main__':
    app.run(debug=True)
