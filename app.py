# set FLASK_APP=app.py
# set FLASK_DEBUG=1
# flask run

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy 
from sklearn.externals import joblib
import numpy as np


app = Flask(__name__, template_folder='templates')
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/db_sales'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nama = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, nama, email, phone):
        self.nama = nama
        self.email = email
        self.phone = phone
    
    def serialize(self):
        return {"id": self.id,
                "nama": self.nama,
                "email": self.email,
                "phone": self.phone}   


@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", employees = all_data, no = '1')


@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Data(nama, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Insert Successfully")
        return redirect(url_for('Index'))

@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.nama = request.form['nama']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']      

        db.session.commit()
        flash("Employee Update Successfully")

        return redirect(url_for('Index'))  

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))


# =================================================== REST FULL API ================================================    
@app.route('/employeeApi', methods = ['GET', 'POST'])
def employeeFunction():
    if request.method == 'GET':
        return getEmployee()

    elif request.method == 'POST':
        nama = request.args.get('nama', '')
        email = request.args.get('email', '')
        phone = request.args.get('phone', '')
        return addEmployee(nama, email, phone)


@app.route('/employeeApi/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def employeeFunctionId(id):
    if request.method == 'GET':
        return getEmployeeId(id)

    elif request.method == 'PUT':
        nama = request.args.get('nama', '')
        email = request.args.get('email', '')
        phone = request.args.get('phone', '')
        return updateEmployee(id, nama, email, phone)

    elif request.method == 'DELETE':
        return deleteEmployee(id)

#--------------
 # FUNCTION API           
#--------------

def getEmployee():
    employees = db.session.query(Data).all()
    return jsonify(list(map(lambda dev: dev.serialize(), employees)))

def getEmployeeId(id):
    employees = Data.query.get(id)
    return jsonify(employees.serialize())

def addEmployee(nama, email, phone):
    addemployee = Data(nama=nama, email=email, phone=phone)
    db.session.add(addemployee)
    db.session.commit()
    return jsonify(addemployee.serialize())

def updateEmployee(id, nama, email, phone):
    updateemployee = Data.query.get(id)
    updateemployee.nama = nama
    updateemployee.email = email    
    updateemployee.phone = phone
    db.session.commit()
    return jsonify(message = "Berhasil diupdate")

def deleteEmployee(id):
    deleteemployees = Data.query.get(id)
    db.session.delete(deleteemployees)
    db.session.commit()
    return jsonify(message = "Berhasil dihapus")

# ======================================= MACHINE LEARNING MODEL ==========================

@app.route('/machinelearning', methods = ['POST'])
def result():
    inputA = request.args.get('inputA', '')
    to_predict_listA=list(inputA)
    to_predict_list = list(map(float, to_predict_listA))
    result = float(ValuePredictor(to_predict_list))
    return jsonify(hasil = result)
        
        

def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(-1,1)
    loaded_model = joblib.load('model.sav')
    result = loaded_model.predict(to_predict)
    return result[2]



if __name__=="__main__":
    app.run(debug=True)