import tempfile
import uploadToDrive, readFromDrive
from flask import Flask, request, render_template, url_for, redirect
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Fires-123'
app.config['MYSQL_DB'] = 'resumate'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

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
@app.route('/job/create', methods=['GET','POST'])
def create_job():
    if request.method == 'POST':
        job_title = request.form['title']
        job_description = request.form['description']
        job_status = "open"
        # connect to sql execute queries
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Job (Job_Title, Job_Description, Job_Status) VALUES (%s,%s,%s)",
                    (job_title, job_description, job_status))
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
                    (job_title,job_description,job_id))
        mysql.connection.commit()
        return redirect(url_for('jobs_page'))


# CREATE SKILLS
@app.route('/job/create/<string:job_id>', methods=['POST', 'GET'])
def link_skills(job_id):
    use_existing = False

    if request.method == 'POST':
        Skills = request.form['skills']
        Title = request.form['skills_title']
        # connect to sql execute queries

        cur = mysql.connection.cursor()
        if use_existing:
            Skills_ID = request.form['Skills_ID']
            # if using an existing skills record, add Skills.ID to Job's Skills_ID
            cur.execute("UPDATE Job SET Skills_id=%s WHERE ID=%s", (Skills_ID, int(job_id)))
        else:
            cur.execute("INSERT INTO Skills (Title, Skills) VALUES (%s,%s)", (Title, Skills))
            # once inserted new Skills record, link to Job
            cur.execute("UPDATE Job j INNER JOIN Skills s ON s.Title = (%s) set j.Skills_ID = s.ID", (Title))

        mysql.connection.autocommit()


################################# APPLICANT ROUTES #######################################

@app.route('/applicant')
def applicant_page():
    return render_template('applicant/jobs-apply.html', title="Applicant")


@app.route('/apply')
def apply_page():
    return render_template('applicant/upload.html', title="Apply")


@app.route('/summary')
def summary_page():
    readFromDrive.readFromDrive()
    return render_template('applicant/applicant.html', title="Applicant")


@app.route("/handleUpload", methods=['GET', 'POST'])
def handleFileUpload():
    if 'resume' not in request.files:
        return redirect('/')

    file = request.files['resume']
    if not file:
        return redirect('/')

    filename = secure_filename(file.filename)

    fp = tempfile.TemporaryFile()
    ch = file.read()
    fp.write(ch)
    fp.seek(0)

    mime_type = request.headers['Content-Type']
    uploadToDrive.insert_file(filename, mime_type, fp)

    return redirect(url_for('summary_page'))

    # if 'resume' in request.files:
    #     resume = request.files['resume']
    #     if resume.filename != '':
    #         print(resume.content)
    #         uploadToDrive.insert_file(resume, "Resumes")


if __name__ == '__main__':
    app.run(debug=True)
