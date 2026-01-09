# Job Portal Web Application

A comprehensive web-based platform designed to connect job seekers and employers efficiently. The system allows employers to post job vacancies and manage applications, while job seekers can search for suitable jobs and apply online.

## Features

### 🔐 Authentication & Authorization
- Secure user registration and login system
- Role-based access control (Job Seeker / Employer / Admin)
- Session management using Flask sessions
- Password hashing with Werkzeug

### 💼 Job Management
- Employers can post job details (title, company, description, salary, location)
- Job status management (Open/Closed)
- Edit and delete job postings
- View applications for posted jobs

### 🔍 Job Search & Application
- Browse available job listings
- Search using keywords and location filters
- One-click job application system
- View detailed job information

### 📊 Application Tracking
- Employers can view all received applications
- Application status management (Pending/Accepted/Rejected)
- Detailed applicant information display

### 👥 User Roles

#### Job Seeker
- Register and login to the system
- View available job listings
- Search jobs based on keyword and location
- Apply for jobs with a single click
- View applied jobs and profile information

#### Employer
- Register and login as an employer
- Post new job openings
- View, update, open/close, or delete job listings
- View applications received for posted jobs
- Manage job status and applicant details

#### Admin
- Manage users (view, delete)
- Monitor platform activity
- View system statistics
- Access comprehensive dashboard

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML, CSS, Bootstrap 5 |
| Backend | Python (Flask Framework) |
| Database | SQLite (via SQLAlchemy ORM) |
| Authentication | Werkzeug Password Hashing |
| Icons | Font Awesome |

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd job-portal
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your web browser and navigate to: `http://127.0.0.1:5000`

## Project Structure

```
job-portal/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── job_portal.db         # SQLite database (created automatically)
└── templates/            # HTML templates
    ├── base.html         # Base template with navigation
    ├── index.html        # Home page
    ├── register.html     # User registration
    ├── login.html        # User login
    ├── jobs.html         # Job listings page
    ├── job_detail.html   # Individual job details
    ├── job_seeker_dashboard.html
    ├── employer_dashboard.html
    ├── admin_dashboard.html
    ├── post_job.html     # Post new job form
    ├── edit_job.html     # Edit existing job
    ├── job_applications.html
    └── manage_users.html
```

## Database Schema

The application uses three main models:

### User Model
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email address
- `password_hash` - Hashed password
- `role` - User role (job_seeker/employer/admin)
- `full_name` - User's full name
- `created_at` - Registration timestamp

### Job Model
- `id` - Primary key
- `title` - Job title
- `company_name` - Company name
- `description` - Job description
- `salary_min` - Minimum salary (optional)
- `salary_max` - Maximum salary (optional)
- `location` - Job location
- `status` - Job status (open/closed)
- `created_at` - Posting timestamp
- `employer_id` - Foreign key to User model

### Application Model
- `id` - Primary key
- `job_id` - Foreign key to Job model
- `applicant_id` - Foreign key to User model
- `applied_at` - Application timestamp
- `status` - Application status (pending/accepted/rejected)

## Usage

### For Job Seekers
1. Register as a job seeker
2. Browse available jobs or search with filters
3. Click on jobs to view details
4. Apply for jobs with a single click
5. Track your applications in the dashboard

### For Employers
1. Register as an employer
2. Post new job openings with detailed information
3. Manage job postings (edit, close, delete)
4. View and manage applications for your jobs
5. Update application statuses

### For Admins
1. Access comprehensive dashboard
2. Monitor platform statistics
3. Manage users (view, delete)
4. View all job postings and applications

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control
- Input validation and sanitization
- CSRF protection (Flask built-in)

## Future Enhancements

- Resume upload feature
- Email notifications for applications
- Admin dashboard with advanced analytics
- Job recommendations using AI
- Company profiles and reviews
- API integration with external job platforms
- Advanced search filters
- Application tracking with status updates via email

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For any questions or issues, please create an issue in the repository or contact the development team.

---

**Note**: The first time you run the application, it will automatically create the SQLite database with all necessary tables. The default admin account can be created by registering a user with the 'admin' role through the registration form.
