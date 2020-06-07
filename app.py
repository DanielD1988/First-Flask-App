from flask import Flask,render_template,request,redirect,url_for,flash
from Database import UseDatabase # Database class deals with mysql connection
import mysql.connector 
app = Flask(__name__)

app.secret_key = "abc" #used to create session

#Make connection to database using dictionary
app.config['dbconfig'] = {  'host': '127.0.0.1', 
              'user': 'vsearch',              
              'password': 'pass',              
              'database': 'vsearchlogDB', }
#-------------------------Main Menu
@app.route('/')
def mainMenu() -> 'none':
    return render_template('mainMenu.html')
#---------add employee form
@app.route('/addRecord')
def display_employee_form() -> 'html':
    return render_template('addEmployee.html')
#------------------------insert in to employee table and redirect back to form
@app.route('/insert', methods =['POST'])
def add_employee() -> 'none':
    with UseDatabase(app.config['dbconfig']) as cursor:#connects to Database class  NOTE search path connects classes
        if request.method == "POST":
            
             #post variables
             fName = request.form['fName']
             lName = request.form['lName']
             address = request.form['address']
             phone = request.form['phone']
             title = request.form['title']
             age = request.form['age']
             pps = request.form['pps']
         
             #excute statement so data goes in to the employee table
             cursor.execute("INSERT INTO employee(firstName, lastName, address, phoneNumber,jobTitle, age, ppsNumber) values(%s, %s, %s, %s, %s, %s, %s)",(fName,lName,address,phone,title,age,pps))      
             flash("The record was added")
             return redirect(url_for('display_employee_form'))#return to method
        else:
             return redirect(url_for('display_employee_form'))
#---------------------------------------------------------------------
#------------------------------------------fill edit employee form

#get list of data from database for updating a record
@app.route('/editData')
def getEditData() -> 'html':
   with UseDatabase(app.config['dbconfig']) as cursor: 
    cursor.execute("select * from employee")
    data = cursor.fetchall()#data returned in a tupple
    return render_template('editEmployee.html',data = data)#send tupple to editEmployee.html form
    
#----------------------------------------update after employee edit
@app.route('/updateRecord',methods =['POST'])
def update_employee():
    
    with UseDatabase(app.config['dbconfig']) as cursor: 
        if request.method == "POST":
            id = request.form['id']
            fName = request.form['fName']
            lName = request.form['lName']
            address = request.form['address']
            phone = request.form['phone']
            title = request.form['title']
            age = request.form['age']
            pps = request.form['pps']
          
            cursor.execute("""
            update employee
            set firstName=%s, lastName=%s,address=%s,phoneNumber=%s,jobTitle=%s,age=%s,ppsNumber=%s
            where id=%s
            """,(fName,lName,address,phone,title,age,pps,id))
            flash("The record was updated")
            return redirect(url_for('getEditData'))#return to method

#------------------------------get data from database for deleting an employee record
@app.route('/deleteData')
def getDeleteData() -> 'html':
   with UseDatabase(app.config['dbconfig']) as cursor: 
    cursor.execute("select * from employee")
    data = cursor.fetchall()#data returned in a tupple
    return render_template('deleteEmployee.html',data = data)#send tupple to deleteEmployee.html form
#-----------------------------------delete employee row from database
@app.route('/deleteRecord',methods =['POST'])
def delete_employee():
    
    with UseDatabase(app.config['dbconfig']) as cursor: 
        if request.method == "POST":
            id = request.form['id']
            query = "delete from employee WHERE id = %s" % (id)
            cursor.execute(query)
            flash("The record was deleted")
            return redirect(url_for('getDeleteData'))#return to method

if __name__ == '__main__': 
   app.run()
