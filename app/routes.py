from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from . import db 
from app.models import User, Content, Specialist, Report
from app.forms import LoginForm, SignupForm, SubmitContentForm, SymptomCheckerForm, AddSpecialistForm, ReportForm
from app.translator import Translator
import os
import logging

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize translator
translator = Translator()

from flask import Blueprint
main = Blueprint('main', __name__)

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    
    """Helper function to validate file extensions."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

### ROUTES ###

@main.route('/', methods=['GET', 'POST'])
def home():
    logger.info("Rendering home page.")
    form = SubmitContentForm()

    # Get the page number from query parameters
    page_number = request.args.get('page', 1, type=int) 
    contents = Content.get_paginated_posts(page=page_number, per_page=10)


    
    # Check form validation and log errors if it fails
    if form.validate_on_submit():
        filename = None
        try:
            if form.image.data and allowed_file(form.image.data.filename):
                filename = secure_filename(form.image.data.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                form.image.data.save(filepath)
                logger.info(f"Image uploaded: {filename}")
                logger.info(f"Upload path: {filepath}")

            content = Content(
                title=form.title.data,
                description=form.description.data,
                image_url=filename,
                user_id=current_user.id
            )
            db.session.add(content)
            db.session.commit()
            flash('Content submitted successfully. It will be reviewed by an admin.', 'success')
            logger.info(f"New content submitted by user {current_user.email}: {content.title}")
        except Exception as e:
            db.session.rollback()  # Ensure rollback in case of failure
            logger.error(f"Error submitting content: {str(e)}")
            flash('There was an error submitting your content. Please try again later.', 'danger')
        
        return redirect(url_for('main.home'))
    else:
        # Log all form errors for debugging
        for field, errors in form.errors.items():
            for error in errors:
                logger.warning(f"Form validation error in {field}: {error}")
        # logger.warning(f"Content submission form validation failed for user {current_user.email}")
        
    return render_template('home.html', contents=contents, form=form)

# User Signup
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    logger.info("Rendering signup page.")
    from app import bcrypt, db  # Delayed imports to avoid circular dependency
    form = SignupForm()

    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(name=form.name.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully. You can now log in.', 'success')
            logger.info(f"New user signed up: {user.email}")
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()  # Ensure rollback in case of failure
            logger.error(f"Error creating user: {str(e)}")
            flash('There was an error creating your account. Please try again later.', 'danger')
    else:
        # Log all form errors to help diagnose what is causing the failure
        for field, errors in form.errors.items():
            for error in errors:
                logger.warning(f"Signup form error - {field}: {error}")
    
    return render_template('signup.html', form=form)


# User Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    logger.info("Rendering login page.")
    from app import bcrypt  # Delayed import
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully.', 'success')
            logger.info(f"User logged in: {user.email}")
            
            # Check if user is admin and redirect to the appropriate page
            if user.is_admin:
                return redirect(url_for('main.review_content'))  # Admin is redirected to review content page
            else:
                return redirect(url_for('main.home'))  # Regular users redirected to home
        else:
            logger.warning(f"Login failed for email: {form.email.data}")
            flash('Login failed. Check your email and password.', 'danger')
    else:
        logger.warning(f"Login form validation failed for email: {form.email.data}")
    return render_template('login.html', form=form)


# User Logout
@main.route('/logout')
@login_required
def logout():
    logger.info(f"User logged out: {current_user.email}")
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))


# Submit Content
@main.route('/submit_content', methods=['GET', 'POST'])
@login_required
def submit_content():
    logger.info(f"User {current_user.email} is accessing the submit content page.")
    form = SubmitContentForm()
    
    # Check form validation and log errors if it fails
    if form.validate_on_submit():
        filename = None
        try:
            if form.image.data and allowed_file(form.image.data.filename):
                filename = secure_filename(form.image.data.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                form.image.data.save(filepath)
                logger.info(f"Image uploaded: {filename}")
                logger.info(f"Upload path: {filepath}")

            content = Content(
                title=form.title.data,
                description=form.description.data,
                image_url=filename,
                user_id=current_user.id
            )
            db.session.add(content)
            db.session.commit()
            flash('Content submitted successfully. It will be reviewed by an admin.', 'success')
            logger.info(f"New content submitted by user {current_user.email}: {content.title}")
        except Exception as e:
            db.session.rollback()  # Ensure rollback in case of failure
            logger.error(f"Error submitting content: {str(e)}")
            flash('There was an error submitting your content. Please try again later.', 'danger')
        
        return redirect(url_for('main.home'))
    else:
        # Log all form errors for debugging
        for field, errors in form.errors.items():
            for error in errors:
                logger.warning(f"Form validation error in {field}: {error}")
        logger.warning(f"Content submission form validation failed for user {current_user.email}")

    return render_template('submit_content.html', form=form)


# Symptom Checker
@main.route('/symptom_checker', methods=['GET', 'POST'])
@login_required
def symptom_checker():
    logger.info("Rendering symptom checker page.")
    form = SymptomCheckerForm()
    result = None
    if form.validate_on_submit():
        symptoms = [form.symptom1.data, form.symptom2.data, form.symptom3.data]
        score = symptoms.count('yes')
        if score >= 2:
            result = "You may be at risk of prostate cancer. Please consult a specialist."
        else:
            result = "Your symptoms are unlikely to indicate prostate cancer."
        logger.info(f"Symptom checker result for user {current_user.email}: {result}")
    else:
        logger.warning(f"Symptom checker form validation failed for user {current_user.email}")
    return render_template('symptom_checker.html', form=form, result=result)

# Other routes as per your original code...
# Review Content (Admin only)
@main.route('/review_content')
@login_required
def review_content():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        logger.warning(f"Unauthorized attempt by user {current_user.email} to access review content.")
        return redirect(url_for('main.home'))
    
    # Fetch content that is not yet approved
    content_to_review = Content.query.filter_by(is_approved=False).all()
    logger.info(f"Rendering review content page with {len(content_to_review)} unapproved content.")

    return render_template('review_content.html', content_to_review=content_to_review)

# Add Specialist (Admin only)
@main.route('/add_specialist', methods=['GET', 'POST'])
@login_required
def add_specialist():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        logger.warning(f"Unauthorized attempt by user {current_user.email} to access add_specialist.")
        return redirect(url_for('main.home'))
    
    logger.info("Rendering add specialist page.")
    form = AddSpecialistForm()
    if form.validate_on_submit():
        try:
            specialist = Specialist(
                name=form.name.data,
                specialty=form.specialty.data,
                location=form.location.data,
                contact=form.contact.data
            )
            db.session.add(specialist)
            db.session.commit()
            flash('Specialist added successfully.', 'success')
            logger.info(f"New specialist added: {specialist.name}")
        except Exception as e:
            logger.error(f"Error during adding specialist: {str(e)}")
            flash('An error occurred while adding the specialist. Please try again.', 'danger')
    
    return render_template('add_specialist.html', form=form)
# Admin Dashboard
@main.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        logger.warning(f"Unauthorized attempt by user {current_user.email} to access dashboard.")
        return redirect(url_for('main.home'))
    
    # Fetch statistics for the admin dashboard
    total_content = Content.query.count()
    approved_content = Content.query.filter_by(is_approved=True).count()
    pending_content = total_content - approved_content
    total_specialists = Specialist.query.count()
    user = current_user
    
    logger.info(f"Rendering dashboard page for admin {current_user.email}")

    # Pass the statistics to the template
    return render_template(
        'dashboard.html',
        total_content=total_content,
        approved_content=approved_content,
        pending_content=pending_content,
        total_specialists=total_specialists,
        user=user
    )


# Approve Content (Admin only)
# Approve Content (Admin only)
@main.route('/approve_content/<int:content_id>', methods=['GET', 'POST'])
@login_required
def approve_content(content_id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        logger.warning(f"Unauthorized attempt by user {current_user.email} to approve content.")
        return redirect(url_for('main.home'))

    try:
        content = Content.query.get_or_404(content_id)
        content.is_approved = True
        db.session.commit()
        flash(f"Content '{content.title}' approved successfully.", 'success')
        logger.info(f"Content approved: {content.title}")
    except Exception as e:
        logger.error(f"Error approving content with ID {content_id}: {str(e)}")
        flash('An error occurred while approving the content. Please try again.', 'danger')

    return redirect(url_for('main.review_content'))

# Reject Content (Admin only)
@main.route('/reject_content/<int:content_id>', methods=['GET', 'POST'])
@login_required
def reject_content(content_id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        logger.warning(f"Unauthorized attempt by user {current_user.email} to reject content.")
        return redirect(url_for('main.home'))

    try:
        content = Content.query.get_or_404(content_id)
        db.session.delete(content)
        db.session.commit()
        flash(f"Content '{content.title}' rejected and removed.", 'info')
        logger.info(f"Content rejected: {content.title}")
    except Exception as e:
        logger.error(f"Error rejecting content with ID {content_id}: {str(e)}")
        flash('An error occurred while rejecting the content. Please try again.', 'danger')

    return redirect(url_for('main.review_content'))



@main.route('/specialists')
def specialists():
    try:
        # Fetch all specialists from the database
        specialists = Specialist.query.all()
        logger.info(f"Retrieved {len(specialists)} specialists from the database.")
        
        # Render the specialists page and pass the specialists data
        return render_template('specialists.html', specialists=specialists)
    
    except Exception as e:
        # Log any errors
        logger.error(f"Error fetching specialists: {e}")
        return render_template('error.html', message="An error occurred while fetching specialists.")


# Report Issue
@main.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    logger.info("Rendering report page.")
    form = ReportForm()
    if form.validate_on_submit():
        try:
            report = Report(message=form.message.data, user_id=current_user.id)
            db.session.add(report)
            db.session.commit()
            flash('Report submitted successfully.', 'success')
            logger.info(f"New report submitted by user {current_user.email}")
        except Exception as e:
            logger.error(f"Error submitting report for user {current_user.email}: {str(e)}")
            flash('An error occurred while submitting your report. Please try again.', 'danger')
    
    return render_template('reports.html', form=form)

# View Reports (Admin only)
@main.route('/view_reports')
@login_required
def view_reports():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        logger.warning(f"Unauthorized attempt by user {current_user.email} to view reports.")
        return redirect(url_for('main.home'))
    
    logger.info("Rendering view reports page.")
    try:
        reports = Report.query.all()
        if not reports:
            logger.warning("No reports found.")
    except Exception as e:
        logger.error(f"Error fetching reports: {str(e)}")
        flash('An error occurred while fetching the reports. Please try again.', 'danger')
        return redirect(url_for('main.home'))
    
    return render_template('view_reports.html', reports=reports)
