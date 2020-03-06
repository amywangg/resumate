from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', title="Home")

@app.route('/about')
def about_page():
    return render_template('about.html', title="ABOUT")

@app.route('/about')
def about_page():
    return render_template('about.html', title="Main")

@app.route('/postings/create')
def about_page():
    return render_template('about.html', title="Main")

@app.route('/postings/view')
def about_page():
    return render_template('about.html', title="Main")

@app.route('/postings/delete')
def about_page():
    return render_template('about.html', title="Main")

@app.route('/postings')
def about_page():
    return render_template('about.html', title="Main")

if __name__ == '__main__':
    app.run(debug=True)

