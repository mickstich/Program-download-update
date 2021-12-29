from flask import Flask, request, redirect, send_file, send_from_directory
from flask.templating import render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
import zipfile

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
def is_integer(n):
    try:
        return float(n).is_integer()
    except ValueError:
        return False


class usw(db.Model):
    name=db.Column(db.String(20),primary_key=True)
    password = db.Column(db.Integer(),nullable=False)

    def __repr__(self):
        return f"Name : {self.name}, password: {self.password}"



@app.route('/', methods=['GET'])
def login():
 #   all_users= usw.query.all()
 #   print(all_users)
 #   passw=all_users[0].password
#    print(passw)
    return render_template('login.html')


@app.route('/download', methods=[ 'POST'])
def download():
    name = request.form.get("name")
    password = request.form.get("password")
    if not is_integer(password):
          return redirect('/')


#    all_users= db.session.query(usw).filter(usw.name == name, usw.password == password)
#   print(all_users)
#    invalid=True
#    for row in all_users:
#       print("ID:", row.name, "Name: ", row.password)
#        invalid=False
#   if invalid is True:
#       return redirect('/')
    filelist = os.listdir('./files/')
    return render_template('download.html', filelist=filelist)


@app.route('/download_file/', methods=['GET', 'POST'])
def download_file():
#    print(request.method)
    filename = request.form.get('filename')

    if filename:
        path = './files/' + filename
        return send_file(path, as_attachment=True)


@app.route('/download_all')
def download_all():
#    print(request.method)
    zipf = zipfile.ZipFile('All_Files.zip', 'w', zipfile.ZIP_DEFLATED)
    for files in os.listdir('./'):
        if files.endswith('.csv'):
            zipf.write(files)
    zipf.close()
    return send_file('All_Files.zip',
                     mimetype='zip',
                     attachment_filename='All_Files.zip',
                     as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
