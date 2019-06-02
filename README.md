# DiabetesHealthTracker
Diabetes Health and Activity Tracker (School project)

This is meant to be a glucose, carbs, activity, and mood log for diabetic persons. One in particular, but others if it's helpful, I guess.
The unique feature added is the ability to average values over the last arbitrary number of days.

GUI Instructions:

Open the project and run main_interface.py

The GUI will now open. It's functional, but not pretty.

Enter your name into the entry box, and click the "Log In" button.

If you did not already have a file, you will see that the window changed to explain this. It will ask if you want to create a file.
Click "Yes" if you would like to do so and continue, or "No" to go back to the Log In screen.

If you did have a file, or you clicked "Yes" on the Create Account screen, you will enter the main screen.

Click the "New Entry" button. The "New Entry" window will pop up. Click the "Today" button to put today's date in the Date box.

If you want to put in a different date, make sure you do it with the format MM/DD/YYYY. If you don't, you can't confirm the entry.

Put in an integer for Glucose.

Pick a time of day. You will not be able to confirm the entry if you don't. You may now either Confirm or continue entering information.

If you enter a Meal, you must enter the Carbs. You will not be able to confirm the entry otherwise.

If you enter an Activity, you must enter both a Start Time and and End Time. Follow the HH:MM AM/PM format example shown to the right of the Start Time box.

Enter your mood.

If you did not earlier, click Confirm. Unless there is an error in the data, the New Entry window will close.

Create a few more entries. Click the box on the main screen and input a positive integer. Click the "Compute Averages" button.

The "__ day average" window will pop up, where __ is the number entered. Look at the stats, then close the "__ day average" menu.

Click the View/Edit Records button. By default, you will see the latest record chronologically.
If any of this information is incorrect, change it, and then click the "Save Changes" button.
Be careful with this, as it will overwrite any record that already takes up that Date and Time of day, and delete the incorrect record at the position you were just at.
Click the "Previous" button to move to the previous existing record (chronologically speaking). If there is no prior record, the button will do nothing.
Click the "Next" button to move to the next existing record (chronologically speaking). If there is no next record, the button will do nothing.

When you are done viewing/editing records, either close the "View/Edit Records" window or click Cancel. Either one will close the window.

Take note of the Remove Empty Days button. This button will remove from the user's data all Days that have no Records.
By default, this happens when files are opened or closed. This button is here in case it needs to be done during runtime.
I do not recommend using this button unless the Display Averages page isn't working as expected after moving all Records from the latest dates to earlier dates.

If you are done, and someone else wishes to use the tracker, click "Log Out" to save your changes and be taken to the Log In screen.

If you are done, and nobody else wishes to use the tracker at this time, you may close the window. Your changes will be saved automatically, and the program will close.

CLI Instructions:

Open the project, specifically, main_interface.py

Uncomment line 11, then comment lines 12 through 15. Now run the project.

This will start up a CLI for the project.

The first thing it will ask you is for your name. Provide this.

Unless your name is "test", it will then say that it could not find your user file, and ask if you would like to create one. Enter '1' without the single-quotes to enable this. If you enter anything else, it will simply ask for another name.

You are now at the main menu. Enter 2. Note how it says there are no records yet.

Now enter 3. There are still no records, so no averages can be provided.

Enter 4 if you want to change your user. This will, effectively, restart the program. Enter 5 if you want to just quit.
If you accidentally enter 4 and still want to quit, just type QUIT at the "Enter name" prompt.

Enter 1. You will be prompted to enter a date. Enter 0 to default to today. Otherwise, enter a date in MM/DD/YYYY format.

You will now be asked to enter 1, 2, or 3 for Morning, Evening, and Night records, respectively. Select one of these.

You will be asked for your glucose level. Enter this number.

You will be asked for your meal. Enter '0' without the single quotes to skip this and the next question. Otherwise, enter your meal.

If you did not skip the meal, you will be asked for the meal's carbs. Enter this number.

You will be asked for your activity. Enter '0' without the single quotes to skip this and the next two questions. Otherwise, enter your activity.

If you did not skip the activity, you will be asked for its start time. Enter this in HH:MM AM/PM format. Example: 2:30 PM

If you did not skip the activity, you will be asked for its end time. Enter this in HH:MM AM/PM format. Example: 3:19 PM

The program does not currently validate that the end time comes after the start time. Be careful with your inputs.

You will be asked to enter your mood. Think about your day and how you feel. Enter that.

Congratulations, you have entered one record for one day.

Enter 2. Note that it now shows you a day and three records. Two of them should say "None".

Enter 1. Note that you are told you are at the earliest day.

Enter 3. Note that you are told you are at the latest day.

Enter 2. You will now be prompted for which record you would like to edit. This has not been set up to validate your choice yet, so be careful.

Choose the record you made. Choose one of the things to edit, or choose to go back.

Keep going back until you get to the main menu.

Add a few more records. Be careful not to overwrite any you've already created.

Return to the main menu and select 3. Enter a number of days. This will determine your average values and ratings for the past however many days, plus today.

Enter 2 from the main menu. Check out the records you've entered. Try moving backwards and forwards through the days (assuming your records span more than one day).

When you are done, enter 5 on the main menu. Your file is now saved, and the program will exit.

This is very much a work in progress.
