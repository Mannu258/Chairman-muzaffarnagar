# save this as app.py
from flask import Flask,render_template,request
import os

# Get the absolute path to the sitemap.xml file
sitemap_path = os.path.abspath('sitemap.xml')
from flask import Flask, request, send_from_directory
app = Flask(__name__, static_folder='static')    

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = "12345"
db = SQLAlchemy(app)

class Details(db.Model):
    ID = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False)
    subject = db.Column(db.String(200),nullable=False)
    msg = db.Column(db.String(200),nullable=False)

    def __repr__(self) -> str:
        return f"{self.s_no} - {self.title}"
    
class Crediantials(db.Model):
    ID = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    def __repr__(self) -> str:
        return f"{self.username}"



@app.route("/", methods=['POST','GET'])
def index():
    if request.method == "POST":
        names = request.form['names']
        emails = request.form['emails']
        subjects = request.form['subjects']
        msgs = request.form['msgs']
        deatils = Details(name=names, email=emails,subject=subjects,msg=msgs)
        db.session.add(deatils)
        db.session.commit()  # Commit the changes once
        return render_template('thankyou.html')
    return render_template('index.html')

@app.route("/about", methods=['POST','GET'])
def about():
    return render_template('about.html')

@app.route("/blog", methods=['POST','GET'])
def blog():
    return render_template('blog.html')

@app.route("/sitemap.xml", methods=['GET'])
def sitemap():
    with open('sitemap.xml', 'r') as xml_file:
        xml_content = xml_file.read()
    return xml_content, 200, {'Content-Type': 'application/xml'}


@app.route("/robots.txt", methods=['GET'])
def robots_txt():
    with open('robots.txt', 'r') as txt:
        txt_content = txt.read()
    return txt_content, 200, {'Content-Type': 'text/plain'}







@app.route("/administrator",methods=['POST','GET'])
def Admin():
    if request.method == "POST":
        username = request.form['Username']
        password = request.form['password']
        admi = Crediantials.query.filter_by(username=username,password=password).first()
        if admi:
            details = Details.query.all()
            return render_template('Database.html',details=details)
        else:
            return render_template('login.html')

    return render_template('login.html')
    
     

if __name__ == '__main__':
   app.run(debug=True ,port=8000)