from datetime import datetime
from datetime import timedelta


class Record:
    """Records:
    glucose
    meal the record goes with
    carbs for that meal
    activity description, start and end times
    mood"""

    def __init__(self, glucose=0, meal="", carbs=0,
                 activity="", activity_start_time=None,
                 activity_end_time=None, mood=""):
        """
        Returns a Record object.

        :param glucose: int
        :param meal: string
        :param carbs: int
        :param activity: string
        :param activity_start_time: time
        :param activity_end_time: time
        :param mood: string
        """

        if glucose < 0:
            raise ValueError("Glucose must be nonnegative.")
        self._glucose = glucose
        self._meal = meal
        if carbs < 0:
            raise ValueError("Carbs must be nonnegative.")
        self._carbs = carbs
        self._activity = activity
        self._activity_start_time = activity_start_time
        self._activity_end_time = activity_end_time
        self._mood = mood

    @property
    def glucose(self) -> int:
        """Returns int representing glucose."""
        return self._glucose

    @glucose.setter
    def glucose(self, value):
        """Sets glucose. Value may not be below 0.

        :param value: int
        """
        if value < 0:
            raise ValueError("Glucose may not be below 0.")
        self._glucose = value

    @property
    def meal(self) -> str:
        """Returns string representing meal."""
        return self._meal

    @meal.setter
    def meal(self, value):
        """Sets the meal.

        :param value: string
        """
        self._meal = value

    @property
    def carbs(self) -> int:
        """Returns int representing carbs."""
        return self._carbs

    @carbs.setter
    def carbs(self, value):
        """Sets carbs. Value may not be below 0.

        :param value: int
        """
        if value < 0:
            raise ValueError("Carbs may not be be below 0.")
        self._carbs = value

    @property
    def activity(self) -> str:
        """Returns a string representing type of activity."""
        return self._activity

    @activity.setter
    def activity(self, value):
        """Sets activity type.

        :param value: string"""
        self._activity = value

    @property
    def activity_start_time(self) -> datetime.time:
        """Returns the starting time of the activity as
        a datetime.time object."""
        return self._activity_start_time

    @activity_start_time.setter
    def activity_start_time(self, value):
        """Sets the activity start time.

        :param value: datetime.time"""
        self._activity_start_time = value

    @property
    def activity_end_time(self) -> datetime.time:
        """Returns the ending time of the activity as
        a datetime.time object."""
        return self._activity_end_time

    @activity_end_time.setter
    def activity_end_time(self, value):
        """Sets the activity end time.

        :param value: datetime.time"""
        self._activity_end_time = value

    @property
    def mood(self) -> str:
        """Returns a string representing the mood."""
        return self._mood

    @mood.setter
    def mood(self, value):
        """Sets the mood.

        :param value: string"""
        self._mood = value

    def was_meal_eaten(self) -> bool:
        """Returns true if a meal was set.

        :return: bool"""
        return self._meal != ""

    def get_time_active(self) -> int:
        """Returns time active in minutes, as an int.

        :return: int"""
        time_active_in_minutes = 0

        # If there is no activity, or either of the activity times are None, do nothing and return 0.
        if self._activity == "" or \
                self.activity_start_time is None or \
                self.activity_end_time is None:
            pass
        # Otherwise, determine time active as (end time - start time) / number of minutes.
        else:
            time_active = self._activity_end_time - self._activity_start_time
            time_active_in_minutes = time_active / timedelta(minutes=1)

        return time_active_in_minutes

    def __eq__(self, other):
        """Returns true if two Record objects have the same values.
        Returns false if other is not a Record."""
        equal_to_other = False
        if isinstance(other, self.__class__):
            equal_to_other = (self.__dict__ == other.__dict__)
        return equal_to_other

    def __ne__(self, other):
        """Returns true if two Record objects do not have the same values,
        or if other is not a Record."""
        return not self.__eq__(other)

    def __str__(self):
        """Returns a string representation of the Record."""

        # Add glucose, meal, carbs, and activity labels & values
        val = "Glucose: " + str(self.glucose) + \
              "\nMeal: " + str(self.meal) + \
              "\nCarbs: " + str(self.carbs) + \
              "\nActivity: " + self.activity

        # Determine activity Start and End time values, then output respective labels and values.
        if self.activity_start_time is None or self.activity_end_time is None:  # If either time is blank, no activity.
            val += "\nActivity start time: N/A" + "\nActivity end time: N/A"
        else:
            # Otherwise, list appropriate start and end times.
            val += "\nActivity start time: " + self.activity_start_time.strftime("%I:%M %p") + \
                "\nActivity end time: " + self.activity_end_time.strftime("%I:%M %p")

        # Add a newline at the end.
        val += "\n"
        return val
