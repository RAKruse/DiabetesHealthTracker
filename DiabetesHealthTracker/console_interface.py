import pickle
import os.path
import datetime
from user import User
from record import Record
from day import Day


def console_interface():
    """Top-level function for console interface.

    Handles user creation, user login, and quitting.
    Responsible for loading and saving binary files."""
    done_with_program = False
    QUIT = "QUIT"   # Sentinel value
    extension = ".dbhat"

    # While the program has yet do finish:
    while not done_with_program:

        # Get the username
        username = input("Enter name ('QUIT' to quit): ").replace(" ", "")

        # If the username is the sentinel value of "QUIT", exit the program.
        if username == QUIT:
            return

        # Otherwise, if the user's file exists:
        elif os.path.isfile(username+extension):
            # Open, read data from, and close the user's file
            userfile = open(username+extension, "rb")
            the_user = pickle.load(userfile)
            userfile.close()

            # Run a quick update function on the data
            the_user._update_days()

            # Enter into the console interface's main menu
            done_with_program = console_main_menu(the_user)

            # When the user has finished, remove all empty days from the data
            the_user._cleanup_empty_days()

            # Open, write data to, and close the user's file
            userfile = open(username+extension, "wb")
            pickle.dump(the_user, userfile)
            userfile.close()

        # Otherwise, inform the user that the file wasn't found.
        else:
            # Inform and prompt user.
            print("User file not found. Enter '1' to create a new one.")
            choice = input()

            # If the user input "1", create a User and start the main menu.
            if choice == "1":
                the_user = User(username)
                done_with_program = console_main_menu(the_user)

                # When the user is done, remove all empty days from their data.
                the_user._cleanup_empty_days()

                # Create, read data into, and close the user's file.
                userfile = open(username+extension, "wb+")
                pickle.dump(the_user, userfile)
                userfile.close()


def console_main_menu(a_user) -> bool:
    """Main menu of the console interface. Called by top-level function.

    User may choose to add or view/edit records, calculate averages, quit, or just log out.

    :param a_user: User
    :return: bool
    """
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

        # If choice is 4, return to top-level function, but do not close the program.
        elif choice == 4:
            return False

        # If choice is 5, return to top-level function, and close the program.
        elif choice == 5:
            return True
        else:
            print("Number out of range.")


def console_view_averages(a_user):
    """Displays the averages and ratings of the user's glucose, carbs,
    missed meals, and activity over the last user-entered number of days.

    :param a_user: User
    """

    # If the user has no days, inform them of this fact.
    if a_user.first_day is None:
        print("No records found. Averages unavailable.\n")

    # Otherwise, get number of days back.
    else:
        days_back = int(input("Enter days to go back (0 means today): "))

        # If days back is negative, do nothing. If it's valid, calculate averages.
        if days_back >= 0:
            glucose_average = a_user.calculate_average_glucose(days_back)
            carbs_per_meal_average = a_user.calculate_average_carbs_per_meal(days_back)
            time_active_average = a_user.calculate_average_time_active(days_back)
            average_meals_missed = a_user.calculate_average_meals_missed(days_back)

            # Print labels, averages, and ratings.
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
    """Allows the user to view records one day at a time.
    Calls console_choose_record_to_edit methood if edits are to be made.

    :param a_user: User
    """
    current_day = a_user.last_day   # Start at the user's last day.
    QUIT = 4                        # Sentinel value
    choice = 0                      # Initialize choice variable

    # If there are no days, inform the user.
    if a_user.last_day is None:
        print("No days found.\n")

    # Otherwise, as long as choice isn't the sentinel value, print the day and menu.
    else:
        while choice != QUIT:
            print(current_day)

            print("1. Previous day")
            print("2. Edit a record")
            print("3. Next day")
            print("4. Back")

            choice = int(input("\nEnter number: "))
            while choice < 1 or choice > 4:
                print("Number not in range.")
                choice = int(input("Enter number: "))

            if choice == 1:
                # If there are no prior days, inform the user they can't go back anymore.
                if current_day.previous_day is None:
                    print("Currently at earliest recorded day.")

                # Otherwise, move to previous day.
                else:
                    current_day = current_day.previous_day
            elif choice == 3:
                # If there are no future days, inform the user they can't go forward anymore.
                if current_day.next_day is None:
                    print("Currently at latest recorded day.")

                # Otherwise, move to next day.
                else:
                    current_day = current_day.next_day

            elif choice == 2:
                console_choose_record_to_edit(current_day)
            else:
                return


