import sqlite3

from HealthcareProfessional import HealthcareProfessional
from clearConsole import clearConsole
from database import c, conn


class Doctor(HealthcareProfessional):
    def __init__(self):
        pass

    # Function to check if a doctor exists
    def doctor_exists(self, employee_num, name):
        c.execute(f"""
            SELECT employee_num from healthcare_professional
            where employee_num = "{employee_num}"
            AND name = "{name}"
        """)
        found = c.fetchone()
        return found and employee_num in found

    # Login function to enter the doctor's menu
    def doctor_login(self):
        clearConsole()
        try:
            employee_num = input("Enter your employee number: ")
            name = input("Enter your name: ")

            if self.doctor_exists(employee_num, name):
                clearConsole()
                self.menu(employee_num)
            else:
                print("Doctor record not found.")
                exit()
        except ValueError:
            print("Entered ID must be a number and name cannot contain numbers.")
        return

    # Doctor's menu
    def menu(self, employee_num):
        clearConsole()
        print("----Doctor's MENU----")
        print("1. View prescription requests")
        print("q. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            self.view_prescription_requests(employee_num)
        elif choice == 'q' or choice == 'Q':
            clearConsole()
            exit()
        else:
            print("Invalid choice")

    # This function fetches all prescription requests for this doctor
    # and allows them to issue the prescription
    def view_prescription_requests(self, employee_num):
        c.execute(f"""
            SELECT rowid,* from prescription
            WHERE ifnull(quantity, '') = '' AND ifnull(dosage, '') = ''
            AND doc_id={int(employee_num)}
        """)
        prescription_requests = c.fetchall()
        if len(prescription_requests) > 0:  # check if there are any appointments
            print("Prescription requests:")

            for prescription in prescription_requests:
                print(f"""
                    Prescription ID : {prescription[0]}
                    Type            : {prescription[1]}
                    Patient's ID    : {prescription[2]}
                """)
        else:
            print("No records found.")

        print("-----SELECT AN OPTION-----")
        print("1: Issue prescription")
        print("2: Go back")

        choice = input("Enter Choice: ")
        if choice == '1':
            self.issue_prescription(employee_num)
        elif choice == '2':
            self.menu(employee_num)

    # This function updated the prescriptions requests by entering the
    # quantity and the dosage of the requested prescription
    def issue_prescription(self, employee_num):
        pre_id = int(input("Enter Prescription ID to be issued: "))
        quantity = int(input("Enter the quantity for the prescription: "))
        dosage = float(input("Enter the dosage for the prescription: "))

        try:
            c.execute(f"""
                UPDATE prescription 
                SET quantity={quantity}, dosage={dosage}
                WHERE rowid={pre_id}
            """)

            c.execute(f"""
                UPDATE healthcare_professional 
                SET occupied=0
                WHERE employee_num={employee_num}
            """)

            conn.commit()
            print("--------------------------------------------------------------")
            print("Prescription successfully issued")
            print("Prescription Number: ", pre_id)
            print("--------------------------------------------------------------")
            self.menu(employee_num)
        except sqlite3.Error as er:
            print("ERROR!", er)
