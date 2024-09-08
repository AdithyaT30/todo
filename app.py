from flask import Flask,render_template,request,redirect
import MySQLdb

app=Flask(__name__)

db=MySQLdb.connect(
    host="localhost",
    user="root",
    password="root",
    database="emp"
)
cursor=db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM tasks")
    tasks=cursor.fetchall()
    return render_template("index.html",tasks=tasks)

@app.route('/add',methods=['GET','POST'])
def add_task():
    task_content=request.form['content']
    if task_content:
        cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (task_content,))
        db.commit()
    return redirect('/')

@app.route('/update/<int:id>')
def update_task(id):
    cursor.execute("SELECT status FROM tasks WHERE id = %s", (id,))
    current_status=cursor.fetchone()[0]
    new_status=1 if current_status ==0 else 0
    cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (new_status, id))
    db.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(id):
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    db.commit()
    return redirect('/')
        

if __name__=='__main__':
    app.run(debug=True)