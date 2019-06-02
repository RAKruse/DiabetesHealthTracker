import tkinter as tk
import os.path
import pickle
import datetime
from user import User
from record import Record
from day import Day


# Global variables to hold the user's name, the User object, and the extension.
_username = ""          # Used for labels and logging in/out. Used by several classes/windows.
the_user = None         # Holds the User object. Used by several classes/windows.
extension = ".dbhat"    # Holds the file extension for the saved binary files. Used by several classes/windows.


class GuiInterface(tk.Tk):
    """Gui Interface: Creates three Frames in one window.
    First frame is to log in.
    Second frame is to create an account.
    Third frame is the main interface frame.
    """

    # This class was primarily taken from the examples shown at
    # https://pythonprogramming.net/change-show-new-frame-tkinter/
    # I do not deserve credit for figuring this part out.

    def __init__(self):
        tk.Tk.__init__(self, className="\nDiabetes Health & Activity Tracker")

        # Create a container frame
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create a dictionary of frames
        self.frames = {}

        # For F in the LoginPage, CreatePage, and MainPage classes:
        for F in (LoginPage, CreatePage, MainPage):

            # Create a frame of the appropriate kind
            frame = F(container, self)

            # Add this frame to the dictionary
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        # Show the login frame
        self.show_frame(LoginPage)

    def show_frame(self, cont):
        """Shows the frame associated with cont.

        :param cont: a Frame, I think.
        """
        frame = self.frames[cont]
        frame.tkraise()

    def on_close(self):
        """Ensures that the user's file is saved and closed before the application closes."""
        global the_user
        global _username
        global extension

        # If the_user exists, remove all empty days, open their file, write to the file, and close the file.
        if the_user is not None:
            the_user._cleanup_empty_days()
            userfile = open(_username.replace(" ", "") + extension, "wb+")
            pickle.dump(the_user, userfile)
            userfile.close()

        # Close the GUI.
        self.destroy()

    def update(self):
        """Updates the Main and Create pages every 0.1 seconds."""
        self.frames[MainPage].update()
        self.frames[CreatePage].update()
        self.after(100, self.update)


class LoginPage(tk.Frame):
    """This frame exists for the user to log in.
    """

    # This class was primarily taken from the examples shown at
    # https://pythonprogramming.net/change-show-new-frame-tkinter/
    # I do not deserve credit for figuring the basic part out.
    # I did add everything else myself.

    def __init__(self, parent, controller):
        """
        :param parent: The controller frame from a GuiInterface object.
        :param controller: The GuiInterface object itself.
        """
        tk.Frame.__init__(self, parent)

        # Add user entry label and associated entry box.
        login_label = tk.Label(self, text="Enter username: ")
        login_label.grid(row=0, column=0)
        login_entry = tk.Entry(self)
        login_entry.grid(row=0, column=1)

        # Add login button
        login_button = tk.Button(self, text="Log In", command=lambda: self.check_login(login_entry.get(), controller))
        login_button.grid(row=0, column=2)

    def check_login(self, username, controller):
        """Checks to see if the user's file already exists. Opens appropriate frame based on this.

        :param username: string
        :param controller: a GuiInterface object.
        """

        global the_user
        global _username
        global extension

        # Set the global _username variable to the entered username
        _username = username

        # If there is already a file for that user...
        if os.path.isfile(_username.replace(" ", "") + extension):
            # ... Open the file, read data from it into the_user, and close the file.
            userfile = open(_username.replace(" ", "") + extension, "rb")
            the_user = pickle.load(userfile)
            userfile.close()

            # Remove empty days from the user's data.
            the_user._update_days()

            # Show the Main frame on the window.
            controller.show_frame(MainPage)

        # Otherwise, show the Create File frame on the window.
        else:
            controller.show_frame(CreatePage)


