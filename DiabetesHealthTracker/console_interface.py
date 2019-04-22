import pickle
import os.path
import datetime
from user import User
from record import Record
from day import Day

# TODO: Docstrings.

def console_interface():
    done_with_program = False
    QUIT = "QUIT"
    extension = ".dbhat"
    while not done_with_program:

        username = input("Enter name ('QUIT' to quit): ").replace(" ", "")
        if username == QUIT:
            return
        elif os.path.isfile(username+extension):
            userfile = open(username+extension, "rb")
            the_user = pickle.load(userfile)
            userfile.close()
            done_with_program = console_main_menu(the_user)
            userfile = open(username+extension, "wb")
            pickle.dump(the_user, userfile)
            userfile.close()
        else:
            print("User file not found. Enter '1' to create a new one.")
            choice = input()
            if choice == "1":
                the_user = User(username)
                done_with_program = console_main_menu(the_user)
                userfile = open(username+extension, "wb+")
                pickle.dump(the_user, userfile)


def console_main_menu(a_user) -> bool:
    QUIT = 5
    choice = 0
    while choice != QUIT:
        print("MAIN MENU")
        print("1. Add record")
        print("2. View/Edit records")
        print("3. Calculate averages")
        print("4. Change user")
        print("5. Quit")

        choice = int(input("\nEnter number: "))
        if choice == 1:
            console_add_record(a_user)
        elif choice == 2:
            console_view_records(a_user)
        elif choice == 3:
            console_view_averages(a_user)
        elif choice == 4:
            return False
        elif choice == 5:
            return True
        else:
            print("Number out of range.")


def console_view_averages(a_user):
    if a_user.first_day is None:
        print("No records found. Averages unavailable.\n")
    else:
        days_back = int(input("Enter days to go back (0 means today): "))
        if days_back >= 0:
            glucose_average = a_user.calculate_average_glucose(days_back)
            carbs_per_meal_average = a_user.calculate_average_carbs_per_meal(days_back)
            time_active_average = a_user.calculate_average_time_active(days_back)
            average_meals_missed = a_user.calculate_average_meals_missed(days_back)

            print(str.format("Glucose:      {:9}    Rating: {}", glucose_average,
                             a_user.get_glucose_rating(glucose_average)))
            print(str.format("Activity:     {:5} min    Rating: {}", time_active_average,
                             a_user.get_time_active_rating(time_active_average)))
            print(str.format("Carbs/meal:   {:9}    Rating: {}", carbs_per_meal_average,
                             a_user.get_carbs_per_meal_rating(carbs_per_meal_average)))
            print(str.format("Meals missed: {:9}    Rating: {}", average_meals_missed,
                             a_user.get_meals_missed_rating(average_meals_missed)))
            print()


def console_view_records(a_user):
    current_day = a_user.last_day
    QUIT = 4
    choice = 0
    if a_user.last_day is None:
        print("No days found.\n")
    else:
        while choice != QUIT:
            print(current_day)

            print("1. Previous day")
            print("2. Edit a record")
            print("3. Next day")
            print("4. Quit")

            choice = int(input("\nEnter number: "))
            while choice < 1 or choice > 4:
                print("Number not in range.")
                choice = int(input("Enter number: "))

            if choice == 1:
                if current_day.previous_day is None:
                    print("Currently at earliest recorded day.")
                else:
                    current_day = current_day.previous_day
            elif choice == 3:
                if current_day.next_day is None:
                    print("Currently at latest recorded day.")
                else:
                    current_day = current_day.next_day
            elif choice == 2:
                console_choose_record_to_edit(current_day)
            else:
                return


def console_choose_record_to_edit(a_day):
    QUIT = 4

    print("1. Morning record")
    print("2. Evening record")
    print("3. Night record")
    print("4. Back")

    choice = int(input("\nEnter number: "))
    while choice < 1 or choice > 4:
        print("Number not in range.")
        choice = int(input("Enter number: "))

    if choice == 1:
        console_edit_record(a_day.morning_record)
    elif choice == 2:
        console_edit_record(a_day.evening_record)
    elif choice == 3:
        console_edit_record(a_day.night_record)
    else:
        return


