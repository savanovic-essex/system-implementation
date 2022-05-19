import sqlite3

from clearConsole import clearConsole
from database import c, conn


class Patient:
    def __init__(self):
        pass

    # Function to check if a patient exists
    def patient_exists(self, patient_id, name):
        c.execute(f"""
            SELECT rowid from patient
            where rowid = {patient_id}
            AND name = "{name}"
        """)
        found = c.fetchone()
        return found and patient_id in found

    # Login function to enter the patient's menu
    def patient_login(self):
        clearConsole()
        try:
            patient_id = int(input("Enter your ID: "))
            name = input("Enter your name: ")

            if self.patient_exists(patient_id, name):
                clearConsole()
                self.menu(patient_id)
            else:
                print("Patient record not found.")
                exit()
        except ValueError:
            print("Entered ID must be a number and name cannot contain numbers.")

    # This function fetches all available doctors
    def fetch_doctors(self):
        c.execute("""
            SELECT * from healthcare_professional
            where occupied=0 AND role='doctor'
        """)

        staff_list = c.fetchall()
        if len(staff_list) > 0:  # Check if there are any doctors available
            print("Available doctors:")

            for staff in staff_list:
                print(f"""
                    DOCTOR'S ID   : {staff[0]}
                    NAME          : {staff[1]}
                """)
        else:
            print("No available doctors at this time.")
        return len(staff_list)

    # Patient's menu
    def menu(self, patient_id):
        clearConsole()
        print("----Patient's MENU----")
        print("1. Request an appointment")
        print("2. Request a prescription")
        print("q. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            self.request_appointment(patient_id)
        elif choice == "2":
            self.request_prescreption(patient_id)
        elif choice == 'q' or choice == 'Q':
            clearConsole()
            exit()
        else:
            print("Invalid choice")

    # Function for requesting prescriptions
    # It creates an entry in the prescription table, which is later updated by a doctor,
    # when they issue the aforementioned prescription
    def request_prescreption(self, patient_id):
        if (self.fetch_doctors()) <= 0:
            self.menu(patient_id)
        else:
            type = input("Enter prescription type: ")
            doctor = int(input("Enter doctor's ID: "))
            try:
                c.execute(f"""
                INSERT INTO prescription VALUES(
                    "{type}",
                    {patient_id},
                    {doctor},
                    NULL,
                    NULL
                )
                """)

                print("--------------------------------------------------------------")
                print("Prescription successfully requested")
                _prescriptionID = c.lastrowid
                print("Prescription Number: ", _prescriptionID)
                print("--------------------------------------------------------------")

                conn.commit()
                self.menu(patient_id)
            except sqlite3.Error as er:
                print("ERROR!", er)

    # Function for requesting appointments
    # It creates an entry in the appointment table, which is later deleted by a receptionist,
    # when they confirm the aforementioned appointment - it later on creates an entry in the
    # appointment_schedule table
    def request_appointment(self, patient_id):
        c.execute("""
            SELECT * from healthcare_professional
            where occupied=0 AND role='doctor'
        """)

        staff_list = c.fetchall()
        if len(staff_list) > 0:  # check if there are doctors available
            print("Available doctors:")

            for staff in staff_list:
                print(f"""
                    NUMBER     : {staff[0]}
                    NAME       : {staff[1]}
                    DESIGNATION: {staff[2]}
                """)

            staff_choice = input("Enter Doctor ID: ")

            try:
                c.execute(f"""
                INSERT INTO appointment VALUES(
                    "appointment",
                    {staff_choice},
                    {patient_id})
                """)

                print("--------------------------------------------------------------")
                print("Appointment successfully requested")
                _appointmentID = c.lastrowid
                print("Appointment Number: ", _appointmentID)
                print("--------------------------------------------------------------")

                conn.commit()
                self.menu(patient_id)
            except sqlite3.Error as er:
                print("ERROR!", er)
        else:
            print("No available doctors at this time.")
            self.menu(patient_id)
