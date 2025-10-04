from login import Login

def main():
    user = Login()

    while True:
        print("1. Log in as medical_staff")
        print("2. Log in as patient")
        print("3. Quit Program")
        choice_identity = int(input("Please enter number choice: "))

        if choice_identity == 3:
            print("Exiting program")
            break

        if choice_identity == 1:
            login_username = input("Please enter staff login username: ")
            login_password = input("Please enter staff password: ")
            result = user.check_valid_username_password_medstaff(login_username, login_password)
            if not result:
                print("Invalid username or password")
                continue

            print("\nLogin successful as Medical Staff")

            while True:
                print("\n--- Staff Menu ---")
                print("1. Log patient medical observations")
                print("2. Log patient personal preferences")
                print("3. Assign care staff to patient")
                print("4. Logout")
                choice = int(input("Please enter number choice: "))

                if choice == 4:
                    print("Logging out")
                    break

                while True:
                    patient_username = input("Enter patient username: ")
                    val_patient = user.find_patient_by_username(patient_username)
                    if val_patient:
                        break
                    else:
                        print("Invalid patient username")

                if choice == 1:
                    user.input_patient_clinical_observation(patient_username, result.username)
                elif choice == 2:
                    user.input_patient_personal_preference(patient_username, result.username)
                elif choice == 3:
                    while True:
                        assigned_staff = input("Please enter to be assigned staff name: ")
                        staff = user.find_medstaff_by_name(assigned_staff)
                        if staff:
                            user.assign_care_staff(patient_username, staff.username)
                            print("Assigned successfully")
                            break
                        else:
                            print("Invalid staff")

        elif choice_identity == 2:
            login_username = input("Please enter patient login username: ")
            login_password = input("Please enter patient password: ")
            result = user.check_valid_username_password_patient(login_username, login_password)
            if not result:
                print("Invalid username or password")
                continue

            print("\nLogin successful as Patient")

            while True:
                print("\n--- Patient Menu ---")
                print("1. Log personal preference")
                print("2. Logout")
                choice = int(input("Please enter number choice: "))

                if choice == 2:
                    print("Logging out")
                    break
                elif choice == 1:
                    user.input_patient_personal_preference(result.username, result.username)


if __name__ == "__main__":
    main()
