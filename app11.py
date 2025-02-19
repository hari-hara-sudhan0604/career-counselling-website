from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from flask_socketio import SocketIO, emit, join_room, leave_room
from typing import Dict, List
from langchain_groq import ChatGroq
from category import category
from statistics import mode
from collections import Counter
from langchain_core.prompts import PromptTemplate
import getpass
import os
import mysql.connector
from bcrypt import hashpw, gensalt, checkpw
import smtplib  # For sending emails
import uuid
from flask_bcrypt import Bcrypt
import re
import pymysql
from werkzeug.utils import secure_filename
import plotly.graph_objects as go

app=Flask(__name__)
app.secret_key = "your_secret_key"
socketio = SocketIO(app, cors_allowed_origins="*")

db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': '',  # Replace with your MySQL password
    'database': 'project'  # Replace with your database name
}

bcrypt = Bcrypt(app)

# Email configuration
EMAIL_ADDRESS = 'futureforge06@gmail.com'
EMAIL_PASSWORD = 'hxqd hppo ejty pfsz'  # Use Gmail app password
os.environ["GROQ_API_KEY"] = "__paste your api here__"



# Function to send an email
def send_email_notification(user_email, user_name):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()  # Secure the connection
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Login with your email credentials

            subject = 'Welcome to Future Forge!'
            body = f"Hi {user_name},\n\nWe are thrilled to have you on board with Future Forge. Thank you for signing up!\n\nBest regards,\nFuture Forge Team"
            msg = f"Subject: {subject}\n\n{body}"

            smtp.sendmail(EMAIL_ADDRESS, user_email, msg)  # Send the email
            print(f"Email sent to {user_email}")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
def send_verification_email(user_email, user_name, token):
    try:
        verification_link = url_for('verify_email', token=token, _external=True)
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            subject = 'Verify Your Email - Future Forge'
            body = f"""Hi {user_name},

Thank you for signing up with Future Forge!

Please verify your email by clicking the link below:
{verification_link}

If you didn't sign up, please ignore this email.

Best regards,
Future Forge Team
"""
            msg = f"Subject: {subject}\n\n{body}"
            smtp.sendmail(EMAIL_ADDRESS, user_email, msg)
            print(f"Verification email sent to {user_email}")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")

@app.route('/')
def homewo():
    return render_template("homewo.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signupform', methods=['POST'])
def signupform():
    try:
        # Get form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        dob = request.form['dob']
        password = request.form['password']
        cpassword = request.form['cpassword']
        gender = request.form['gender']
        state = request.form['state']

        # Check if passwords match
        if password != cpassword:
            return "Passwords do not match. Please go back and try again."
        # Hash the password
        hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

         # Generate a verification token
        verification_token = str(uuid.uuid4())
        
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert data into the database
        query = """
            INSERT INTO students_master (firstname, lastname, email, password,dob,gender,state, verification_token)
            VALUES (%s, %s, %s, %s, %s ,%s ,%s,%s)
        """
        cursor.execute(query, (firstname, lastname, email, hashed_password,dob,gender,state, verification_token))
        connection.commit()
        session['user_email'] = email
        # Close the connection
        send_verification_email(email, firstname, verification_token)
        cursor.close()
        connection.close()
        send_email_notification(email, firstname)
        flash("Signup successful! Please login.", "success")
       
        return redirect(url_for('verification_message'))

    except mysql.connector.Error as err:
        return f"Database error: {err}"
    except Exception as e:
        return f"An error occurred: {e}"
@app.route('/verification_message')
def verification_message():
    return render_template("verification_message.html")

@app.route('/verify_email/<token>')
def verify_email(token):
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if the token exists in pending_users
        query = "SELECT * FROM pending_users WHERE verification_token = %s"
        cursor.execute(query, (token,))
        user = cursor.fetchone()

        if user:
            # Move user data to the users table
            move_query = """
                INSERT INTO students_master (firstname, lastname, email, password, dob, gender, state, is_verified)
                VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
            """
            cursor.execute(move_query, user[:-1])  # Exclude the token column
            connection.commit()

            # Delete user data from pending_users
            delete_query = "DELETE FROM pending_users WHERE verification_token = %s"
            cursor.execute(delete_query, (token,))
            connection.commit()

            flash("Your email has been verified. Please sign in to access your account.", "success")
        else:
            flash("Invalid or expired verification link.", "danger")

        # Close connection
        cursor.close()
        connection.close()

        # Redirect to the sign-in page
        return redirect(url_for('signin'))
    except mysql.connector.Error as err:
        flash(f"Database error: {err}", "danger")
        return redirect(url_for('home'))
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('home'))



@app.route('/profile')
def profile():
    if 'user_email' not in session:
        return redirect(url_for('signin'))
    
    email = session['user_email']
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)  # Use dictionary=True for easy column access
        
        # Fetch user details from the database
        query = "SELECT firstname, lastname, email, dob, gender, state FROM students_master WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        
        # Close the connection
        cursor.close()
        connection.close()

        if user:
            return render_template('profile.html', user=user)  # Pass user data to the template
        else:
            flash('User not found!', 'danger')
            return render_template("homewo.html")
    except mysql.connector.Error as err:
        flash(f'Database error: {err}', 'danger')
        return render_template("homewo.html")
    except Exception as e:
        flash(f'Error occurred: {e}', 'danger')
        return render_template("homewo.html")



@app.route('/signin')
def signin():
    return render_template("signin.html")

@app.route('/signinform', methods=['GET', 'POST'])
def signinform():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Connect to the database
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            # Check user in database
            query = "SELECT * FROM students_master WHERE email = %s"
            cursor.execute(query, (email,))
            students_master = cursor.fetchone()

            # Close the connection
            cursor.close()
            connection.close()

            if students_master and checkpw(password.encode('utf-8'), students_master['password'].encode('utf-8')):
                session['user_email'] = email
                session['student_id'] = students_master['student_id']
                flash("Login successful!", "success")
                return render_template("home.html")  # Replace 'home' with your homepage route
            else:
                flash("Invalid email or password. Please try again.", "danger")
        except mysql.connector.Error as err:
            return f"Database error: {err}"
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template('signin.html')  # Replace with your signin template
    
    
    

