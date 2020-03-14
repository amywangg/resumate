import tempfile
from driveAPI import readFromDrive, uploadToDrive
from flask import Flask, request, render_template, url_for, redirect, jsonify, Blueprint, json
from resumate import MySQL
from pyresparser import ResumeParser

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
    # get skills from resume
    if request.method == 'POST':
        # TODO: change resume collection to handle upload
        resume = request.files['resume']
        resumedata = ResumeParser('resumetemp/' + resume.filename).get_extracted_data()
        name = resumedata['name']
        email = "none"

        if resumedata['email'] != None:
            email = resumedata['email']
        phone = resumedata['mobile_number']
   
        skills = json.dumps(resumedata['skills'])
 
        cur.execute("INSERT INTO Applicant (Name, Email, Phone_Number, Skills) VALUES (%s,%s,%s,%s)",
        (name, email, phone, skills))
        app_id = cur.lastrowid
        cur.execute("SELECT Skills FROM Skills s INNER JOIN Job j ON s.ID = j.Skills_ID WHERE j.ID =(%s)",[job_id])
        job_skills = cur.fetchall()[0]

        # find applicant and job matching skills
        matched_skills = match_skills(resumedata['skills'], job_skills)
        score = len(matched_skills)
        matched_skills = json.dumps(matched_skills)
        cur.execute("INSERT INTO Rankings (Applicant_ID, Job_ID, Score, Matched_Skills) VALUES (%s,%s,%s,%s)",
                (app_id, job_id, score, matched_skills))

        mysql.connection.commit()

    return render_template('applicant/upload.html', title="Apply", jobs=data)



@applicant.route('/summary')
def summary_page():
    readFromDrive.readFromDrive()
    return render_template('applicant/applicant.html', title="Applicant")




# TODO: Implement file upload on applicant side
@applicant.route("/handleUpload", methods=['GET', 'POST'])
def handleFileUpload():

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

def match_skills(app_skills, job_skills):
    matches = []
    for word in job_skills:
        if any(word.lower() in s.lower() for s in app_skills):
            matches.append(word)
    return matches