class CreatePage(tk.Frame):
    """This frame exists for a user to either create a file or go back and fix a typo in their name.
    """

    # This class was primarily taken from the examples shown at
    # https://pythonprogramming.net/change-show-new-frame-tkinter/
    # I do not deserve credit for figuring the basic idea out.
    # I did add all additional things myself.

    global _username

    def __init__(self, parent, controller):
        """
        :param parent: The controller frame from a GuiInterface object.
        :param controller: The GuiInterface object itself.
        """
        tk.Frame.__init__(self, parent)

        # Add label to explain lack of file.
        self.create_account_label = tk.Label(self, text="File for " + _username + " not found! Create an account?")
        self.create_account_label.grid(row=0)

        # Add "Yes" and "No" buttons.

        # If user picks "No", head back to the Login frame.
        no_button = tk.Button(self, text="No", command=lambda: controller.show_frame(LoginPage))
        no_button.grid(row=1, column=0)

        # If user picks "Yes", call self.create_file to make a new User and head to the Main Page frame.
        yes_button = tk.Button(self, text="Yes", command=lambda: self.create_file(controller))
        yes_button.grid(row=1, column=2)

    def create_file(self, controller):
        global the_user

        # Create a user, and head to the Main Page frame.
        the_user = User(_username.replace(" ", ""))
        controller.show_frame(MainPage)

    def update(self):
        # Update label with _username's value. Happens every .1 seconds.
        self.create_account_label['text'] = "File for " + _username + " not found! Create an account?"


