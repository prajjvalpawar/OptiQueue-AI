import sqlite3

def setup_database():
    with sqlite3.connect('healthcare.db') as conn:
        cursor = conn.cursor()
        
        # 1. Specialists Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS doctors 
                          (id INTEGER PRIMARY KEY, 
                           name TEXT, 
                           specialization TEXT, 
                           fee INTEGER, 
                           experience TEXT, 
                           success_rate TEXT)''')
        
        # 2. Patient Records Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS patients 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           name TEXT, 
                           mobile TEXT, 
                           age INTEGER, 
                           gender TEXT, 
                           visit_type TEXT, 
                           ai_result TEXT, 
                           assigned_doctor TEXT,
                           timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        
        # Initialize Doctors if table is empty
        cursor.execute("SELECT COUNT(*) FROM doctors")
        if cursor.fetchone()[0] == 0:
            doctors = [
                ('Dr. Sharma', 'Cataracts', 500, '15 Years', '98%'),
                ('Dr. Verma', 'Glaucoma', 700, '20 Years', '95%'),
                ('Dr. Iyer', 'Uveitis', 600, '12 Years', '92%'),
                ('Dr. Reddy', 'Bulging Eyes', 800, '18 Years', '97%'),
                ('Dr. Kapoor', 'Crossed Eyes', 550, '10 Years', '94%')
            ]
            cursor.executemany("INSERT INTO doctors (name, specialization, fee, experience, success_rate) VALUES (?, ?, ?, ?, ?)", doctors)
        conn.commit()

def save_patient_record(name, mobile, age, gender, visit_type, ai_result, doctor):
    with sqlite3.connect('healthcare.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO patients (name, mobile, age, gender, visit_type, ai_result, assigned_doctor) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)""",
                       (name, mobile, age, gender, visit_type, ai_result, doctor))
        conn.commit()

def delete_patient(patient_id):
    with sqlite3.connect('healthcare.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
        conn.commit()