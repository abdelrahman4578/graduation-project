from flask import Flask,render_template,url_for,request,flash
from flask_mysqldb import MySQL
import numpy as np
import mysql.connector
import re
import matplotlib.image as mpimg
import out
import os
import random
import datetime
import asyncio
global log_in_user_email 
global user_password
log_in_user_email ,user_password=0,0
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/diagnosed_cases')
def diagnosed_cases():
    return render_template('diagnosed.html')
@app.route('/undiagnosed_cases')
def undiagnosed_cases():
    return render_template('admin.html')
@app.route('/upload_photo')
def upload_photo():
    return render_template('home.html')
@app.route('/update_profile')
def update_profile():
    return render_template('Update.html')
@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/logintask',methods = ['POST','GET'])
def login():
            mesage = ''
            if request.method == 'POST' and 'login_usermail' in request.form and 'login_userpass' in request.form:
                global log_in_user_email
                global user_password
                log_in_user_email = request.form.get("login_usermail")
                user_password = request.form.get("login_userpass")
                mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="database"
                )
                mycursor = mydb.cursor()
                mycursor.execute('SELECT * FROM users WHERE Email = %s AND Password = %s', (log_in_user_email, user_password ))
                user = mycursor.fetchone()
                mycursor.execute('SELECT * FROM admin WHERE Email = %s AND Password = %s', (log_in_user_email, user_password ))
                admin = mycursor.fetchone()
                if user:
                    return render_template('home.html')
                elif admin:
                    return render_template('admin.html')
                else:
                    flash("There is no user with this email and password")
                    return render_template('register.html')
                
@app.route('/registertask',methods = ['POST','GET'])
def registerTask():
    if request.method == 'POST':
        global user_email
        global user_pass
        user_full_name = request.form.get("FullName")
        user_email = request.form.get("Email")
        user_Address = request.form.get("Address" )
        user_pass = request.form.get("Password")
        confirm_user_pass = request.form.get("ConfirmPassword")
        if user_full_name and user_email and user_Address and user_pass and confirm_user_pass:
            if confirm_user_pass == user_pass:
                if len(user_pass) >= 8: 
                    mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="database"
                    )
                    mycursor = mydb.cursor()
                    sql = "INSERT INTO users (FullName,Address,Email,Password) VALUES (%s, %s, %s, %s)"
                    val = (user_full_name,user_Address,user_email,user_pass)
                    mycursor.execute(sql,val)
                    mydb.commit()
                    mycursor.execute('SELECT id FROM users WHERE Email = %s AND Password = %s', (user_email, user_pass ))
                    user_id = mycursor.fetchone()
                    for i in user_id:
                        os.makedirs(f'static/database/{i}')
                        os.makedirs(f'static/database/{i}/results')
                        os.makedirs(f'static/database/{i}/images')
                    return render_template('home.html')
                else:
                    flash("Password must be at least 8 character long")
                    return(render_template('register.html'))
            else:
                flash("password and confirm password aren't the same")
                return(render_template('register.html'))
        else:
            flash("You must fill all boxes!")
            return render_template('register.html')
    
@app.route('/updatetask',methods = ['POST','GET'])
def updatetask():
    if request.method == 'POST':
        U_user_full_name = request.form.get('FullName')
        U_user_Address = request.form.get('Address')
        U_user_email = request.form.get('Email')
        U_user_pass = request.form.get('Password')
        U_confirm_user_pass = request.form.get('ConfirmPassword')
        if U_user_full_name and U_user_Address and U_user_email and U_user_pass and U_confirm_user_pass:
            if U_confirm_user_pass == U_user_pass:
                if len(U_user_pass) >= 8: 
                    if log_in_user_email and user_password:
                        mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="database"
                        )
                        mycursor = mydb.cursor()
                        mycursor.execute('SELECT id FROM users WHERE Email = %s AND Password = %s', (log_in_user_email, user_password ))
                        user_id = mycursor.fetchone()
                        for i in user_id:
                            mycursor.execute('UPDATE users SET FullName = %s WHERE id = %s',(U_user_full_name,i))
                            mycursor.execute('UPDATE users SET Address = %s WHERE id = %s',(U_user_Address,i))
                            mycursor.execute('UPDATE users SET Email = %s WHERE id = %s',(U_user_email,i))
                            mycursor.execute('UPDATE users SET Password = %s WHERE id = %s',(U_user_pass,i))
                        mydb.commit()
                        return render_template('home.html')
                    else:
                        mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="database"
                        )
                        mycursor = mydb.cursor()
                        mycursor.execute('SELECT id FROM users WHERE Email = %s AND Password = %s', (user_email, user_pass ))
                        user_id = mycursor.fetchone()
                        for i in user_id:
                            mycursor.execute('UPDATE users SET FullName = %s WHERE id = %s',(U_user_full_name,i))
                            mycursor.execute('UPDATE users SET Address = %s WHERE id = %s',(U_user_Address,i))
                            mycursor.execute('UPDATE users SET Email = %s WHERE id = %s',(U_user_email,i))
                            mycursor.execute('UPDATE users SET Password = %s WHERE id = %s',(U_user_pass,i))
                        mydb.commit()
                        return render_template('home.html')
                        
                else:
                    flash("Password must be at least 8 character long")
                    return(render_template('update.html'))
            else:
                flash("password and confirm password aren't the same")
                return(render_template('update.html'))
        else:
            flash("You must fill all data!")
            return render_template('update.html')

