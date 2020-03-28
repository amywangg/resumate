
import parse, drive
from flask import Flask, request, render_template, url_for, redirect, jsonify, Blueprint, json
from resumate import MySQL

mysql = MySQL()

################################# JOB ROUTES #######################################
job = Blueprint('job', __name__, template_folder='templates/job')


# GET ALL JOBS
@job.route('/jobs', methods=['GET'])
def jobs_page():
    # need to display all jobs, display matches,
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Job J INNER JOIN Skills S ON J.Skills_ID = S.ID ")
    data = cur.fetchall()
    for x in data:
        cur.execute(
            "SELECT Count(ID) FROM Applicant A INNER JOIN Rankings R ON A.ID=R.Applicant_ID AND R.Job_ID=(%s)", [x['ID']])
        count = cur.fetchall()    
        x['Count'] = count[0]['Count(ID)']
        x['Skills']= x['Skills'].replace('[','')
        x['Skills']= x['Skills'].replace(']','')
        x['Skills']= x['Skills'].replace('"','')

    cur.close()
    return render_template('job/jobs.html', title="Jobs", jobs=data)


# CREATE JOB
# GET: get skills matrix if use existing, POST: post new job and skills
@job.route('/job/create', methods=['GET', 'POST'])
def create_job():
    if request.method == 'POST':
        job_title = request.form['title']
        job_description = request.form['description']
        job_status = "open"

        skill_name = request.form['skillname']
        skills = request.form['skilltag']

        # connect to sql execute queries
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO Skills (Title, Skills) VALUES (%s,%s)", (skill_name, skills))
        cur.execute("INSERT INTO Job (Job_Title, Job_Description, Job_Status, Skills_ID) VALUES (%s,%s,%s,%s)",
                    (job_title, job_description, job_status, cur.lastrowid))
        job_id = cur.lastrowid

       # Create a folder in the drive with the job id return folder id for future use
        folder_id = drive.createFolder(str(job_id) + "-" + job_title)
        cur.execute("UPDATE Job SET Folder_ID = (%s)"
                    "WHERE job.ID = (%s)",
                    (folder_id, job_id))
        mysql.connection.commit()

        return redirect(url_for('job.jobs_page'))
        # return redirect('/job/create/' + str(cur.lastrowid))

    return render_template('create-job.html', title="Create Job")


# DELETE JOB
@job.route('/job/delete/<string:job_id>', methods=['GET'])
def delete_job(job_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT Skills_ID FROM Job WHERE ID=%s", [job_id])
    skills_id = cur.fetchall()[0]['Skills_ID']
    cur.execute("DELETE FROM Job WHERE ID=%s", [job_id])
    cur.execute("DELETE FROM Skills WHERE ID=%s", [skills_id])
    cur.execute("DELETE FROM resumate.Match WHERE Job_ID=%s", [job_id])
    mysql.connection.commit()

    return redirect(url_for('job.jobs_page'))


# UPDATE JOB
@job.route('/job/update/<string:job_id>', methods=['POST'])
def update_job(job_id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        job_title = request.form['title']
        job_description = request.form['description']
        job_status = request.form['status']
        cur.execute("UPDATE Job SET Job.Job_Title = (%s), Job.Job_Description=(%s), Job.Job_Status=(%s)"
                    "WHERE job.ID = (%s)",
                    (job_title, job_description, job_status, job_id))
        mysql.connection.commit()
        return redirect(url_for('job.jobs_page'))


# UPDATE SKILL
@job.route('/skill/update/<string:skill_id>', methods=['GET','POST'])
def update_skill(skill_id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form['skilltitle'+skill_id]
        skills = request.form['editskilltag'+skill_id]
        skills= json.loads(skills)
        skillist = []
        for x in skills:
            skillist.append(x['value'])
        cur.execute("UPDATE Skills SET Title = (%s), Skills=(%s)"
                    "WHERE ID = (%s)",
                    (title, json.dumps(skillist), skill_id))
        mysql.connection.commit()
        return redirect(url_for('job.jobs_page'))

# AJAX: GET SKILLS FROM JOB DESC
@job.route('/popskills')
def pop_skills():
    a = request.args.get('a', 0, type=str)
    cur = mysql.connection.cursor()
    cur.execute("SELECT Skills FROM Skills WHERE ID=%s", [a])
    skills = cur.fetchall()
    skills=json.loads(skills[0]['Skills'])
    return jsonify(skills)

# AJAX: GET SKILLS FROM JOB DESC
@job.route('/getskills')
def get_skills():
    a = request.args.get('a', 0, type=str)
    return jsonify(parse.text_rank(a))