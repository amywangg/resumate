import parse, drive
from flask import Flask, request, render_template, url_for, redirect, jsonify, json
from flask_mysqldb import MySQL
from applicant import applicant
from job import job

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


################################# MAIN ROUTES #######################################

@app.route('/')
@app.route('/home', methods=['GET'])
def home_page():
    # need to display all jobs, display matches,
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Job ORDER BY ID desc limit 5")
    data = cur.fetchall()
    cur.close()
    return render_template('home.html', title="Home", jobs=data)


@app.route('/rankings', methods=['GET'])
def rankings_page():
    # need to display all jobs, display matches,
    cur = mysql.connection.cursor()
    cur.execute("SELECT ID, Job_Title FROM Job ORDER BY ID desc")
    data = cur.fetchall()
    print(data)
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
    cur.execute("SELECT Folder_ID FROM Job WHERE ID = %s",[job_id])
    folder = cur.fetchall()
    link = drive.getLink(folder[0]['Folder_ID'], resume)
    return link


# AJAX: GET LINK TO RESUME
@app.route('/match', methods=['GET'])
def match():
    resume = request.args.get('a', 0, type=str)
    job_id = request.args.get('b', 0, type=str)
    cur = mysql.connection.cursor()
    cur.execute("SELECT Folder_ID FROM Job WHERE ID = %s",[job_id])
    folder = cur.fetchall()
    link = drive.getLink(folder[0]['Folder_ID'], resume)
    return link


# AJAX: GET RANKINGS OF APPLICANTS
@app.route('/getrankings', methods=['GET'])
def get_rankings():
    job_id = request.args.get('a', 0, type=str)
    app_id = request.args.get('b', 0, type=str)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Match (Applicant_ID, Job_ID) VALUES (%s,%s)",
                    (app_id, job_id))
    mysql.connection.commit()

    return ""


# # CREATE SKILLS MODAL
# @app.route('/skill', methods=['POST'])
# def create_skill():
#     if request.method == 'POST':
#         skill_name = request.form['skilltitle']
#         skills = request.form['createskilltag']

#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO Skills (Title, Skills) VALUES (%s,%s)", (skill_name, skills))
#         mysql.connection.commit()
#     return redirect(url_for('job.jobs_page'))