def console_edit_record(a_record):
    QUIT = 5
    choice = 0

    while choice != QUIT:
        print(a_record)

        print("1. Edit glucose")
        print("2. Edit meal & Carbs")
        print("3. Edit activity information")
        print("4. Edit mood")
        print("5. Back")

        choice = int(input("\nEnter number: "))
        while choice < 1 or choice > 5:
            print("Number out of range.")
            choice = int(input("Enter number: "))

        if choice == 1:
            a_record.glucose = int(input("Enter new glucose: "))
        elif choice == 2:
            meal = input("Enter new meal (0 for nothing): ")
            if meal != "0":
                a_record.carbs = int(input("Enter new carb amount: "))
            else:
                a_record.carbs = 0
                meal = ""
            a_record.meal = meal
        elif choice == 3:
            activity = input("Enter new activity (0 for nothing): ")
            if activity == "0":
                activity = ""
                activity_start_time = None
                activity_end_time = None
            else:
                activity_start_time = datetime.datetime.strptime(input("Enter start time (h:m AM/PM): "), "%I:%M %p")
                activity_end_time = datetime.datetime.strptime(input("Enter end time (h:m AM/PM): "), "%I:%M %p")
            a_record.activity = activity
            a_record.activity_start_time = activity_start_time
            a_record.activity_end_time = activity_end_time
        elif choice == 4:
            a_record.mood = input("Enter new mood:")
        else:
            return


def console_add_record(a_user):
    good_format = False
    while not good_format:
        date_string = input("Enter date for record (MM/DD/YYYY, 0 for today: ")
        if date_string != "0":
            try:
                date_obj = datetime.datetime.strptime(date_string, '%m/%d/%Y').date()
                good_format = True
            except ValueError:
                print("Accepted inputs are 0 or the format MM/DD/YYYY. Try again.")
        else:
            good_format = True
            date_obj = datetime.datetime.today().date()

    current_day = Day(date_of_day=date_obj)

    if not a_user.insert_day_in_list(current_day):
        current_day = a_user.last_day
        while current_day.date_of_day != date_obj:
            current_day = current_day.previous_day

    print("Add record for:")
    print("1. Morning")
    print("2. Evening")
    print("3. Night")
    print("4. Quit")

    choice = int(input("\nEnter number: "))

    while choice < 1 or choice > 4:
        print("Invalid entry.")
        choice = int(input("Enter number:"))

    if choice != 4:
        if choice == 1:
            current_day.morning_record = console_create_record()
        elif choice == 2:
            current_day.evening_record = console_create_record()
        else:
            current_day.night_record = console_create_record()


def console_create_record() -> Record:
    glucose = int(input("Enter glucose: "))
    meal = input("Enter meal (0 for none): ")
    if meal != "0":
        carbs = int(input("Enter carbs: "))
    else:
        meal = ""
        carbs = 0
    activity = input("Enter activity (0 for none): ")
    if activity != "0":
        good_format = False
        while not good_format:
            try:
                activity_start_time = datetime.datetime.strptime(input("Enter start time (h:m AM/PM): "), "%I:%M %p")
                activity_end_time = datetime.datetime.strptime(input("Enter end time (h:m AM/PM): "), "%I:%M %p")
                good_format = True
            except ValueError:
                print("Invalid time formats. Please enter in hh:mm AM/PM format.")
    else:
        activity = ""
        activity_start_time = None
        activity_end_time = None
    mood = input("Enter mood: ")

    return Record(glucose=glucose, meal=meal, carbs=carbs, activity=activity,
                  activity_start_time=activity_start_time,
                  activity_end_time=activity_end_time, mood=mood)
