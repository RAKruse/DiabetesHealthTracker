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
        self._glucose = glucose
        self._meal = meal
        self._carbs = carbs
        self._activity = activity
        self._activity_start_time = activity_start_time
        self._activity_end_time = activity_end_time
        self._mood = mood

    # TODO: Docstrings.

    @property
    def glucose(self):
        return self._glucose

    @glucose.setter
    def glucose(self, value):
        if value < 0:
            raise ValueError("Glucose may not be below 0.")
        self._glucose = value

    @property
    def meal(self):
        return self._meal

    @meal.setter
    def meal(self, value):
        self._meal = value

    @property
    def carbs(self):
        return self._carbs

    @carbs.setter
    def carbs(self, value):
        if value < 0:
            raise ValueError("Carbs may not be be below 0.")
        self._carbs = value

    @property
    def activity(self):
        return self._activity

    @activity.setter
    def activity(self, value):
        self._activity = value

    @property
    def activity_start_time(self):
        return self._activity_start_time

    @activity_start_time.setter
    def activity_start_time(self, value):
        self._activity_start_time = value

    @property
    def activity_end_time(self):
        return self._activity_end_time

    @activity_end_time.setter
    def activity_end_time(self, value):
        self._activity_end_time = value

    @property
    def mood(self):
        return self._mood

    @mood.setter
    def mood(self, value):
        self._mood = value

    def was_meal_eaten(self) -> bool:
        """Returns true if a meal was set."""
        return self._meal != ""

    def get_time_active(self) -> int:
        """Returns time active in minutes."""
        if self._activity == "" or \
                self.activity_start_time is None or \
                self.activity_end_time is None:
            return 0
        else:
            time_active = self._activity_end_time - self._activity_start_time
            time_active_in_minutes = time_active / timedelta(minutes=1)
            return time_active_in_minutes

    def __str__(self):
        val = "Glucose: " + str(self.glucose) + "\nMeal: " + str(self.meal) + "\nCarbs: " + str(self.carbs) + \
                                "\nActivity: " + self.activity
        if self.activity_start_time is None:
            val += "\nActivity start time: N/A" + "\nActivity end time: N/A"
        else:
            val += "\nActivity start time: " + self.activity_start_time.strftime("%I:%M %p") + \
                "\nActivity end time: " + self.activity_end_time.strftime("%I:%M %p")

        val += "\n"
        return val