#questions
@app.route('/assessment')
def assessment():
    return render_template("assesmentqn.html")

@app.route('/questions')
def questions():
    return render_template("questions.html")

llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.4,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
   
def format_response_for_html(response: str) -> str:
    """
    Converts newline characters in the response to <br> tags for HTML rendering.
    """
    return response.replace("\n", "<br>")
    #from here
def generate_chart(value_counts):
    """
    Generates a bar chart for user preferences.
    """
    
    all_traits = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
    
    # Ensure all traits are included, even if their count is 0
    value_counts = {trait: value_counts.get(trait, 0) for trait in all_traits}
    
    # Create Plotly Bar Chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=list(value_counts.keys()),
                y=list(value_counts.values()),
                text=list(value_counts.values()),  # Display counts as hover text
                textposition='outside',
                marker_color='skyblue'
            )
        ]
    )
    fig.update_layout(
        yaxis=dict(
            tickmode='linear',
            dtick=1  # Set interval between ticks to 1
        ),
        #title='Your Preferences',
        xaxis_title='Traits',
        yaxis_title='Frequency',
        template='plotly_white',
        font=dict(size=14),
        autosize=True,  # Enable automatic resizing
    )
    config = {
        'displayModeBar': True,  # Show the toolbar
        'modeBarButtonsToRemove': [
            'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d',
            'zoomOut2d', 'autoScale2d', 'resetScale2d'  # Remove unwanted buttons
        ],
        'displaylogo': False  # Hide the Plotly logo
    }
    # Convert Plotly figure to HTML (to embed in web pages) or PNG (if needed)
    return fig.to_html(config=config)



# Mapping of values to URLs
value_to_url = {
    "Realistic": "/realistic-careers",
    "Investigative": "/investigative-careers",
    "Artistic": "/artistic-careers",
    "Social": "/social-careers",
    "Enterprising": "/enterprising-careers",
    "Conventional": "/conventional-careers",
    # Add more mappings as needed
}
 # routing career pages..

@app.route("/investigative-careers")
def investigative_careers():
    return render_template("/investigative_careers.html")

@app.route("/conventional-careers")
def conventional_careers():
    return render_template("/conventional_careers.html")

@app.route("/enterprising-careers")
def enterprising_careers():
    return render_template("/enterprising_careers.html")

@app.route("/realistic-careers")
def realistic_careers():
    return render_template("realistic_careers.html")

@app.route("/social-careers")
def social_careers():
    return render_template("social_careers.html")

@app.route("/artistic-careers")
def artistic_careers():
    return render_template("artistic_careers.html")
    #ending career pages..

@app.route("/", methods=["GET", "POST"])
def questionnaire():
    mode_result = None
    links = []  # To hold links for recommendations
    error_message = None  # For edge cases
    chart_image = None  # Initialize chart_image to avoid UnboundLocalError

    if request.method == "POST":
        data = request.form.to_dict()

        if not data:  # Edge case: No responses submitted
            error_message = "Please complete the questionnaire before submitting."
            return render_template("questions.html", error_message=error_message)

        # Count the frequency of each value
        value_counts = Counter(data.values())
        sorted_values = value_counts.most_common()

        # Edge case: Only one value present
        if len(sorted_values) == 1:
            combined_modes = [sorted_values[0][0]]  # Only the most frequent value
        else:
            # Get the most frequent and second most frequent values
            most_frequent = [sorted_values[0][0]]
            second_most_frequent = [sorted_values[1][0]]
            combined_modes = most_frequent + second_most_frequent

        # Handle ties in frequencies (include all tied values)
        max_frequency = sorted_values[0][1]
        combined_modes = [
            value for value, count in sorted_values if count == max_frequency
        ]
        #chart generation
        chart_image = generate_chart(value_counts)

        #to here
        # Prompt Template for LLM
        prompt = PromptTemplate.from_template(
            "you are good talking about their values: {value}. Try to provide the professional jobs best suited for their values: {value}, . explain in such a way that school student od age 10 could understand, and do not add extra text. Do not mention the college or university name. Start with: 'As per interest, the suggestions/recommendations are as follows:'")
        chain = prompt | llm

        # Generate recommendations
        output = chain.invoke({"value": combined_modes})
        mode_result = format_response_for_html(output.content)


        #this also
        # Generate links for recommendations
        for mode in combined_modes:
            if mode in value_to_url:
                links.append({"label": f"Explore careers in {mode}", "url": value_to_url[mode]})

    return render_template("questions.html", mode_result=mode_result, links=links, chart_image=chart_image)
       #till here
@app.route('/mentorpage')
def mentorpage():
    student_id = session.get('student_id')
    if not student_id:
        flash('Please log in to access your dashboard', 'danger')
        return redirect(url_for('signin'))
    return render_template("mentor.html",student_id=student_id)

@app.route('/mentor1-profile')
def mentor1_profile():
    # Profile page for Mentor 1
    return render_template('mentor1_profile.html')

@app.route('/mentor2-profile')
def mentor2_profile():
    # Profile page for Mentor 2
    return render_template('mentor2_profile.html')
    
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    prompt = PromptTemplate.from_template(
        """You are an AI assistant specializing in education, career guidance, and job trends. You can only provide information related to academic courses, qualifications, job market trends, career pathways, and skills development. If a user asks about a topic outside these areas, politely inform them that your expertise is limited to studies and career-related guidance and redirect them to relevant questions within this scope. : {input}"""
        )
    chain = prompt | llm
    output=chain.invoke({"input":input})
    out=output.content
    print(out)
    return out

