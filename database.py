# Import SQLite and connect to database
import sqlite3
conn = sqlite3.connect('./db/hospital.db')

# Create cursor
c = conn.cursor()


# This function generates the initial tables if they are not present
def create_tables():
    # Create a table where a unique ROW ID gets assigned for each patient
    c.execute("""
        CREATE TABLE IF NOT EXISTS patient(
            name text NOT NULL,
            address text,
            phone text
        );
    """)

    # Create a table for receptionists
    c.execute("""
        CREATE TABLE IF NOT EXISTS receptionist(
            employee_num text NOT NULL PRIMARY KEY,
            name TEXT NOT NULL);
    """)

    # Create a table for healthcare professionals which keeps records of all hospital staff
    # i.e. Doctor or Nurse
    c.execute("""
        CREATE TABLE IF NOT EXISTS healthcare_professional(
            employee_num text NOT NULL PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            occupied INTEGER,
            CONSTRAINT valid_occupy CHECK (occupied IN (0,1)),
            CONSTRAINT validate_role CHECK (role IN ('doctor','nurse'))
        );
    """)

    # Create a table for prescriptions
    # Entries are updated when a doctors issues a prescription
    c.execute("""
        CREATE TABLE IF NOT EXISTS prescription(
            type TEXT,
            pat_id INTEGER,
            doc_id INTEGER,
            quantity INTEGER,
            dosage REAL
        );
    """)

    # Create a table for appointment requests
    # The pat_id references to the unique row id of the patient table
    # The staff_id references to the employee number of the healthcare_professional table
    c.execute("""
        CREATE TABLE IF NOT EXISTS appointment(
            type TEXT,
            staff_id INTEGER NOT NULL,
            pat_id INTEGER NOT NULL,
            FOREIGN KEY (staff_id) references healthcare_professional(employee_num),
            FOREIGN KEY (pat_id) references patient(rowid)
        );
    """)

    # Create a table for confirmed appointments
    # The pat_id references to the unique row id of the patient table
    # The staff_id references to the employee number of the healthcare_professional table
    c.execute("""
        CREATE TABLE IF NOT EXISTS appointment_schedule(
            type TEXT,
            staff_id INTEGER NOT NULL,
            pat_id INTEGER NOT NULL,
            FOREIGN KEY (staff_id) references healthcare_professional(employee_num),
            FOREIGN KEY (pat_id) references patient(rowid)
        );
    """)
