import parse, drive
from flask import Flask, request, render_template, url_for, redirect, jsonify, json
from flask_mysqldb import MySQL
from applicant import applicant

app = Flask(__name__)
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


# GET ALL JOBS
@app.route('/jobs', methods=['GET'])
def jobs_page():
    # need to display all jobs, display matches,
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Job")
    data = cur.fetchall()
    cur.close()
    return render_template('jobs.html', title="Jobs", jobs=data)


# CREATE JOB
# GET: get skills matrix if use existing, POST: post new job and skills
@app.route('/job/create', methods=['GET', 'POST'])
def create_job():
    # TODO: if using existing add skill id from existing to db
    if request.method == 'POST':
        job_title = request.form['title']
        job_description = request.form['description']
        job_status = "open"

        skill_name = request.form['skillname']
        print(request.form['skilltag'])
        print(type(request.form['skilltag']))
        skills = request.form['skilltag']
 
        # connect to sql execute queries
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Skills (Title, Skills) VALUES (%s,%s)", (skill_name, skills))
        cur.execute("INSERT INTO Job (Job_Title, Job_Description, Job_Status, Skills_ID) VALUES (%s,%s,%s,%s)",
                    (job_title, job_description, job_status, cur.lastrowid))
        job_id = cur.lastrowid

       # Create a folder in the drive with the job id return folder id for future use
        folder_id = drive.createFolder(str(job_id) + "-" + job_title )
        cur.execute("UPDATE Job SET Folder_ID = (%s)"
                    "WHERE job.ID = (%s)",
                    (folder_id, job_id))
        mysql.connection.commit()

        return redirect(url_for('jobs_page'))
        # return redirect('/job/create/' + str(cur.lastrowid))

    return render_template('create-job.html', title="Create Job")


# DELETE JOB
@app.route('/job/delete/<string:job_id>', methods=['GET'])
def delete_job(job_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Job WHERE ID=%s", (job_id,))
    mysql.connection.commit()

    # TODO: delete folder from drive

    return redirect(url_for('jobs_page'))


# UPDATE JOB
@app.route('/job/update/<string:job_id>', methods=['POST'])
def update_job(job_id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        job_title = request.form['title']
        job_description = request.form['description']
        cur.execute("UPDATE Job SET Job.Job_Title = (%s), Job.Job_Description=(%s)"
                    "WHERE job.ID = (%s)",
                    (job_title, job_description, job_id))
        mysql.connection.commit()
        return redirect(url_for('jobs_page'))


# AJAX: GET SKILLS FROM JOB DESC
@app.route('/getskills')
def get_skills():
    a = request.args.get('a', 0, type=str)
    return jsonify(parse.text_rank(a))


# TODO: IMPLEMENT OPTION TO USE EXISTING SKILLS MATRIX
# GET EXISTING SKILLS FROM DB
@app.route('/getexistingskills')
def get_existing_skills():
    a = request.args.get('a', 0, type=str)
    return jsonify(parse.text_rank(a))