@app.route('/diploma')
def diploma():
    return render_template("diploma.html")

@app.route('/skillcourses')
def skillcourses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT skill_course_name,course_description FROM skill_courses")
    skillcourses= cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("skillcourses.html",skillcourses=skillcourses)

@app.route('/vocationalcourses')
def vocationalcourses():
    return render_template("vocationalcourses.html")

@app.route('/exams')
def exams():
    return render_template("exams.html")

@app.route('/groups')
def groups ():
    return render_template("groups.html")

# Helper function to fetch categories from MySQL
def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Fetch as dictionary for better readability
    cursor.execute("SELECT category_id, category_name FROM category")
    categories = cursor.fetchall()
    conn.close()
    return categories

# Helper function to fetch courses by category_id from MySQL
def get_courses_by_category(category_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT course_name, about, eligibility, why_choose 
        FROM course 
        WHERE category_id = %s
    """, (category_id,))
    courses = cursor.fetchall()
    conn.close()
    return courses

@app.route('/category')
def category_list():
    categories = get_categories()
    return render_template('category_list.html', categories=categories)

@app.route('/courses/<int:category_id>')
def course_list(category_id):
    courses = get_courses_by_category(category_id)
    # Fetch category name (for display in the course list page)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT category_name FROM category WHERE category_id = %s", (category_id,))
    category = cursor.fetchone()
    conn.close()

    # Pass category name along with courses to the template
    return render_template('course_list.html', courses=courses, category_name=category['category_name'])

@app.route('/homewo')
def wo():
    return render_template("homewo.html")
@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('Logged out successfully!')
    return redirect(url_for('signin'))

#mentor pages
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/mentorsignup')
def mentorsignup():
    return render_template("mentorsignup.html")
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form ['lastname']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        gender =  request.form['gender']
        qualification = request.form['qualification']
        years_of_experience = request.form['years_of_experience']
        field_of_work = request.form['field_of_work']
        biography = request.form['biography']

        # Input validation
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'danger')
            return render_template('mentorsignup.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters!', 'danger')
            return render_template('mentorsignup.html')

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO mentors_master (firstname, lastname, email, password, age,qualification, years_of_experience, field_of_work,biography) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)",
                           (firstname, lastname, email, hashed_password, age,qualification,years_of_experience, field_of_work, biography))
            conn.commit()
            flash('You have successfully registered! Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Email already exists!', 'danger')
            return render_template('mentorsignup.html')
        finally:
            cursor.close()
            conn.close()
    return render_template('mentorsignup.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_candidate = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM mentors_master WHERE email = %s", [email])
        mentor = cursor.fetchone()
        cursor.close()
        conn.close()

        if mentor and checkpw( password_candidate.encode('utf-8'), mentor['password'].encode('utf-8')):
            session['mentor_id'] = mentor.get('mentor_id')
            print("Session mentor_id:", session.get('mentor_id'))
            session['firstname'] = mentor.get('firstname', 'Mentor')
            flash('Logged in successfully!', 'success')
            return redirect(url_for('mhome'))
        else:
            flash('Invalid email or password!', 'danger')
            return render_template('mentorsignin.html')
    return render_template('mentorsignin.html')
@app.route('/mhome')
def mhome():
    if 'mentor_id' in session:
        mentor_id = session.get('mentor_id')
        return render_template('mhome.html', firstname=session.get('firstname','Mentor'),mentor_id=mentor_id)
    else:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
@app.route('/students')
def students():
    if 'mentor_id' in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT student_id, firstname, lastname, email, dob, gender, state FROM students_master")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('students.html', students=students)
    else:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
### ======== Logout Route ======== ###
@app.route('/mlogout')
def mlogout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))




# adminpages#
@app.route('/adminhome')
def adminhome():
    return render_template("admin'shome.html")

@app.route('/adminlogin')
def login_page():
    return render_template('login.html')

@app.route('/adminsignup', methods=['POST'])
def login_admin():
    email = request.form['email']
    password = request.form['password']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM admin WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    admin = cursor.fetchone()

    conn.close()

    if admin:
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid email or password!')
        return redirect(url_for('login_page'))

# Admin dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# View students details
@app.route('/view_students')
def view_students():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Fetch all student details from the "users" table
    cursor.execute("SELECT * FROM students_master")
    students = cursor.fetchall()

    conn.close()
    return render_template('view_students.html', students=students)

@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Delete a student by ID from the "users" table
    cursor.execute("DELETE FROM students_master WHERE student_id = %s", (student_id,))
    conn.commit()

    conn.close()
    flash('Student deleted successfully!')
    return redirect(url_for('view_students'))

# View mentors details
@app.route('/view_mentors')
def view_mentors():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mentors_master")
    mentors = cursor.fetchall()

    conn.close()
    return render_template('view_mentors.html', mentors=mentors)

@app.route('/delete_mentor/<int:mentor_id>', methods=['POST'])
def delete_mentor(mentor_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM mentors_master WHERE mentor_id  = %s", (mentor_id,))
    conn.commit()

    conn.close()
    flash('Mentor deleted successfully!')
    return redirect(url_for('view_mentors'))

@app.route('/add_mentor')
def add_mentor():
    return render_template("add_mentor.html")

@app.route('/add_mentors', methods=['GET', 'POST'])
def add_mentors():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form ['lastname']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        gender =  request.form['gender']
        qualification = request.form['qualification']
        years_of_experience = request.form['years_of_experience']
        field_of_work = request.form['field_of_work']
        biography = request.form['biography']

        # Input validation
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'danger')
            return render_template('mentorsignup.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters!', 'danger')
            return render_template('mentorsignup.html')

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO mentors_master (firstname, lastname, email, password, age,qualification, years_of_experience, field_of_work,biography) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)",
                           (firstname, lastname, email, hashed_password, age,qualification,years_of_experience, field_of_work, biography))
            conn.commit()
            flash('You have successfully registered! Please login.', 'success')
            return redirect(url_for('view_mentors'))
        except mysql.connector.IntegrityError:
            flash('Email already exists!', 'danger')
            return render_template("add_mentor.html")
        finally:
            cursor.close()
            conn.close()
    return render_template('view_mentors.html')

@app.route('/approve_mentor/<int:mentor_id>', methods=['POST'])
def approve_mentor(mentor_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("UPDATE mentors_master SET is_approved = 1 WHERE mentor_id = %s", (mentor_id,))
    conn.commit()

    conn.close()
    flash('Mentor approved successfully!')
    return redirect(url_for('view_mentors'))


@app.route('/approved')
def approved():
    if 'student_id' not in session:
        flash('Please log in to view mentors.', 'danger')
        return redirect(url_for('signin'))

    student_id = session['student_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch mentors and their connection status for the logged-in student
        cursor.execute("""
            SELECT mm.*, 
                   CASE 
                       WHEN smm.status = 'pending' THEN 'pending'
                       WHEN smm.status = 'accepted' THEN 'connected'
                       ELSE 'connect'
                   END AS connection_status
            FROM mentors_master mm
            LEFT JOIN student_mentor_map smm 
            ON mm.mentor_id = smm.mentor_id AND smm.student_id = %s
            WHERE mm.is_approved = 1
        """, (student_id,))
        approved_mentors = cursor.fetchall()

    except Exception as e:
        flash(f'Error fetching mentors: {e}', 'danger')
        approved_mentors = []
    finally:
        cursor.close()
        conn.close()

    return render_template('approved.html', approved_mentors=approved_mentors, student_id=student_id)




#showing cards for mentor and selecting particular mentor

@app.route('/api/mentors')
def api_get_mentors():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mentors_master WHERE is_approved = 1")  # Only fetch approved mentors
    mentors = cursor.fetchall()

    conn.close()
    return jsonify(mentors)


@app.route('/connection-status', methods=['GET'])
def connection_status():
    mentor_id = request.args.get('mentor_id')
    if 'student_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    student_id = session['student_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT status FROM student_mentor_map 
            WHERE student_id = %s AND mentor_id = %s
        """, (student_id, mentor_id))
        result = cursor.fetchone()

        if result:
            return jsonify({"connection_status": result['status']})
        else:
            return jsonify({"connection_status": "connect"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()




def get_db_connection1():
    try:
        connection = pymysql.connect(
            host='localhost',  # Update with your DB host
            user='root',  # Update with your DB user
            password='',  # Update with your DB password
            database='project',  # Update with your DB name
            cursorclass=pymysql.cursors.DictCursor  # Ensures results are returned as dictionaries
        )
        return connection
    except Exception as e:
        # Log error if database connection fails
        print(f"Error: {str(e)}")
        return None

@app.route('/mentorpage')
def mentorpages():
    return render_template("mentor.html")

@app.route('/mentor-profile/<int:mentor_id>')
def mentor_profile(mentor_id):
    # Fetch the mentor details from the database using mentor_id
    db_connection = get_db_connection1()
    if not db_connection:
        return render_template('404.html', error="Unable to connect to the database"), 500

    try:
        db_cursor = db_connection.cursor()
        db_cursor.execute('SELECT * FROM mentors_master WHERE mentor_id = %s', (mentor_id,))
        mentor = db_cursor.fetchone()
    except Exception as e:
        return render_template('404.html', error=f"Database error: {str(e)}"), 500
    finally:
        db_connection.close()
    
    if mentor:
        # Render the template and pass the mentor's data
        return render_template('mentor-profile.html', mentor=mentor)
    else:
        # If no mentor is found, display a 404 page with a helpful message
        return render_template('404.html', error="Mentor not found"), 404
    
    



@app.route('/get-mentor-details', methods=['GET'])
def get_mentor_details():
    mentor_id = request.args.get('id')  # Retrieve the 'id' query parameter from the URL
    if not mentor_id:
        return jsonify({"error": "Mentor ID not provided"}), 400

    # Fetch mentor details from the database
    conn = get_db_connection1()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM mentors_master WHERE mentor_id = %s', (mentor_id,))
    mentor = cursor.fetchone()
    conn.close()

    if mentor:
        return jsonify({
            "firstname": mentor['firstname'],
            "lastname": mentor['lastname'],
            "email": mentor['email'],
            "age": mentor['age'],
            "gender": mentor['gender'],
            "qualification": mentor['qualification'],
            "years_of_experience": mentor['years_of_experience'],
            "biography": mentor['biography'],
            "field_of_work": mentor.get('field_of_work', 'Not available'),
            "image": mentor.get('image', '/static/default.jpg')
        })
    else:
        return jsonify({"error": "Mentor not found"}), 404



#student-mentor connection codes

@app.route('/connect', methods=['POST'])
def connect():
    """Send a connection request to a mentor."""
    if 'student_id' not in session:
        flash('Please log in to connect with mentors.', 'danger')
        return redirect(url_for('student_login'))

    student_id = session['student_id']  # Retrieve student_id from session
    mentor_id = request.form['mentor_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if there is an existing record for this student-mentor pair
        cursor.execute("""
            SELECT id, status FROM student_mentor_map
            WHERE student_id = %s AND mentor_id = %s
        """, (student_id, mentor_id))
        record = cursor.fetchone()

        if record:
            # Update the existing record if it was declined earlier
            if record[1] == 'declined':
                cursor.execute("""
                    UPDATE student_mentor_map
                    SET status = 'pending'
                    WHERE id = %s
                """, (record[0],))
            else:
                flash('Request already in process.', 'warning')
        else:
            # Insert a new connection request
            cursor.execute("""
                INSERT INTO student_mentor_map (student_id, mentor_id, status)
                VALUES (%s, %s, 'pending')
            """, (student_id, mentor_id))

        conn.commit()
        flash('Connection request sent!', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('approved'))


@app.route('/disconnect', methods=['POST'])
def disconnect():
    # Extract form data
    student_id = request.form.get('student_id')
    mentor_id = request.form.get('mentor_id')

    # Verify the user is logged in as a student or mentor
    if 'student_id' in session:
        # Student is logged in
        logged_in_student_id = session['student_id']
        if student_id and int(student_id) != logged_in_student_id:
            flash('Unauthorized action.', 'danger')
            return redirect(url_for('signin'))
    elif 'mentor_id' in session:
        # Mentor is logged in
        logged_in_mentor_id = session['mentor_id']
        if mentor_id and int(mentor_id) != logged_in_mentor_id:
            flash('Unauthorized action.', 'danger')
            return redirect(url_for('signin'))
    else:
        # Neither student nor mentor is logged in
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('signin'))

    # Perform the disconnection in the database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE student_mentor_map
            SET status = 'declined'
            WHERE student_id = %s AND mentor_id = %s
        """, (student_id, mentor_id))
        conn.commit()
        flash('Disconnected successfully.', 'success')
    except Exception as e:
        flash(f'Error disconnecting: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()

    # Redirect back to the referring page
    return redirect(request.referrer)


@app.route('/mentor_requests', methods=['GET', 'POST'])
def mentor_requests():
    """View and respond to connection requests for the logged-in mentor."""
    if 'mentor_id' not in session:
        flash('Please log in to view connection requests.', 'danger')
        return redirect(url_for('mentor_login'))

    mentor_id = session['mentor_id']

    if request.method == 'POST':
        connection_id = request.form['connection_id']
        action = request.form['action']
        status = 'accepted' if action == 'accept' else 'declined'

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Update the status in the student_mentor_map table
            cursor.execute("""
                UPDATE student_mentor_map
                SET status = %s
                WHERE id = %s
            """, (status, connection_id))

            conn.commit()
            flash(f'Request has been {status}!', 'success')

        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('mentor_requests'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch pending connection requests for the logged-in mentor
        cursor.execute("""
            SELECT smm.id AS connection_id, 
                   sm.firstname, 
                   sm.lastname, 
                   smm.status
            FROM student_mentor_map smm
            JOIN students_master sm ON smm.student_id = sm.student_id
            WHERE smm.mentor_id = %s AND smm.status = 'pending'
        """, (mentor_id,))
        requests = cursor.fetchall()

    except Exception as e:
        flash(f'Error retrieving requests: {e}', 'danger')
        requests = []
    finally:
        cursor.close()
        conn.close()

    return render_template('mentor_requests.html', requests=requests, mentor_id=mentor_id)


@app.route('/mentor_connections/<int:mentor_id>')
def mentor_connections(mentor_id):
    """View accepted students for a mentor."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT sm.firstname, sm.lastname, sm.student_id
            FROM student_mentor_map smm
            JOIN students_master sm ON smm.student_id = sm.student_id
            WHERE smm.mentor_id = %s AND smm.status = 'accepted'
        """, (mentor_id,))
        connections = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return render_template('mentor_connections.html', connections=connections, mentor_id=mentor_id)

@app.route('/student_connections/<int:student_id>')
def student_connections(student_id):
    """View connected mentors for a student."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT mm.firstname, mm.lastname, mm.mentor_id
            FROM student_mentor_map smm
            JOIN mentors_master mm ON smm.mentor_id = mm.mentor_id
            WHERE smm.student_id = %s AND smm.status = 'accepted'
        """, (student_id,))
        connections = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return render_template('student_connections.html', connections=connections, student_id=student_id)


@app.route('/adminlogout')
def adminlogout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('adminlogin'))

#lifecoach routes
@app.route('/lifecoach')
def lifecoach ():
    student_id = session.get('student_id')
    if not student_id:
        flash('Please log in to access your dashboard', 'danger')
        return redirect(url_for('signin'))
    return render_template("lifecoach.html",student_id=student_id)



@app.route('/lifecoachsignup')
def lifecoachsignup():
    return render_template("lifecoachsignup.html")
@app.route('/lifecoachregister', methods=['GET', 'POST'])
def lifecoachregister():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form ['lastname']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        gender =  request.form['gender']
        qualification = request.form['qualification']
        years_of_experience = request.form['years_of_experience']
        field_of_work = request.form['field_of_work']
        biography = request.form['biography']

        # Input validation
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'danger')
            return render_template('lifecoachsignup.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters!', 'danger')
            return render_template('lifecoachsignup.html')

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO life_coach_master (firstname, lastname, email, password, age,qualification, years_of_experience, field_of_work,biography) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)",
                           (firstname, lastname, email, hashed_password, age,qualification,years_of_experience, field_of_work, biography))
            conn.commit()
            flash('You have successfully registered! Please login.', 'success')
            return redirect(url_for('lifecoachlogin'))
        except mysql.connector.IntegrityError:
            flash('Email already exists!', 'danger')
            return render_template('lifecoachsignup.html')
        finally:
            cursor.close()
            conn.close()
    return render_template('lifecoachsignup.html')

@app.route('/lifecoachlogin', methods=['GET', 'POST'])
def lifecoachlogin():
    if request.method == 'POST':
        email = request.form['email']
        password_candidate = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM life_coach_master WHERE email = %s", [email])
        coach = cursor.fetchone()
        cursor.close()
        conn.close()

        if coach and checkpw( password_candidate.encode('utf-8'), coach['password'].encode('utf-8')):
            session['coach_id'] = coach.get('coach_id')
            print("Session coach_id:", session.get('coach_id'))
            session['firstname'] = coach.get('firstname', 'Coach')
            flash('Logged in successfully!', 'success')
            return redirect(url_for('lhome'))
        else:
            flash('Invalid email or password!', 'danger')
            return render_template('lifecoachsignin.html')
    return render_template('lifecoachsignin.html')

@app.route('/lhome')
def lhome():
    if 'coach_id' in session:
        coach_id = session.get('coach_id')
        return render_template('lhome.html', firstname=session.get('firstname','coach'),coach_id=coach_id)
    else:
        flash('Please login first.', 'warning')
        return redirect(url_for('lifecoachlogin'))
@app.route('/lstudents')
def lstudents():
    if 'coach_id' in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT student_id, firstname, lastname, email, dob, gender, state FROM students_master")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('lstudents.html', students=students)
    else:
        flash('Please login first.', 'warning')
        return redirect(url_for('lifecoachlogin'))
@app.route('/llogout')
def llogout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('lifecoachlogin'))

@app.route('/view_coaches')
def view_coaches():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM life_coach_master")
    coaches = cursor.fetchall()

    conn.close()
    return render_template('view_coaches.html', coaches=coaches)

@app.route('/delete_coach/<int:coach_id>', methods=['POST'])
def delete_coach(coach_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM life_coach_master WHERE coach_id  = %s", (coach_id,))
    conn.commit()

    conn.close()
    flash('Mentor deleted successfully!')
    return redirect(url_for('view_coaches'))

@app.route('/add_coach')
def add_coach():
    return render_template("add_coach.html")

@app.route('/add_coaches', methods=['GET', 'POST'])
def add_coaches():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form ['lastname']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        gender =  request.form['gender']
        qualification = request.form['qualification']
        years_of_experience = request.form['years_of_experience']
        field_of_work = request.form['field_of_work']
        biography = request.form['biography']

        # Input validation
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'danger')
            return render_template('add_coach.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters!', 'danger')
            return render_template('add_coach.html')

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO life_coach_master (firstname, lastname, email, password, age,qualification, years_of_experience, field_of_work,biography) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)",
                           (firstname, lastname, email, hashed_password, age,qualification,years_of_experience, field_of_work, biography))
            conn.commit()
            flash('You have successfully registered! Please login.', 'success')
            return redirect(url_for('view_coaches'))
        except mysql.connector.IntegrityError:
            flash('Email already exists!', 'danger')
            return render_template("add_coach.html")
        finally:
            cursor.close()
            conn.close()
    return render_template('add_coach.html')

@app.route('/approve_coach/<int:coach_id>', methods=['POST'])
def approve_coach(coach_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("UPDATE life_coach_master SET is_approved = 1 WHERE coach_id = %s", (coach_id,))
    conn.commit()

    conn.close()
    flash('coach approved successfully!')
    return redirect(url_for('view_coaches'))


@app.route('/approvedcoaches')
def approvedcoaches():
    if 'student_id' not in session:
        flash('Please log in to view mentors.', 'danger')
        return redirect(url_for('signin'))

    student_id = session['student_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch mentors and their connection status for the logged-in student
        cursor.execute("""
            SELECT mm.*, 
                   CASE 
                       WHEN smm.status = 'pending' THEN 'pending'
                       WHEN smm.status = 'accepted' THEN 'connected'
                       ELSE 'connect'
                   END AS connection_status
            FROM life_coach_master mm
            LEFT JOIN student_life_coach_map smm 
            ON mm.coach_id = smm.coach_id AND smm.student_id = %s
            WHERE mm.is_approved = 1
        """, (student_id,))
        approved_coaches = cursor.fetchall()

    except Exception as e:
        flash(f'Error fetching mentors: {e}', 'danger')
        approved_coaches = []
    finally:
        cursor.close()
        conn.close()

    return render_template('approvedcoaches.html', approved_coaches=approved_coaches, student_id=student_id)



@app.route('/api/coaches')
def api_get_coaches():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM life_coach_master WHERE is_approved = 1")  # Only fetch approved mentors
        coaches = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": "Failed to fetch mentors"}), 500
    finally:
        conn.close()

    return jsonify(coaches)


@app.route('/connection-status', methods=['GET'])
def connection_status_coach():
    coach_id = request.args.get('coach_id')
    if 'student_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    student_id = session['student_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT status FROM life_coach_master 
            WHERE student_id = %s AND coach_id = %s
        """, (student_id, coach_id))
        result = cursor.fetchone()

        if result:
            return jsonify({"connection_status_coach": result['status']})
        else:
            return jsonify({"connection_status_coach": "connect"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


def get_db_connection1():
    try:
        connection = pymysql.connect(
            host='localhost',  # Update with your DB host
            user='root',  # Update with your DB user
            password='',  # Update with your DB password
            database='project',  # Update with your DB name
            cursorclass=pymysql.cursors.DictCursor  # Ensures results are returned as dictionaries
        )
        return connection
    except Exception as e:
        # Log error if database connection fails
        print(f"Error: {str(e)}")
        return None


@app.route('/coach-profile/<int:coach_id>')
def lifecoachprofile(coach_id):
    # Fetch the mentor details from the database using mentor_id
    db_connection = get_db_connection1()
    if not db_connection:
        return render_template('404.html', error="Unable to connect to the database"), 500

    try:
        db_cursor = db_connection.cursor()
        db_cursor.execute('SELECT * FROM life_coach_master WHERE coach_id = %s', (coach_id,))
        coach = db_cursor.fetchone()
    except Exception as e:
        return render_template('404.html', error=f"Database error: {str(e)}"), 500
    finally:
        db_connection.close()
    
    if coach:
        # Render the template and pass the mentor's data
        return render_template('lifecoachprofile.html', coach=coach)
    else:
        # If no mentor is found, display a 404 page with a helpful message
        return render_template('404.html', error="Mentor not found"), 404
    
    



@app.route('/get-lifecoach-details', methods=['GET'])
def get_coach_details():
    coach_id = request.args.get('id')  # Retrieve the 'id' query parameter from the URL
    if not coach_id:
        return jsonify({"error": "coach ID not provided"}), 400

    # Fetch mentor details from the database
    conn = get_db_connection1()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM life_coach_master WHERE coach_id = %s', (coach_id,))
    coach = cursor.fetchone()
    conn.close()

    if coach:
        return jsonify({
            "firstname": coach['firstname'],
            "lastname": coach['lastname'],
            "email": coach['email'],
            "age": coach['age'],
            "gender": coach['gender'],
            "qualification": coach['qualification'],
            "years_of_experience": coach['years_of_experience'],
            "biography": coach['biography'],
            "field_of_work": coach.get('field_of_work', 'Not available'),
            "image": coach.get('/static/profile-pic-dummy.jpg')
        })
    else:
        return jsonify({"error": "coach not found"}), 404


#connecting the coach and students
@app.route('/connectcoach', methods=['POST'])
def connect_coach():
    
    student_id = session['student_id']  # Get the logged-in student's ID from the session
    coach_id = request.form.get('coach_id')
    
    # Check if the student is logged in
    if 'student_id' not in session:
        return jsonify({"error": "Unauthorized access. Please log in."}), 401


    if not coach_id:
        return jsonify({"error": "Coach ID is required"}), 400

    conn = get_db_connection1()
    cursor = conn.cursor()
    
    try:
        # Insert a new connection with pending status
        cursor.execute(
            'INSERT INTO student_life_coach_map (student_id, coach_id, status) VALUES (%s, %s, "pending")',
            (student_id, coach_id)
        )
        conn.commit()
        return redirect(url_for('lifecoachprofile', coach_id=coach_id))
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

@app.route('/connection-statuss', methods=['GET'])
def connection_statuss():
    coach_id = request.args.get('coach_id')
    student_id = session['student_id'] # Replace with session-based logic

    conn = get_db_connection1()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'SELECT status FROM student_life_coach_map WHERE student_id = %s AND coach_id = %s',
            (student_id, coach_id)
        )
        connection = cursor.fetchone()
        if not connection:
            return jsonify({"connection_status": "connect"})
        return jsonify({"connection_status": connection['status']})
    finally:
        conn.close()

@app.route('/coach-requests')
def coach_requests():
    # Check if the coach is logged in
    if 'coach_id' not in session:
        return jsonify({"error": "Unauthorized access. Please log in."}), 401

    coach_id = session['coach_id']  # Get the logged-in coach's ID from the session
    conn = get_db_connection1()
    cursor = conn.cursor()
    try:
        # Fetch pending requests for the coach
        cursor.execute(
            '''
            SELECT c.id, s.firstname, s.lastname, s.email, c.status
            FROM student_life_coach_map c
            JOIN students_master s ON c.student_id = s.student_id
            WHERE c.coach_id = %s AND c.status = "pending"
            ''',
            (coach_id,)
        )
        requests = cursor.fetchall()
        return render_template('coach_requests.html', requests=requests)
    finally:
        conn.close()


# Handle request accept/decline
@app.route('/handle-request', methods=['POST'])
def handle_request():
    connection_id = request.form.get('connection_id')
    action = request.form.get('action')  # 'accept' or 'decline'

    conn = get_db_connection1()
    cursor = conn.cursor()
    try:
        status = "accepted" if action == "accept" else "declined"
        cursor.execute('UPDATE student_life_coach_map SET status = %s WHERE id = %s', (status, connection_id))
        conn.commit()
        return redirect(url_for('coach_requests'))
    finally:
        conn.close()

    
# Student's connected coaches
@app.route('/student-coaches')
def student_coaches():
    student_id = session['student_id'] # Replace with session-based logic
    conn = get_db_connection1()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'SELECT lc.firstname, lc.lastname, lc.email,c.student_id, c.coach_id '
            'FROM student_life_coach_map c JOIN life_coach_master lc ON c.coach_id = lc.coach_id '
            'WHERE c.student_id = %s AND c.status = "accepted"', 
            (student_id,)
        )
        coaches = cursor.fetchall()
        return render_template('student_coaches.html', coaches=coaches)
    finally:
        conn.close()


# Coach's connected students
@app.route('/coach-students', methods=['GET', 'POST'])
def coach_students():
    # Ensure the coach is logged in
    if 'coach_id' not in session:
        flash("Unauthorized access. Please log in.", "danger")
        return redirect(url_for('lifecoachlogin'))

    coach_id = session['coach_id']  # Retrieve the logged-in coach ID from the session
    conn = get_db_connection1()
    cursor = conn.cursor()

    try:
        if request.method == 'POST':
            # Handle disconnect request
            student_id = request.form.get('student_id')  # Retrieve student_id from form
            if not student_id:
                flash("Student ID is required to disconnect.", "danger")
                return redirect(request.referrer)

            # Validate if the connection exists
            cursor.execute(
                """
                SELECT * FROM student_life_coach_map 
                WHERE coach_id = %s AND student_id = %s
                """,
                (coach_id, student_id)
            )
            connection = cursor.fetchone()

            if not connection:
                flash("Connection not found or unauthorized action.", "danger")
                return redirect(request.referrer)

            # Perform the disconnect operation
            cursor.execute(
                """
                DELETE FROM student_life_coach_map
                WHERE coach_id = %s AND student_id = %s
                """,
                (coach_id, student_id)
            )
            conn.commit()
            flash("Connection successfully disconnected.", "success")
            return redirect(url_for('coach_students'))

        # Fetch the list of students connected to the logged-in coach
        cursor.execute(
            """
            SELECT 
    s.firstname, 
    s.lastname, 
    s.email, 
    c.student_id, 
    c.coach_id
FROM 
    student_life_coach_map c
JOIN 
    students_master s 
ON 
    c.student_id = s.student_id
WHERE 
    c.coach_id = %s 
    AND c.status = 'accepted';

            """, 
            (coach_id,)
        )
        students = cursor.fetchall()

        # Render the coach-students page
        return render_template('coach_students.html', students=students)

    except Exception as e:
        flash(f"Error processing request: {e}", "danger")
        return redirect(url_for('lifecoachlogin'))
    finally:
        conn.close()


@app.route('/disconnectCoach', methods=['POST'])
def disconnectCoach():
    # Check if the user is logged in
    if 'student_id' in session:
        logged_in_user_id = session['student_id']
        user_role = 'student'
    elif 'coach_id' in session:
        logged_in_user_id = session['coach_id']
        user_role = 'coach'
    else:
        flash("Unauthorized access. Please log in.", "danger")
        return redirect(url_for('lifecoachlogin'))
   
    # Retrieve the coach_id or student_id from the form
    connection_coach_id = request.form.get('coach_id')
    connection_student_id = request.form.get('student_id')
    
    # Validate required fields based on user role
    if user_role == 'student' and not connection_coach_id:
        flash("Coach ID is required to disconnect.", "danger")
        return redirect(request.referrer)
    elif user_role == 'coach' and not connection_student_id:
        flash("Student ID is required to disconnect.", "danger")
        return redirect(request.referrer)

    conn = get_db_connection1()
    cursor = conn.cursor()

    try:
        # Validate the connection exists and belongs to the logged-in user
        if user_role == 'student':
            cursor.execute(
                """
                SELECT * FROM student_life_coach_map 
                WHERE student_id = %s AND coach_id = %s
                """, (logged_in_user_id, connection_coach_id)
            )
        else:  # user_role == 'coach'
            cursor.execute(
                """
                SELECT * FROM student_life_coach_map 
                WHERE student_id = %s AND coach_id = %s
                """, (connection_student_id, logged_in_user_id)
            )

        connection = cursor.fetchone()
        if not connection:
            flash("Unauthorized action or connection not found.", "danger")
            return redirect(request.referrer)

        # Delete the connection from the database
        cursor.execute(
            """
            DELETE FROM student_life_coach_map
            WHERE student_id = %s AND coach_id = %s
            """,
            (connection_student_id if user_role == 'coach' else logged_in_user_id,
             connection_coach_id if user_role == 'student' else logged_in_user_id)
        )

        conn.commit()

        flash("Connection successfully disconnected.", "success")
        return redirect(request.referrer)
    except Exception as e:
        conn.rollback()
        flash(f"Error disconnecting: {e}", "danger")
        return redirect(request.referrer)
    finally:
        cursor.close()
        conn.close()


@app.route('/parentlogin')
def parentlogin():
    return render_template("parentlogin.html")

@app.route('/parentregister')
def parentregister():
    return render_template("parentregister.html")

@app.route('/parenthome')
def parenthome():
    return render_template("parenthome.html")

@app.route('/parentregisterform', methods=['GET', 'POST'])
def parentregisterform():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']
        state = request.form['state']
        
        hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
        
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO parents_master (firstname, lastname, email, password, age, gender, state)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (firstname, lastname, email, hashed_password, age, gender, state))
            conn.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('parentlogin'))
        except Exception as e:
            flash('Error during registration: ' + str(e), 'danger')
        finally:
            cursor.close()
            conn.close()
    return render_template('parentregister.html')

