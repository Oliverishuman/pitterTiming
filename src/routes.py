from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from user import User
from db import get_connection, get_rider_by_id, get_laps_by_rider, insert_lap, get_all_riders

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return redirect(url_for('routes.login'))

@routes.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_by_username(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('routes.dashboard'))
        else:
            error = "Invalid username or password"
    return render_template('login.html', error=error)

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        User.create(username, hashed_password)
        return redirect(url_for('routes.login'))
    return render_template('register.html')

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))

@routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@routes.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        new_username = request.form['username']
        User.update_profile(current_user.id, new_username)
        return redirect(url_for('routes.dashboard'))
    return render_template('edit_profile.html', user=current_user)

@routes.route('/leaderboard')
@login_required
def leaderboard():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM riders ORDER BY best_lap ASC")
    riders = cursor.fetchall()
    return render_template('leaderboard.html', riders=riders)

@routes.route('/rider/<int:rider_id>')
def rider_profile(rider_id):
    rider = get_rider_by_id(rider_id)
    rider_laps = get_laps_by_rider(rider_id)
    return render_template('rider.html', rider=rider, rider_laps=rider_laps)

@routes.route('/add_lap', methods=['GET', 'POST'])
@login_required
def add_lap():
    if request.method == 'POST':
        rider_id = request.form['rider_id']
        lap_time = request.form['lap_time']
        insert_lap(rider_id, lap_time)
        return redirect(url_for('routes.leaderboard'))

    riders = get_all_riders()
    return render_template('add_lap.html', riders=riders)