def console_choose_record_to_edit(a_day):
    """Lets the user choose which record to edit.

    :param a_day: Day
    """
    QUIT = 4    # Sentinel value

    print("1. Morning record")
    print("2. Afternoon record")
    print("3. Evening record")
    print("4. Back")

    choice = int(input("\nEnter number: "))
    while choice < 1 or choice > 4:
        print("Number not in range.")
        choice = int(input("Enter number: "))

    if choice == 1:
        console_edit_record(a_day.morning_record)
    elif choice == 2:
        console_edit_record(a_day.afternoon_record)
    elif choice == 3:
        console_edit_record(a_day.evening_record)
    else:
        return


def console_edit_record(a_record):
    """Allows the user to choose and edit parts of a record.
    Unable to edit the date or time of day.

    :param a_record: Record
    """
    QUIT = 5    # sentinel value
    choice = 0  # initialize choice variable

    # Until the user decides to quit, print the record and menu.
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

            # If the user enetered a meal, also have them enter carbs.
            if meal != "0":
                a_record.carbs = int(input("Enter new carb amount: "))

            # Otherwise, if the user did not enter a meal, set the meal to "" and the carbs to 0.
            else:
                a_record.carbs = 0
                meal = ""
            a_record.meal = meal
        elif choice == 3:
            activity = input("Enter new activity (0 for nothing): ")

            # If the user did not enter an activity, set the activity to "" and the times to None.
            if activity == "0":
                activity = ""
                activity_start_time = None
                activity_end_time = None

            # Otherwise, have the user enter the start and end times.
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
    """Allows the user to add a Record to a day. Calls the console_create_record function to do so.

    :param a_user: User
    """

    good_format = False     # Will not allow the user to continue without a valid date format.
    while not good_format:
        date_string = input("Enter date for record (MM/DD/YYYY, 0 for today: ")

        # If the user entered a date of their own, check it for validity.
        if date_string != "0":
            try:
                date_obj = datetime.datetime.strptime(date_string, '%m/%d/%Y').date()
                good_format = True
            except ValueError:
                print("Accepted inputs are 0 or the format MM/DD/YYYY. Try again.")

        # Otherwise, set the date to today's date.
        else:
            good_format = True
            date_obj = datetime.datetime.today().date()

    current_day = Day(date_of_day=date_obj)     # Create a new Day object.

    # Attempt to insert the day into the user's doubly-linked list of Days.
    if not a_user.insert_day_in_list(current_day):
        # If the date was already there, find the appropriate day instead of inserting a new one.
        current_day = a_user.last_day
        while current_day.date_of_day != date_obj:
            current_day = current_day.previous_day

    # Display menu for adding records.
    print("Add record for:")
    print("1. Morning")
    print("2. Afternoon")
    print("3. Evening")
    print("4. Back")

    choice = int(input("\nEnter number: "))

    while choice < 1 or choice > 4:
        print("Invalid entry.")
        choice = int(input("Enter number:"))

    if choice != 4:
        if choice == 1:
            current_day.morning_record = console_create_record()
        elif choice == 2:
            current_day.afternoon_record = console_create_record()
        else:
            current_day.evening_record = console_create_record()


def console_create_record() -> Record:
    """Allows the user to create a Record.

    :return: Record
    """
    # Get the glucose value.
    glucose = int(input("Enter glucose: "))

    # Get the meal
    meal = input("Enter meal (0 for none): ")

    # If there was a meal, get the carbs
    if meal != "0":
        carbs = int(input("Enter carbs: "))

    # If there wasn't a meal, set meal to "" and carbs to 0
    else:
        meal = ""
        carbs = 0

    # Get the activity
    activity = input("Enter activity (0 for none): ")

    # If there was an activity...
    if activity != "0":
        good_format = False     # Does not allow the user to continue until the time formats are good
        while not good_format:
            try:
                activity_start_time = datetime.datetime.strptime(input("Enter start time (h:m AM/PM): "), "%I:%M %p")
                activity_end_time = datetime.datetime.strptime(input("Enter end time (h:m AM/PM): "), "%I:%M %p")
                good_format = True
            except ValueError:
                print("Invalid time formats. Please enter in hh:mm AM/PM format.")

    # Otherwise, set activity to "" and both times to None
    else:
        activity = ""
        activity_start_time = None
        activity_end_time = None

    # Get the mood
    mood = input("Enter mood: ")

    # Create and return a new Record object
    return Record(glucose=glucose, meal=meal, carbs=carbs, activity=activity,
                  activity_start_time=activity_start_time,
                  activity_end_time=activity_end_time, mood=mood)