@app.route('/parentloginform', methods=['GET', 'POST'])
def parentloginform():
    if 'email' in session:
        return redirect(url_for('parenthome'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT password FROM parents_master WHERE email=%s
            """, (email,))
            result = cursor.fetchone()

            if result and checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                session['email'] = email
                flash('Login successful!', 'success')
                return redirect(url_for('parenthome'))
            else:
                flash('Invalid email or password', 'danger')
        except Exception as e:
            flash('Error during login: ' + str(e), 'danger')
        finally:
            cursor.close()
            conn.close()
    return render_template('parentlogin.html')


@app.route('/parentmainhome')
def parentmainhome():
    return render_template("parentmainhome.html")



@app.route('/plogout')
def plogout():
    session.pop('email', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('parentlogin'))



#chat
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/chat', methods=['POST'])
def chats():
    sender_id = request.form.get('sender_id')
    receiver_id = request.form.get('receiver_id')
    return render_template('chat.html', sender_id=sender_id, receiver_id=receiver_id)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    message = data['message']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (sender_id, receiver_id, message, timestamp) VALUES (%s, %s, %s, NOW())",
        (sender_id, receiver_id, message)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'status': 'Message sent successfully'})

@app.route('/fetch_messages', methods=['POST'])
def fetch_messages():
    data = request.json
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT sender_id, receiver_id, message, timestamp 
        FROM messages 
        WHERE (sender_id = %s AND receiver_id = %s) 
           OR (sender_id = %s AND receiver_id = %s) 
        ORDER BY timestamp ASC
        """,
        (sender_id, receiver_id, receiver_id, sender_id)
    )
    messages = cursor.fetchall()
    
    
    
    cursor.close()
    conn.close()
    
    return jsonify(messages)


#quiz
def get_questions_from_db():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()

    for question in questions:
        question_id = question['id']
        cursor.execute("SELECT * FROM answers WHERE question_id = %s", (question_id,))
        question['answers'] = cursor.fetchall()

    cursor.close()
    connection.close()
    return questions

@app.route('/quiz')
def quiz():
    questions = get_questions_from_db()
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    questions = get_questions_from_db()
    total_score = 0
    
    # Process user answers
    for question in questions:
        question_id = str(question["id"])
        selected_answer_id = request.form.get(question_id)  # Fetch selected answer ID for the question
        if selected_answer_id:
            for answer in question["answers"]:
                if answer["id"] == int(selected_answer_id) and answer["is_correct"]:
                    total_score += 1

    return render_template('results.html', score=total_score)

if __name__=='__main__':
    app.run(debug=True)
