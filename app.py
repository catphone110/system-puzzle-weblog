import datetime
import os
import psycopg2

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def index():
    # Connect to database
    conn = psycopg2.connect(host='db',
                            database=os.environ['POSTGRES_DB'],
                            user=os.environ['POSTGRES_USER'],
                            password=os.environ['POSTGRES_PASSWORD'])
    cur = conn.cursor()

    # Get number of all GET requests
    sql_all = """SELECT COUNT(*) FROM weblogs;"""
    cur.execute(sql_all)
    all = cur.fetchone()[0]

    # Get number of all local succesful requests
    sql_success_local = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'local\' AND status LIKE \'2__\';"""
    cur.execute(sql_success_local)
    success_local = cur.fetchone()[0]
    
    # Get number of all remote succesful requests
    sql_success_remote= """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'local\' AND status LIKE \'2__\';"""
    cur.execute(sql_success_remote)
    success_remote = cur.fetchone()[0]

    # Determine rate if there was at least one request
    rate_local = "No entries yet!"
    rate_remote = "No entries yet!"
    
    if all != 0:
        local_rate = str(round((success_local/all)*100))
        remote_rate = str(round((success_remote/all)*100))
    
    return render_template('index.html', local_rate=local_rate, remote_rate=remote_rate)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