@app.route('/upload',methods = ['POST','GET'])
def upload():
    image_file = request.files['image']
    filename = image_file.filename
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="database"
            )
    mycursor = mydb.cursor()
    if log_in_user_email !=0 and user_password !=0:
        mycursor.execute('SELECT id FROM users WHERE Email = %s AND Password = %s', (log_in_user_email, user_password ))
        user_id = mycursor.fetchone()
        now = datetime.datetime.now()
        now = now.date()
        for i in user_id:
            image_file = image_file.save(f'static/database/{i}/images/{filename}')
            sql = "INSERT INTO xray (X_Ray ,userid, date) VALUES (%s, %s,%s)"
            val = (f'{i}/images/{filename}',i,now)
            mycursor.execute(sql,val)
            mydb.commit()
    else:
        mycursor.execute('SELECT id FROM users WHERE Email = %s AND Password = %s', (user_email, user_pass ))
        user_id = mycursor.fetchone()
        now = datetime.datetime.now()
        now = now.date()
        for i in user_id:
            image_file = image_file.save(f'static/database/{i}/images/{filename}')
            sql = "INSERT INTO xray (X_Ray ,userid, date) VALUES (%s, %s,%s)"
            val = (f'{i}/images/{filename}',i,now)
            mycursor.execute(sql,val)
            mydb.commit()
    flash('The result will be sent in the empty area below after the admin approve the XRay')
    return render_template('home.html')

@app.route('/message', methods=['POST','GET'])
def message():
    userdata=''
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="database")
    mycursor = mydb.cursor()
    query = 'SELECT  t2.X_Ray,t2.date,t2.text FROM users t1 LEFT JOIN xray t2 ON t1.id = t2.userid WHERE t2.statue = "done" And t1.Email = %s And t1.Password = %s'
    mycursor.execute(query,(log_in_user_email,user_password))
    users = mycursor.fetchall()
    if users:
        for user in users:
            message = f"the XRay you uploaded in {user[1]} \n the result: {user[2]} \n \n"
            userdata += message
    else:
        userdata = "No X-Ray results found for this user"
    return render_template('home.html', userdata=userdata)

@app.route('/admin',methods = ['POST','GET'])
def admin():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="database")
    mycursor = mydb.cursor()
    query = 'SELECT t1.FullName,t1.Email,t1.id, t2.userid,t2.X_Ray,t2.date,t2.id FROM users t1 LEFT JOIN xray t2 ON t1.id = t2.userid WHERE t2.diagnosis = "undiagnosed" And t2.x_ray != "NULL"'
    mycursor.execute(query)
    users = mycursor.fetchall()
    return render_template('admin.html', users=users)

@app.route('/api',methods = ['POST','GET'])
def api():
    if request.method == 'POST':
        user_image = request.form["user_image"]
        user_id = request.form["user_ID"]
        id = request.form["ID"]
        button_value = request.form['button_value']
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="database")
        mycursor = mydb.cursor()
        if button_value == "acc":
            image_file,title = out.show_visual_img(f'static/database/{user_image}')
            diagnosis_parts = title.split(': ')
            diagnosis_value = diagnosis_parts[1].split()[0]
            if diagnosis_value == 'PNEUMONIA':
                message = "you will live for 10 days"
            elif diagnosis_value == 'COVID19':
                message = "gg you will day"
            else:
                message = "man you are so lucky"
            filename = user_image.replace(f'{user_id}/images/', "")
            image_file = image_file.save(f'static/database/{user_id}/results/{filename}')
            mycursor.execute('UPDATE xray SET result = %s,diagnosis = %s ,text = %s WHERE id = %s',(f'{user_id}/results/{filename}',title,message,id))
            mydb.commit()
        elif button_value == "rej":
            os.remove(f'static/database/{user_image}')
            id = (id,) 
            mycursor.execute('DELETE FROM xray WHERE id = %s',(id))
            mydb.commit()
        return render_template('admin.html')
    
@app.route('/diagnosed',methods = ['POST','GET'])
def diagnosed():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="database")
    mycursor = mydb.cursor()
    query = 'SELECT t1.FullName,t1.Email,t1.id,t2.userid,t2.X_Ray,t2.result,t2.diagnosis,t2.text,t2.date,t2.id FROM users t1 LEFT JOIN xray t2 ON t1.id = t2.userid WHERE t2.diagnosis != "undiagnosed" And t2.statue != "done"'
    mycursor.execute(query)
    users = mycursor.fetchall()
    return render_template('diagnosed.html', users=users)


    
        
@app.route('/done',methods = ['POST','GET'])
def done():
    user_image = request.form["user_image"]
    button_value = request.form['button_value']
    message = request.form["textbox"]
    user_id = request.form["user_ID"]
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="database")
    mycursor = mydb.cursor()
    if button_value == "done":
         mycursor.execute('UPDATE xray SET statue = %s WHERE id = %s',('done',user_id))
         mycursor.execute('UPDATE xray SET text = %s WHERE id = %s',(message,user_id))
         mydb.commit()
    return render_template('diagnosed.html')

@app.route('/data',methods = ['POST','GET'])
def taple():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="database")
    mycursor = mydb.cursor()
    query = 'SELECT t1.FullName,t1.Email,t2.X_Ray,t2.date,t2.diagnosis,t2.result FROM users t1 LEFT JOIN xray t2 ON t1.id = t2.userid WHERE  t2.statue = "done"'
    mycursor.execute(query)
    users = mycursor.fetchall()
    return render_template('data.html',users=users)

if __name__ == "__main__":
    app.run(debug=True)