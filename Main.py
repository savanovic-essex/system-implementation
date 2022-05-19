import os

# Create the database directory if it does not exist
if not os.path.exists('db'):
    os.mkdir('db')

from database import create_tables
from Doctor import Doctor
from Patient import Patient
from Receptionist import Receptionist


# Main function which is initialized on programme start
def main():
    create_tables()

    print("----WELCOME MENU----")
    print("1: Doctor Login")
    print("2: Receptionist Login")
    print("3: Patient Login")

    choice = input("Enter Choice: ")
    if choice == '1':
        d = Doctor()
        d.doctor_login()
    elif choice == '2':
        r = Receptionist()
        r.receptionist_login()
    if choice == '3':
        p = Patient()
        p.patient_login()
    elif choice == 'q' or choice == 'Q':
        exit()
    else:
        print("Invalid Choice")


if __name__ == "__main__":
    main()
