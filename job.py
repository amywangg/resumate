
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
    cur.execute("SELECT * FROM Job")
    data = cur.fetchall()
    cur.close()
    return render_template('job/jobs.html', title="Jobs", jobs=data)


# CREATE JOB
# GET: get skills matrix if use existing, POST: post new job and skills
@job.route('/job/create', methods=['GET', 'POST'])
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

        return redirect(url_for('job.jobs_page'))
        # return redirect('/job/create/' + str(cur.lastrowid))

    return render_template('create-job.html', title="Create Job")


# DELETE JOB
@job.route('/job/delete/<string:job_id>', methods=['GET'])
def delete_job(job_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT FROM Job WHERE ID=%s",[job_id])
    folder_id = cur.fetchall()[0]['Folder_ID']
    cur.execute("DELETE FROM Job WHERE ID=%s", [job_id])
    mysql.connection.commit()

    # TODO: delete folder from drive
    drive.deleteFolder(folder_id)
    return redirect(url_for('job.jobs_page'))


# UPDATE JOB
@job.route('/job/update/<string:job_id>', methods=['POST'])
def update_job(job_id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        job_title = request.form['title']
        job_description = request.form['description']
        cur.execute("UPDATE Job SET Job.Job_Title = (%s), Job.Job_Description=(%s)"
                    "WHERE job.ID = (%s)",
                    (job_title, job_description, job_id))
        mysql.connection.commit()
        return redirect(url_for('job.jobs_page'))


# AJAX: GET SKILLS FROM JOB DESC
@job.route('/getskills')
def get_skills():
    a = request.args.get('a', 0, type=str)
    return jsonify(parse.text_rank(a))

# TODO: IMPLEMENT OPTION TO USE EXISTING SKILLS MATRIX
# GET EXISTING SKILLS FROM DB
@job.route('/getexistingskills')
def get_existing_skills():
    a = request.args.get('a', 0, type=str)
    return jsonify(parse.text_rank(a))