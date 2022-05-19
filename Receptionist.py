import sqlite3

from clearConsole import clearConsole
from database import c, conn


class Receptionist:
    def __init__(self):
        pass

    # Function to check if the receptionist exists
    def receptionist_exists(self, employee_num, name):
        c.execute(f"""
            SELECT rowid,* from receptionist
            where employee_num = {employee_num}
            AND name = "{name}"
        """)
        found = c.fetchone()
        return found and employee_num in found

    # Login function to enter the receptionist's menu
    def receptionist_login(self):
        clearConsole()
        try:
            employee_num = int(input("Enter your Employee Number: "))
            name = input("Enter your name: ")

            if self.receptionist_exists(employee_num, name):
                clearConsole()
                self.menu()
            else:
                print("Employee record not found.")
                exit()
        except ValueError:
            print("Entered ID must be a number and name cannot contain numbers.")

    # Receptionist's menu
    def menu(self):
        clearConsole()
        print("----Receptionist's MENU----")
        print("1: View confirmed appointments")
        print("2: View appointment requests")
        print("q: Exit")

        choice = input("Enter Choice: ")
        if choice == '1':
            self.view_appointments()
        elif choice == '2':
            self.view_appointment_requests()
        elif choice == 'q' or choice == 'Q':
            clearConsole()
            exit()
        else:
            print("Invalid choice")

    # Function for fetching all appointments
    # "type" argument is used to decide whether to fetch requests or confirmed appointments
    def fetch_appointments(self, type):
        c.execute(f"""
            SELECT rowid,* from {type} 
        """)
        appointments = c.fetchall()
        if len(appointments) > 0:  # Check if there are any appointments
            if type == "appointment_schedule":
                print("Appointments:")
            else:
                print("Appointment requests:")

            for appointment in appointments:
                print(f"""
                    APPOINTMENT ID  : {appointment[0]}
                    DOCTOR'S ID     : {appointment[2]}
                    PATIENT'S ID    : {appointment[3]}
                """)
        else:
            print("No records found.")
        return

    # View all confirmed appointments
    # Choose to cancel an appointment or to leave the menu
    def view_appointments(self):
        print(self.fetch_appointments("appointment_schedule"))

        print("-----SELECT AN OPTION-----")
        print("1: Cancel an appointment")
        print("2: Go back")

        choice = input("Enter Choice: ")
        if choice == '1':
            self.cancel_appointment("appointment_schedule")
        elif choice == '2':
            self.menu()

    # View all appointment requests
    # Choose to approve or cancel an appointment requests or leave the menu
    def view_appointment_requests(self):
        print(self.fetch_appointments("appointment"))

        print("-----SELECT AN OPTION-----")
        print("1: Confirm an appointment")
        print("2: Cancel an appointment")
        print("3: Go back")

        choice = input("Enter Choice: ")
        if choice == '1':
            self.make_appointment()
        elif choice == '2':
            self.cancel_appointment("appointment")
        elif choice == '3':
            self.menu()

    # Confirm an appointment and add it to the appointment schedule
    def make_appointment(self):
        print("Enter the appointment ID you want to confirm")
        app_id = int(input("Appointment ID: "))

        try:
            # Fetch appointment data from appointment table (appointment requests from patients)
            c.execute(f"""
                SELECT * from appointment 
                WHERE rowid={app_id}
            """)
            appointment = c.fetchone()

            # Insert appointment data into appointment_schedule table (appointment confirmed/made by the receptionist)
            c.execute(f"""
                INSERT INTO appointment_schedule VALUES(
                    "appointment",
                    {int(appointment[1])},
                    {int(appointment[2])})
            """)

            # Delete appointment request from appointment table after confirming it
            c.execute(f"""
                DELETE FROM appointment
                WHERE rowid={app_id}
            """)

            # Sets the doctor as occupied when the appointment is confirmed
            c.execute(f"""
                UPDATE healthcare_professional 
                SET occupied=1
                WHERE employee_num={int(appointment[1])}
            """)

            conn.commit()
            print(f"Successfully confirmed appointment {app_id}")
            self.menu()
        except sqlite3.Error as er:
            print("Could not confirm!", er)

    # Cancel an appointment
    # "type" argument is used to decide whether to cancel requests or confirmed appointments
    def cancel_appointment(self, type):
        app_id = int(input("Enter Appointment ID to be removed: "))
        try:
            c.execute(f"""
            DELETE FROM {type}
            WHERE rowid={app_id}
        """)

            conn.commit()
            print(f"Successfully canceled appointment {app_id}")
            self.menu()
        except sqlite3.Error as er:
            print("Could not delete!", er)
