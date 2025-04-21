import os
import sys
from flask import Flask, render_template, request, redirect, url_for
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from db import get_connection, init_db, get_rider_by_id, get_laps_by_rider, insert_lap, get_all_riders

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/leaderboard')
def leaderboard():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM riders ORDER BY best_lap ASC")
    riders = cursor.fetchall()
    return render_template('leaderboard.html', riders=riders)

@app.route('/rider/<int:rider_id>')
def rider_profile(rider_id):
    rider = get_rider_by_id(rider_id)
    rider_laps = get_laps_by_rider(rider_id)
    return render_template('rider.html', rider=rider, rider_laps=rider_laps)

@app.route('/add_lap', methods=['GET', 'POST'])
def add_lap():
    if request.method == 'POST':
        rider_id = request.form['rider_id']
        lap_time = request.form['lap_time']
        insert_lap(rider_id, lap_time)
        return redirect(url_for('leaderboard'))

    riders = get_all_riders()
    return render_template('add_lap.html', riders=riders)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)