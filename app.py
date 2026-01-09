import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuration for different environments
if os.environ.get('VERCEL'):
    # Vercel production environment
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///job_portal.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    # Local development environment
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'job_seeker', 'employer', 'admin'
    full_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    jobs = db.relationship('Job', backref='employer', lazy=True)
    applications = db.relationship('Application', backref='applicant', lazy=True)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    salary_min = db.Column(db.Float)
    salary_max = db.Column(db.Float)
    location = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='open')  # 'open', 'closed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    applications = db.relationship('Application', backref='job', lazy=True)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'rejected'

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    def decorator(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'danger')
                return redirect(url_for('login'))
            
            user = User.query.get(session['user_id'])
            if user.role not in allowed_roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        role = request.form['role']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return render_template('register.html')
        
        password_hash = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=password_hash, 
                       full_name=full_name, role=role)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    
    if user.role == 'job_seeker':
        jobs = Job.query.filter_by(status='open').all()
        applications = Application.query.filter_by(applicant_id=user.id).all()
        return render_template('job_seeker_dashboard.html', user=user, jobs=jobs, applications=applications)
    
    elif user.role == 'employer':
        posted_jobs = Job.query.filter_by(employer_id=user.id).all()
        total_applications = sum(len(job.applications) for job in posted_jobs)
        return render_template('employer_dashboard.html', user=user, jobs=posted_jobs, total_applications=total_applications)
    
    elif user.role == 'admin':
        total_users = User.query.count()
        total_jobs = Job.query.count()
        total_applications = Application.query.count()
        users = User.query.all()
        jobs = Job.query.all()
        return render_template('admin_dashboard.html', user=user, 
                             total_users=total_users, total_jobs=total_jobs, 
                             total_applications=total_applications, users=users, jobs=jobs)

@app.route('/jobs')
def jobs():
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    
    query = Job.query.filter_by(status='open')
    
    if search:
        query = query.filter(Job.title.contains(search) | Job.description.contains(search))
    
    if location:
        query = query.filter(Job.location.contains(location))
    
    jobs = query.all()
    return render_template('jobs.html', jobs=jobs, search=search, location=location)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_detail.html', job=job)

@app.route('/apply/<int:job_id>', methods=['POST'])
@login_required
@role_required('job_seeker')
def apply_job(job_id):
    user = User.query.get(session['user_id'])
    job = Job.query.get_or_404(job_id)
    
    existing_application = Application.query.filter_by(
        job_id=job_id, applicant_id=user.id
    ).first()
    
    if existing_application:
        flash('You have already applied for this job!', 'warning')
    else:
        application = Application(job_id=job_id, applicant_id=user.id)
        db.session.add(application)
        db.session.commit()
        flash('Application submitted successfully!', 'success')
    
    return redirect(url_for('job_detail', job_id=job_id))

@app.route('/post_job', methods=['GET', 'POST'])
@login_required
@role_required('employer')
def post_job():
    if request.method == 'POST':
        user = User.query.get(session['user_id'])
        
        new_job = Job(
            title=request.form['title'],
            company_name=request.form['company_name'],
            description=request.form['description'],
            salary_min=float(request.form['salary_min']) if request.form['salary_min'] else None,
            salary_max=float(request.form['salary_max']) if request.form['salary_max'] else None,
            location=request.form['location'],
            employer_id=user.id
        )
        
        db.session.add(new_job)
        db.session.commit()
        
        flash('Job posted successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('post_job.html')

@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
@role_required('employer')
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    user = User.query.get(session['user_id'])
    
    if job.employer_id != user.id:
        flash('You can only edit your own jobs!', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        job.title = request.form['title']
        job.company_name = request.form['company_name']
        job.description = request.form['description']
        job.salary_min = float(request.form['salary_min']) if request.form['salary_min'] else None
        job.salary_max = float(request.form['salary_max']) if request.form['salary_max'] else None
        job.location = request.form['location']
        job.status = request.form['status']
        
        db.session.commit()
        flash('Job updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_job.html', job=job)

@app.route('/delete_job/<int:job_id>', methods=['POST'])
@login_required
@role_required('employer')
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    user = User.query.get(session['user_id'])
    
    if job.employer_id != user.id:
        flash('You can only delete your own jobs!', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/job_applications/<int:job_id>')
@login_required
@role_required('employer')
def job_applications(job_id):
    job = Job.query.get_or_404(job_id)
    user = User.query.get(session['user_id'])
    
    if job.employer_id != user.id:
        flash('You can only view applications for your own jobs!', 'danger')
        return redirect(url_for('dashboard'))
    
    applications = Application.query.filter_by(job_id=job_id).all()
    return render_template('job_applications.html', job=job, applications=applications)

@app.route('/manage_users')
@login_required
@role_required('admin')
def manage_users():
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == session['user_id']:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('manage_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('manage_users'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
else:
    # For Vercel/serverless deployment
    with app.app_context():
        db.create_all()
