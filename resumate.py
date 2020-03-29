import parse, drive
from flask import Flask, request, render_template, url_for, redirect, jsonify, json
from flask_mysqldb import MySQL
from applicant import applicant
from job import job
from collections import Counter

app = Flask(__name__)
app.register_blueprint(job)
app.register_blueprint(applicant)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Fires-123'
app.config['MYSQL_DB'] = 'resumate'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['UPLOAD_FOLDER'] = 'resumetemp'
mysql = MySQL(app)

############## STATS AJAX ###################
@app.route('/jobapplicants', methods=['GET'])
def job_applicants():
    cur = mysql.connection.cursor()
    cur.execute("SELECT J.ID, J.Job_Title, COUNT(R.Applicant_ID) as Applicants  FROM Job J INNER JOIN Rankings R ON R.Job_ID=J.ID INNER JOIN Applicant A ON R.Applicant_ID=A.ID GROUP BY R.Job_ID ORDER BY Count(R.Applicant_ID) desc LIMIT 10")
    data = cur.fetchall()
    print(data)
    for x in data:
        cur.execute(
            "SELECT COUNT(Applicant_ID) FROM resumate.Match WHERE Job_ID=(%s)", [x['ID']])
        matches = cur.fetchall()
        x['Matches'] = matches[0]['COUNT(Applicant_ID)']

    return jsonify(data)


@app.route('/topskills', methods=['GET'])
def top_skills():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Skills FROM Skills")
    data = cur.fetchall()
    skillist=[]
    for x in data:
        skillist += json.loads(x['Skills'])
    sortedskills = sorted(dict(Counter(skillist)).items(), key=lambda x: x[1], reverse=True)
    print(sortedskills)
    return jsonify(sortedskills)

################################# MAIN ROUTES #######################################


@app.route('/')
@app.route('/home', methods=['GET'])
def home_page():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM resumate.Match M INNER JOIN Job J ON J.ID=M.Job_ID WHERE Job_Status='open' ")
    match=[]
    for x in cur.fetchall():
        data=dict()
        cur.execute("SELECT Name, Email FROM Applicant WHERE ID =(%s)",[x['Applicant_ID']])
        app = cur.fetchall()[0]
        data['Name']=app['Name']
        data['Email']=app['Email']
        cur.execute("SELECT Job_Title FROM Job WHERE ID =(%s)",[x['Job_ID']])
        data['Job_Title']=cur.fetchall()[0]['Job_Title']
        cur.execute("SELECT Matched_Skills FROM Rankings WHERE Applicant_ID =(%s) AND Job_ID = (%s)",[x['Applicant_ID'],x['Job_ID']])
        data['Skills']=cur.fetchall()[0]['Matched_Skills']
        data['Skills']= data['Skills'].replace('[','')
        data['Skills']= data['Skills'].replace(']','')
        data['Skills']= data['Skills'].replace('"','')
        match.append(data)

    return render_template('home.html', title="Home", match = match)


@app.route('/rankings', methods=['GET'])
def rankings_page():
    # need to display all jobs, display matches,
    cur = mysql.connection.cursor()
    cur.execute("SELECT ID, Job_Title FROM Job ORDER BY ID desc")
    data = cur.fetchall()
    cur.close()
    return render_template('rankings.html', title="Rankings", jobs=data)


# AJAX: GET LIST OF JOBS FOR SEARCH
@app.route('/getjobs', methods=['GET'])
def get_jobs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Job ORDER BY ID desc")
    data = cur.fetchall()
    return list(data['Title'])


# AJAX: GET LINK TO RESUME
@app.route('/drive', methods=['GET'])
def get_link():
    resume = request.args.get('a', 0, type=str)
    job_id = request.args.get('b', 0, type=str)
    cur = mysql.connection.cursor()
    cur.execute("SELECT Folder_ID FROM Job WHERE ID = %s", [job_id])
    folder = cur.fetchall()
    link = drive.getLink(folder[0]['Folder_ID'], resume)
    return link


# AJAX: GET RANKINGS OF APPLICANTS
@app.route('/getrankings', methods=['GET'])
def get_rankings():
    job_id = request.args.get('a', 0, type=str)
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM Applicant A INNER JOIN Rankings R ON R.Job_ID=(%s) AND A.ID = R.Applicant_ID ORDER BY r.Score desc", [job_id])
    data = cur.fetchall()
    # check if theres a match
    for x in data:
        cur.execute("SELECT * FROM resumate.Match WHERE Applicant_ID=(%s) AND Job_ID=(%s)",
                    (x['Applicant_ID'], job_id))
        match = cur.fetchall()
        if match == ():
            x['Match'] = 'False'
        else:
            x['Match'] = 'True'

    return jsonify(data)


# AJAX: GET RANKINGS OF APPLICANTS
@app.route('/match', methods=['POST', 'GET'])
def match():
    app_id = request.args.get('a', 0, type=str)
    job_id = request.args.get('b', 0, type=str)

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO resumate.Match (Applicant_ID, Job_ID) VALUES (%s,%s)", (int(
        app_id), int(job_id)))
    mysql.connection.commit()

    return app_id


# AJAX: GET RANKINGS OF APPLICANTS
@app.route('/unmatch', methods=['POST', 'GET'])
def unmatch():
    app_id = request.args.get('a', 0, type=str)
    job_id = request.args.get('b', 0, type=str)

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM resumate.Match WHERE Applicant_ID=(%s) AND Job_ID=(%s)", (int(
        app_id), int(job_id)))
    mysql.connection.commit()

    return app_id
