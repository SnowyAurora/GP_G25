from login import Login

def main():
    user = Login()
    main_menu(user)

def main_menu(user):
    while True:
        print("\n--- Main Menu ---")
        print("1. Log in as Medical Staff")
        print("2. Log in as Admin Staff")
        print("3. Log in as Patient")
        print("4. Quit Program")

        choice = input("Please enter your choice: ").strip()
        if choice == "1":
            staff_login(user)
        elif choice == "2":
            admin_login(user)
        elif choice == "3":
            patient_login(user)
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please try again.")


def staff_login(user):
    login_username = input("Enter staff username: ")
    login_password = input("Enter staff password: ")

    staff_user = user.check_valid_username_password_medstaff(login_username, login_password)
    if not staff_user:
        print("Invalid username or password.")
        return

    print(f"\nLogin successful. Welcome, {staff_user.name}.")
    staff_menu(user, staff_user)

def staff_menu(user, staff_user):
    while True:
        print("\n--- Staff Menu ---")
        print("1. Log patient medical observations")
        print("2. Log patient personal preferences")
        print("3. View patient log record")
        print("4. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "4":
            print("Logging out.")
            break
        elif choice in ["1", "2"]:
            patient = get_valid_patient(user)
            if not patient:
                continue
            if choice == "1":
                user.input_patient_clinical_observation(patient.username, staff_user.username)
            elif choice == "2":
                user.input_patient_personal_preference(patient.username, staff_user.username)
            
        elif choice == "3":
            result = user.get_patient_records_staff()
            print(result)
        else:
            print("Invalid option. Please try again.")

def patient_login(user):
    login_username = input("Enter patient username: ")
    login_password = input("Enter patient password: ")

    patient_user = user.check_valid_username_password_patient(login_username, login_password)
    if not patient_user:
        print("Invalid username or password.")
        return

    print(f"\nLogin successful. Welcome, {patient_user.username}.")
    patient_menu(user, patient_user)


def patient_menu(user, patient_user):
    while True:
        print("\n--- Patient Menu ---")
        print("1. Log personal preference")
        print("2. Retrieve personal preference logs")
        print("3. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            user.input_patient_personal_preference(patient_user.username, patient_user.username)        
        elif choice == "2":
            result = user.get_patient_records_patient(patient_user.username)
            print(result)
        elif choice == "3":
            print("Logging out.")
            break
        else:
            print("Invalid option. Please try again.")

def admin_menu(user, admin_user):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Register new patient")
        print("2. Remove existing patient")
        print("3. Assign care staff to patient")
        print("4. List all existing medical staff")
        print("5. List all existing patients")
        print("6. Register new medical staff")
        print("7. Remove existing medical taff")
        print("8. Logout")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            user.register_new_patient()
        elif choice == "2":
            user.remove_patient()
        elif choice == "3":
            patient = get_valid_patient(user)

            staff_to_assign = get_valid_med_staff(user)
            if staff_to_assign:
                user.assign_care_staff(patient.username, staff_to_assign.username)
                print("Staff assigned successfully.")
        elif choice == "4":
            result = user.list_all_medical_staff()
            print(result)
        elif choice == "5":
            result = user.list_all_patients()
            print(result)
        elif choice == "6":
            user.register_staff()
            print("Staff registered successfully")
        elif choice == "7":
            user.remove_staff()
            print("Staff removed successfully")

        elif choice == "8":
            print("Logging out.")
            break
        else:
            print("Invalid option. Please try again")

def admin_login(user):
    login_username = input("Enter admin username: ")
    login_password = input("Enter admin password: ")
    admin_user = user.check_valid_username_password_admin(login_username, login_password)
    print(type(admin_user))
    if not admin_user:
        print("Invalid username or password")
        return

    print(f"\nLogin successful. Welcome, {admin_user.username}.")
    admin_menu(user, admin_user)

def get_valid_patient(user):
    """Prompt for a valid patient username."""
    while True:
        username = input("Enter patient username: ").strip()
        patient = user.find_patient_by_username(username)
        if patient:
            return patient
        print("Invalid patient username. Try again or type 'cancel' to stop.")
        if username.lower() == "cancel":
            return None

def get_valid_med_staff(user):
    """Prompt for a valid staff name."""
    while True:
        name = input("Enter staff name: ").strip()
        staff = user.find_medstaff_by_name(name)
        if staff:
            return staff
        print("Invalid staff name. Try again or type 'cancel' to stop.")
        if name.lower() == "cancel":
            return None
        
def get_valid_admin(user):
    while True:
        username = input("Enter admin username: ").strip()
        admin = user.find_patient_by_name(username)
        if admin:
            return admin
        print("Invalid patient username. Try again or type 'cancel' to stop.")
        if username.lower() == "cancel":
            return None

if __name__ == "__main__":
    main()
