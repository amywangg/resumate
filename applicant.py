import tempfile, ast, parse, drive
from flask import Flask, request, render_template, url_for, redirect, jsonify, Blueprint, json
from resumate import MySQL
from pyresparser import ResumeParser
from flask import current_app as app
from werkzeug.utils import secure_filename
import os

mysql = MySQL()

################################# APPLICANT ROUTES #######################################
applicant = Blueprint('applicant', __name__, template_folder='templates/applicant')


@applicant.route('/applicant', methods=['GET'])
def applicant_page():
    # need to display all jobs, display matches,
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Job ORDER BY ID desc")
    data = cur.fetchall()
    cur.close()
    return render_template('applicant/jobs-apply.html', title="Applicant", jobs=data)


# UPLOAD AND PARSE RESUME
@applicant.route('/applicant/<string:job_id>', methods=['GET','POST'])
def apply(job_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Job WHERE ID =(%s)",[job_id])
    data = cur.fetchall()
    print(data[0]['Folder_ID'])
    folder_id = data[0]['Folder_ID']
    cur.execute("SELECT Skills FROM Skills s INNER JOIN Job j ON s.ID = j.Skills_ID WHERE j.ID =(%s)",[job_id])
    job_skills = cur.fetchall()
    job_skills = ast.literal_eval(job_skills[0]['Skills'])
    skilltext = ''
    for skill in job_skills:
        skilltext+= skill + ', '
    skilltext = skilltext.rstrip(', ')

    # get skills from resume
    if request.method == 'POST':
        # TODO: change resume collection to handle upload
        resume = request.files['resume']
        filename = secure_filename(resume.filename)
        resume.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resumedata = ResumeParser('resumetemp/' + resume.filename).get_extracted_data()
        name = resumedata['name']
        email = "none"

        if resumedata['email'] != None:
            email = resumedata['email']
        phone = resumedata['mobile_number']
   
        skills = json.dumps(resumedata['skills'])
        # upload file to drive
        file_id = drive.uploadFile(resume, folder_id)
 
        cur.execute("INSERT INTO Applicant (Name, Email, Phone_Number, Skills, Resume) VALUES (%s,%s,%s,%s,%s)",
        (name, email, phone, skills, file_id))
        app_id = cur.lastrowid

        # find applicant and job matching skills
        matched_skills = parseSkills.match_skills(resumedata['skills'], job_skills)
        score = len(matched_skills)
        matched_skills = json.dumps(matched_skills)
        cur.execute("INSERT INTO Rankings (Applicant_ID, Job_ID, Score, Matched_Skills) VALUES (%s,%s,%s,%s)",
                (app_id, job_id, score, matched_skills))

        mysql.connection.commit()

    return render_template('applicant/upload.html', title="Apply", jobs=data, skills = skilltext)



@applicant.route('/summary')
def summary_page():

    return render_template('applicant/applicant.html', title="Applicant")





# TODO: Implement file upload on applicant side
# @app.route('/upload/<path:filename>', methods=['GET', 'POST'])
# def download(filename):
#     upload = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
#     return send_from_directory(directory=uploads, filename=filename)

# if 'resume' not in request.files:
#     return redirect('/')
#
# file = request.files['resume']
# if not file:
#     return redirect('/')
#
# filename = secure_filename(file.filename)
#
# fp = tempfile.TemporaryFile()
# ch = file.read()
# fp.write(ch)
# fp.seek(0)
#
# mime_type = request.headers['Content-Type']
# uploadToDrive.insert_file(filename, mime_type, fp)

    return redirect(url_for('summary_page'))

# if 'resume' in request.files:
#     resume = request.files['resume']