class MainPage(tk.Frame):
    """The Main Interface Frame for the GUI. Handles everything but logging in and creating accounts."""

    # The basic skeleton for this class was primarily taken from the examples shown at
    # https://pythonprogramming.net/change-show-new-frame-tkinter/
    # I do not deserve credit for figuring that part out.
    # I did do all the rest of the code.

    def __init__(self, parent, controller):
        """
        :param parent: The controller frame from a GuiInterface object.
        :param controller: The GuiInterface object itself.
        """
        global _username
        tk.Frame.__init__(self, parent)

        # Create and place Welcome label (instance variable in order to be updated with user's name)
        self.welcome_label = tk.Label(self, text="Welcome, " + _username + "!")
        self.welcome_label.grid(row=0, column=0, pady=5)

        # Create and place Logout button
        logout_button = tk.Button(self, text="Log Out", command=lambda: self.log_out(controller))
        logout_button.grid(row=0, column=2, sticky="ew")

        # Create and place New Entry button
        new_entry_button = tk.Button(self, text="New Entry", command=lambda: self.new_entry())
        new_entry_button.grid(row=1, column=0, sticky="ew", pady=5)

        # Create and place View/Edit Records button
        view_button = tk.Button(self, text="View/Edit Records", command=lambda: self.view_records())
        view_button.grid(row=1, column=3, sticky="ew")

        # Create and place View Averages button and associated labels and entry box
        averages_button = tk.Button(self, text="Compute Averages", command=lambda: self.get_averages())
        averages_button.grid(row=3, column=0, sticky="ew", pady=5)
        tk.Label(self, text=" over last ").grid(row=3, column=1, sticky="nsew")
        self.averages_entry_box = tk.Entry(self, justify='center')
        self.averages_entry_box.grid(row=3, column=2)
        self.averages_entry_box.insert(0, "0")
        tk.Label(self, text=" days").grid(row=3, column=3, sticky="w")

        # Create and place Remove Empty Days button
        remove_empty_days = tk.Button(self, text="Remove Empty Days", command=lambda: self.cleanup_empty_days())
        remove_empty_days.grid(row=4, column=3, sticky="ew")

        # Set instance variables for current day and current record to None
        self.current_day = None
        self.current_record = None

    def cleanup_empty_days(self):
        """Removes Days with no Records from the user's list of Days."""
        global the_user
        the_user._cleanup_empty_days()

    def log_out(self, controller):
        """Logs the user out. Returns to the Login frame."""
        global the_user
        global _username

        # Open user's file and write to it.
        userfile = open(_username.replace(" ", "") + extension, "wb+")
        the_user._cleanup_empty_days()
        pickle.dump(the_user, userfile)
        userfile.close()

        # Reset values for current day, username, user, and current record.
        self.current_day = None
        self.current_record = None
        _username = ""
        the_user = None

        # Return to Login frame.
        controller.show_frame(LoginPage)

    def new_entry(self):
        """Opens a new window to enter to enter a new Record."""
        n_entry = self._new_and_view_base("New Entry")

        # Add button to set date entry box to today's date
        today_button = tk.Button(n_entry, text="Today", command=lambda: self._today_in_box(n_entry))
        today_button.grid(row=0, column=3, sticky="ew")

        # Add button to cancel entry (works the same as closing the window)
        cancel_button = tk.Button(n_entry, text="Cancel", command=lambda: n_entry.destroy())
        cancel_button.grid(row=9, column=2, sticky="nsew")

        # Add a button to confirm submission of the entry. Closes the window if submission was successful.
        confirm_button = tk.Button(n_entry, text="Confirm & Close", command=lambda:
                                   self.add_record(n_entry.time_variable.get(), n_entry))
        confirm_button.grid(row=9, column=1, sticky="nsew", columnspan=2)

    def _today_in_box(self, new_entry_window):
        """Places today's date in the new_entry_window's date_entry_box.

        :param new_entry_window: tkinter.Toplevel
        """
        new_entry_window.date_entry_box.delete(0, len(new_entry_window.date_entry_box.get()))
        new_entry_window.date_entry_box.insert(0, datetime.datetime.today().date().strftime("%m/%d/%Y"))

    def _create_record(self, record_window) -> Record:
        """Strips the data from a _new_and_view_base window and creates a Record.

        :param record_window: tkinter.Toplevel (specifically a _new_and_view_base window)
        :return: Record
        """

        # Get glucose data from glucose entry box
        glucose = int(record_window.glucose_entry_box.get())

        # If meal was empty, set carbs to 0
        if record_window.meal_entry_box.get() == "":
            carbs = 0

        # Otherwise, get carbs from carbs entry box
        else:
            carbs = int(record_window.carbs_entry_box.get())

        # If activity was not empty, get activity start and end time from respective entry boxes
        if record_window.activity_entry_box.get() != "":
            activity_start = datetime.datetime.strptime(record_window.activity_start_entry_box.get(), "%I:%M %p")
            activity_end = datetime.datetime.strptime(record_window.activity_end_entry_box.get(), "%I:%M %p")

        # Otherwise, set activity start and end times to None
        else:
            activity_start = None
            activity_end = None

        # Create new record
        new_record = Record(glucose, record_window.meal_entry_box.get(), carbs,
                            record_window.activity_entry_box.get(), activity_start, activity_end,
                            record_window.mood_entry_box.get())
        return new_record

    def add_record(self, time, new_entry_window, close_on_add=True):
        """Strips date and Record from new_entry_window. Inserts Record into appropriate spot in the_user's
        doubly-linked list of Days. (adds spot if not found)

        :param time: int (represents Morning (1), Afternoon (2), Evening (3)
        :param new_entry_window: tkinter.Toplevel (specifically a _new_or_view_base window)
        :param close_on_add: bool (defaults to True)
        :return:
        """

        # Strip date from window
        date = datetime.datetime.strptime(new_entry_window.date_entry_box.get(), "%m/%d/%Y").date()

        # Strip Record from window
        record_to_add = self._create_record(new_entry_window)

        # Creates a Day object with the appropriate date
        current_day = Day(date_of_day=date)

        # Inserts day in list (unless it is already there)
        if not the_user.insert_day_in_list(current_day):
            # Navigates to appropriate day in the list
            current_day = the_user.last_day
            while current_day.date_of_day != date:
                current_day = current_day.previous_day

        # Inserts record in appropriate spot of Day
        if time == 1:
            current_day.morning_record = record_to_add
        elif time == 2:
            current_day.afternoon_record = record_to_add
        elif time == 3:
            current_day.evening_record = record_to_add
        else:
            raise ValueError("Time of day not set.")

        # Closes window upon successfully adding record if close_on_add is true
        if close_on_add:
            new_entry_window.grab_release()
            new_entry_window.destroy()

    def view_records(self):
        """Creates window that allows the user to view and edit existing records."""
        global the_user

        # Set current day and current record values to the last non-empty ones found
        self.current_day = None
        self.current_record, time_of_day = self._get_last_record()  # Also set time_of_day to the appropriate value
                                                                    # 1) Morning, 2) Afternoon, 3) Evening

        # Create base window
        view_window = self._new_and_view_base("View/Edit Records")

        # Add cancel button to viewing window
        cancel_button = tk.Button(view_window, text="Cancel", command=lambda: view_window.destroy())
        cancel_button.grid(row=9, column=3)

        # Add button to navigate to previous record
        view_window.show_previous_button = tk.Button(view_window, text="Previous",
                                                     command=lambda: self.show_previous(view_window))
        view_window.show_previous_button.grid(row=9, column=0)

        # Add button to navigate to next record
        view_window.show_next_button = tk.Button(view_window, text="Next",
                                                 command=lambda: self.show_next(view_window))
        view_window.show_next_button.grid(row=9, column=2)

        # Add button to save changes to current record
        view_window.edit_record_button = tk.Button(view_window, text="Save Changes",
                                                   command=lambda: self.edit_record(view_window))
        view_window.edit_record_button.grid(row=9, column=1)

        # By default, display most recent record
        self.display_record(view_window, time_of_day)

    def display_record(self, record_window, time_of_day):
        """Displays the data in a record, alongside its associated date.

        :param record_window: tkinter.Toplevel (specifically, a _new_and_view_base window)
        :param time_of_day: int (1 for Morning, 2 for Afternoon, 3 for Evening)
        :return:
        """

        # If either the current record or current day are None, don't display anything.
        if self.current_record is None or self.current_day is None:
            pass
        else:
            # Display date.
            record_window.date_entry_box.delete(0, len(record_window.date_entry_box.get()))
            record_window.date_entry_box.insert(0, self.current_day.date_of_day.strftime("%m/%d/%Y"))

            # Display glucose.
            record_window.glucose_entry_box.delete(0, len(record_window.glucose_entry_box.get()))
            record_window.glucose_entry_box.insert(0, str(self.current_record.glucose))

            # Display meal.
            record_window.meal_entry_box.delete(0, len(record_window.meal_entry_box.get()))
            record_window.meal_entry_box.insert(0, self.current_record.meal)

            # Set time of day.
            record_window.time_variable.set(time_of_day)

            # Display carbs for the meal.
            record_window.carbs_entry_box.delete(0, len(record_window.carbs_entry_box.get()))
            record_window.carbs_entry_box.insert(0, str(self.current_record.carbs))

            # Clear activity, activity_start, and activity_end entry boxes.
            record_window.activity_entry_box.delete(0, len(record_window.activity_entry_box.get()))
            record_window.activity_start_entry_box.delete(0, len(record_window.activity_start_entry_box.get()))
            record_window.activity_end_entry_box.delete(0, len(record_window.activity_end_entry_box.get()))

            if self.current_record.activity != "":
                # Display activity type, activity start time, and activity end times.
                record_window.activity_entry_box.insert(0, self.current_record.activity)
                record_window.activity_start_entry_box.insert(0,
                                                        self.current_record.activity_start_time.strftime("%I:%M %p"))
                record_window.activity_end_entry_box.insert(0,
                                                            self.current_record.activity_end_time.strftime("%I:%M %p"))

            # Display mood.
            record_window.mood_entry_box.delete(0, len(record_window.mood_entry_box.get()))
            record_window.mood_entry_box.insert(0, self.current_record.mood)

    def show_next(self, record_window):
        """Finds and shows the next existing record from the currently viewed one.
        Does nothing if at the most recent record.

        :param record_window: tkinter.Toplevel (specifically a view_records window)
        """
        current_day = self.current_day  # set temporary current_day variable to current_day instance variable
        current_record = None   # set temporary current_record variable to None

        position = record_window.time_variable.get()    # Determine which time we are at (morning, afternoon, evening)

        # While there are still days to check AND we haven't found the next record yet:
        while current_day is not None and current_record is None:
            # If we're the morning record, set ourself to afternoon record.
            if position == 1:
                current_record = current_day.afternoon_record
                position = 2

            # If we're the afternoon record, set ourself to evening record.
            elif position == 2:
                current_record = current_day.evening_record
                position = 3

            # If we're the evening record, go to next day...
            elif position == 3:
                current_day = current_day.next_day
                # ...Check if that day exists, and if so, set ourself to that day's morning record.
                if current_day is not None:
                    position = 1
                    current_record = current_day.morning_record
                else:
                    position = 0

        # If we found a record:
        if current_record is not None:
            self.current_day = current_day  # Set current_day instance variable to local current_day's value
            self.current_record = current_record    # Set current_record instance variable to
                                                    # local current_record's value
            self.display_record(record_window, position)    # Display found record

    def show_previous(self, record_window):
        """Finds and shows the previous existing record from the currently viewed one.
        Does nothing if at the most recent record.

        :param record_window: tkinter.Toplevel (specifically a view_records window)
        """

        current_day = self.current_day  # set temporary current_day variable to current_day instance variable
        current_record = None   # set temporary current_record variable to None

        position = record_window.time_variable.get()    # Determine which time we are at (morning, afternoon, evening)

        # While there are still days to check AND we haven't found the previous record yet:
        while current_day is not None and current_record is None:
            # If we're the evening record, set ourself to afternoon record.
            if position == 3:
                current_record = current_day.afternoon_record
                position = 2

            # If we're the afternoon record, set outself to morning record.
            elif position == 2:
                current_record = current_day.morning_record
                position = 1

            # If we're the morning record, go to the previous day...
            elif position == 1:
                current_day = current_day.previous_day
                # ...Check if that day exists, and if so, set ourself to that day's evening record.
                if current_day is not None:
                    position = 3
                    current_record = current_day.evening_record
                else:
                    position = 0

        # If we found a record:
        if current_record is not None:
            self.current_day = current_day  # Set current_day instance variable to local current_day's value
            self.current_record = current_record    # Set current_record instance variable to
                                                    # local current_record's value
            self.display_record(record_window, position)    # Display found record

    def edit_record(self, view_window):
        """Edits the currently viewed record.

        :param view_window: tkinter.Toplevel (specifically, a view_records window)
        """

        edited_record = self._create_record(view_window)     # Create a copy of the edited record

        old_time_of_day = 0     # Create a variable to hold unedited time of day

        # Set old_time_of_day to the appropriate value
        if self.current_day.morning_record is self.current_record:
            old_time_of_day = 1
        elif self.current_day.afternoon_record is self.current_record:
            old_time_of_day = 2
        elif self.current_day.evening_record is self.current_record:
            old_time_of_day = 3
        else:
            raise ValueError("Invalid time of day, somehow.")

        # If the date was changed, or the time of day was changed,
        # delete the unedited record, and add the edited one.
        if view_window.date_entry_box.get() != self.current_day.date_of_day.strftime("%m/%d/%Y") or \
            edited_record == self.current_record:
            if old_time_of_day == 1:
                self.current_day.morning_record = None
            elif old_time_of_day == 2:
                self.current_day.afternoon_record = None
            elif old_time_of_day == 3:
                self.current_day.evening_record = None
            self.add_record(view_window.time_variable.get(), view_window, close_on_add=False)

        # Otherwise, add the edited record. It will overwrite and replace the unedited one.
        else:
            self.add_record(old_time_of_day, view_window, close_on_add=False)

    def _get_last_record(self) -> (Record, int):
        """Returns the last record found in the_user's doubly-linked list of Days.
        Also returns what time of day (1 for morning, 2 for afternoon, 3 for evening) the record was found at.

        :return: Record, int (representing Record's position in the day)
        """
        # Set current day instance variable to user's last day.
        self.current_day = the_user.last_day
        current_record = None   # set local current_record variable to None
        time_of_day = 0     # Create time_of_day variable (1 for morning, 2 for afternoon, 3 for evening)

        # While there are still days to go back, and a record hasn't been found...
        while self.current_day is not None and current_record is None:
            # If the evening record exists, set current_record to evening record, and time_of_day to 3.
            if self.current_day.evening_record is not None:
                current_record = self.current_day.evening_record
                time_of_day = 3
            # Else if the afternoon record exists, set current_record to afternoon record, and time_of_day to 2.
            elif self.current_day.afternoon_record is not None:
                current_record = self.current_day.afternoon_record
                time_of_day = 2
            # Else if the morning record exists, set current_record to morning record, and time_of_day to 1.
            elif self.current_day.morning_record is not None:
                current_record = self.current_day.morning_record
                time_of_day = 1
            # Otherwise, set current_day instance variable to its previous day.
            else:
                self.current_day = self.current_day.previous_day

        # Return the current record and its associated time of day.
        return current_record, time_of_day

    def get_averages(self):
        """Opens a window to display the averages of glucose, carbs per meal, activity time, and meals missed
        over the past user-specified number of days."""
        global the_user

        # Get total days to go back
        total_days_back = int(self.averages_entry_box.get())

        # Create window
        avg_scores = tk.Toplevel(self)
        avg_scores.grab_set()
        avg_scores.wm_title(str(total_days_back) + " day average")

        # Create labels for Glucose and associated Rating
        tk.Label(avg_scores, text="Averages over last " + str(total_days_back)
                                  + " days:").grid(row=0, column=0, columnspan=2,pady=5)
        tk.Label(avg_scores, text="Glucose:").grid(row=1, column=0)
        average_glucose = the_user.calculate_average_glucose(total_days_back)
        tk.Label(avg_scores, text=str(average_glucose)).grid(row=1, column=1)
        tk.Label(avg_scores, text=the_user.get_glucose_rating(average_glucose)).grid(row=1, column=4)

        # Create labels for Activity and associated Rating
        tk.Label(avg_scores, text="Activity:").grid(row=2, column=0)
        tk.Label(avg_scores, text="min.").grid(row=2, column=2, sticky="w")
        average_activity = the_user.calculate_average_time_active(total_days_back)
        tk.Label(avg_scores, text=str(average_activity)).grid(row=2, column=1)
        tk.Label(avg_scores, text=the_user.get_time_active_rating(average_activity)).grid(row=2, column=4)

        # Create labels for Carbs per meal and associated Rating
        tk.Label(avg_scores, text="Carbs/meal:").grid(row=3, column=0)
        average_carbs = the_user.calculate_average_carbs_per_meal(total_days_back)
        tk.Label(avg_scores, text=str(average_carbs)).grid(row=3, column=1)
        tk.Label(avg_scores, text=the_user.get_carbs_per_meal_rating(total_days_back)).grid(row=3, column=4)

        # Create labels for Meals missed and associated Rating
        tk.Label(avg_scores, text="Meals missed:").grid(row=4, column=0)
        average_missed = the_user.calculate_average_meals_missed(total_days_back)
        tk.Label(avg_scores, text=str(average_missed)).grid(row=4, column=1)
        tk.Label(avg_scores, text=the_user.get_meals_missed_rating(average_missed)).grid(row=4, column=4)

        # Insert "Rating:" in column 3 of rows 1 through 4
        # As this is the only thing completely identical across those columns, it is fine to
        # place it in a loop.
        for i in range(1, 5):
            tk.Label(avg_scores, text="Rating:").grid(row=i, column=3, padx=(10, 0), pady=5)

    def update(self):
        """Updates the Welcome label with the user's name."""
        global _username
        self.welcome_label['text'] = "Welcome, " + _username + "!"

    def _new_and_view_base(self, wm_name):
        """Returns the base of the new_entry and view_record windows, with the wm_title set to wm_name.

        :param wm_name: string
        :return: tkinter.Toplevel
        """

        universal_pady = 2

        # Create tkinter.Toplevel window
        n_entry = tk.Toplevel(self)
        n_entry.grab_set()
        n_entry.wm_title(wm_name)

        # Add date label and associated entry box
        tk.Label(n_entry, text="Date:").grid(row=0, column=0)
        n_entry.date_entry_box = tk.Entry(n_entry)
        n_entry.date_entry_box.grid(row=0, column=1, pady=universal_pady)
        tk.Label(n_entry, text="EX: 03/22/2019").grid(row=0, column=2, sticky="w")  # Add example format label

        # Add glucose label and associated entry box
        tk.Label(n_entry, text="Glucose:").grid(row=1, column=0)
        n_entry.glucose_entry_box = tk.Entry(n_entry)
        n_entry.glucose_entry_box.grid(row=1, column=1, pady=universal_pady)

        # Add meal label and associated entry box
        tk.Label(n_entry, text="Meal:").grid(row=2, column=0)
        n_entry.meal_entry_box = tk.Entry(n_entry)
        n_entry.meal_entry_box.grid(row=2, column=1, columnspan=2, sticky="nsew", pady=universal_pady)

        # Add Carbs label and associated entry box
        tk.Label(n_entry, text="Carbs:").grid(row=3, column=1)
        n_entry.carbs_entry_box = tk.Entry(n_entry)
        n_entry.carbs_entry_box.grid(row=3, column=2, pady=universal_pady)

        # Add Time of day label, associated radio buttons, and associated tk.IntVar
        n_entry.time_variable = tk.IntVar()
        tk.Label(n_entry, text="Time of day:").grid(row=4, column=0, pady=universal_pady)
        tk.Radiobutton(n_entry, text="Morning", variable=n_entry.time_variable, value=1).grid(row=4, column=1)
        tk.Radiobutton(n_entry, text="Afternoon", variable=n_entry.time_variable, value=2).grid(row=4, column=2)
        tk.Radiobutton(n_entry, text="Evening", variable=n_entry.time_variable, value=3).grid(row=4, column=3)

        # Add Activity label and associated entry box
        tk.Label(n_entry, text="Activity:").grid(row=5, column=0)
        n_entry.activity_entry_box = tk.Entry(n_entry)
        n_entry.activity_entry_box.grid(row=5, column=1, pady=universal_pady)

        # Add activity Start time label and associated entry box
        tk.Label(n_entry, text="Start time:").grid(row=6, column=1)
        n_entry.activity_start_entry_box = tk.Entry(n_entry)
        n_entry.activity_start_entry_box.grid(row=6, column=2, pady=universal_pady)
        tk.Label(n_entry, text="EX: 12:43 PM").grid(row=6, column=3)    # Add example format label

        # Add activity End time label and associated entry box
        tk.Label(n_entry, text="End time:").grid(row=7, column=1)
        n_entry.activity_end_entry_box = tk.Entry(n_entry)
        n_entry.activity_end_entry_box.grid(row=7, column=2, pady=universal_pady)

        # Add Mood label and associated entry box
        tk.Label(n_entry, text="Mood:").grid(row=8, column=0)
        n_entry.mood_entry_box = tk.Entry(n_entry)
        n_entry.mood_entry_box.grid(row=8, column=1, pady=universal_pady)

        # Return created Toplevel object to use as a template
        return n_entry
