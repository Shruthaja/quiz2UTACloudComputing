import pyodbc
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
server = 'assignmentservershruthaja.database.windows.net'
database = 'quiz2'
username = 'shruthaja'
password = 'mattu4-12'
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
        query = "SELECT * FROM [dbo].[city] WHERE ( 6371 * ACOS(COS(RADIANS(lat)) * COS(RADIANS(?)) * COS(RADIANS(lon) - RADIANS(?)) + SIN(RADIANS(lat)) * SIN(RADIANS(?)) ))< ?;"
        cursor.execute(query, lr[0], lr[1], lr[0], 100)
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

if __name__ == '__main__':
    app.run(debug=True)
