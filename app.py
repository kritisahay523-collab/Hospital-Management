from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

# -------------------- DATABASE CONNECTION --------------------
def get_db_connection():
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12806448",
        password="uyyq4XUH5A",
        database="sql12806448"
    )

# -------------------- HOME PAGE --------------------
@app.route('/')
def home():
    return render_template('home.html')


# -------------------- PATIENT REGISTRATION --------------------
@app.route('/Registration')
def patient_register():
    return render_template('Registration.html')


@app.route('/register_patient', methods=['POST'])
def register_patient():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    username = request.form['username']
    password = request.form['password']
    contact_number = request.form['contact_number']
    address = request.form['address']
    email_id = request.form['email_id']
    city = request.form['city']
    pincode = request.form['pincode']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO patients (name, age, gender, username, password, contact_number, address, email_id, city, pincode)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (name, age, gender, username, password, contact_number, address, email_id, city, pincode))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('login'))


# -------------------- PATIENT LOGIN --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM patients WHERE username=%s AND password=%s", (username, password))
        patient = cur.fetchone()
        cur.close()
        conn.close()

        if patient:
            session['patient_id'] = patient['patient_id']
            session['name'] = patient['name']
            return redirect(url_for('patient_details'))
        else:
            return "<h3>❌ Invalid username or password</h3><a href='/login'>Try again</a>"

    return render_template('login.html')


# -------------------- PATIENT DASHBOARD --------------------
@app.route('/PatientDetails')
def patient_details():
    if 'patient_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM patients WHERE patient_id = %s", (session['patient_id'],))
    patient = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('Patient Details.html', patient=patient)


# -------------------- PRESCRIPTIONS --------------------
@app.route('/prescription')
def prescription():
    if 'patient_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM prescriptions WHERE patient_id = %s", (session['patient_id'],))
    prescriptions = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('prescription.html', prescriptions=prescriptions)


# -------------------- DOCTOR REGISTRATION --------------------
@app.route('/DoctorRegister')
def doctor_register():
    return render_template('Doctor Register.html')


@app.route('/register_doctor', methods=['POST'])
def register_doctor():
    name = request.form['name']
    specialization = request.form['specialization']
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO doctors (name, specialization, username, password)
        VALUES (%s, %s, %s, %s)
    """, (name, specialization, username, password))
    conn.commit()
    cur.close()
    conn.close()

    return "<h3>✅ Doctor Registered Successfully!</h3><a href='/DoctorLogin'>Go to Login</a>"


# -------------------- DOCTOR LOGIN --------------------
@app.route('/DoctorLogin', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM doctors WHERE username=%s AND password=%s", (username, password))
        doctor = cur.fetchone()
        cur.close()
        conn.close()

        if doctor:
            session['doctor_name'] = doctor['name']
            return redirect(url_for('doctor_dashboard'))
        else:
            return "<h3>❌ Invalid username or password</h3><a href='/DoctorLogin'>Try again</a>"

    return render_template('Doctor Login.html')


# -------------------- DOCTOR DASHBOARD --------------------
@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'doctor_name' not in session:
        return redirect(url_for('doctor_login'))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('prescription.html', patients=patients, doctor_name=session['doctor_name'])


# -------------------- LOGOUT --------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# -------------------- RUN APP --------------------
if __name__ == "__main__":
    app.run(debug=True)
