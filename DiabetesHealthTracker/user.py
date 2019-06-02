from __future__ import annotations
from day import Day


class User:
    """Holds a user's name and data."""

    # Class variables:

    _GLUCOSE_LOW_RANGE = 80     # Glucose below this range is low.
    _GLUCOSE_HIGH_RANGE = 140   # Glucose above this range is high.

    _ACTIVITY_RANGE_LOW = 30    # Activity amounts below this range are too low.
    _ACTIVITY_RANGE_HIGH = 60   # Activity amounts below this range are acceptable, and above are great.

    _CARB_RANGE_LOW = 15        # Carb amounts below this range are low.
    _CARB_RANGE_MID = 30        # Carb amounts below this range are good.
    _CARB_RANGE_HIGH = 45       # Carb amounts below this range are poor (too high),
                                #   and above are terrible (way too high)

    _MEALS_PER_DAY = 3          # The expected number of meals per day.

    def __init__(self, name, first_day=None, last_day=None):
        """Returns a User object.

        :param name: string
        :param first_day: Day
        :param last_day: Day
        """
        self._name = name
        self._first_day = first_day
        self._last_day = last_day

    @property
    def name(self) -> str:
        """Returns the user's name as a string."""
        return self._name

    @name.setter
    def name(self, value):
        """Sets the user's name.

        :param value: string"""
        self._name = value

    @property
    def first_day(self) -> Day:
        """Returns the first day in the user's doubly-linked list of Days."""
        return self._first_day

    @first_day.setter
    def first_day(self, value):
        """Sets the first day in the user's doubly-linked list of Days.

        :param value: Day"""
        self._first_day = value

    @property
    def last_day(self) -> Day:
        """Returns the last day in the user's doubly-linked list of Days."""
        return self._last_day

    @last_day.setter
    def last_day(self, value):
        """Sets the last day in the user's doubly-linked list of Days.

        :param value: Day"""
        self._last_day = value

    def calculate_average_glucose(self, total_days_back=0) -> float:
        """Calculates average glucose over last specified number of days.
        0 days means today.

        :param total_days_back: int
        :return: float"""
        current_day = self.last_day     # Start at the final day.
        days_back = 0                   # counter to hold days we went back.
        glucose_total = 0               # Accumulator variable to hold total glucose.
        number_of_records = 0           # Accumulates the total number of records over the traversed days.

        # While there are still days to go back...
        while days_back <= total_days_back and current_day is not None:
            number_of_records += current_day.get_number_of_records()    # Inrease the number of records
            glucose_total += current_day.get_total_glucose()            # Increase the glucose total.
            current_day = current_day.previous_day                      # Move to the previous day
            days_back += 1                                              # Increment days_back count.

        # If there were no records, set average to 0.
        if number_of_records == 0:
            glucose_average = 0
        # Otherwise, compute average as (total glucose from found records) / (number of records found)
        else:
            glucose_average = glucose_total / number_of_records

        return glucose_average

    def get_glucose_rating(self, glucose) -> str:
        """Returns a string representing the rating of the glucose value.

        :param glucose: float
        :return: string
        """
        if glucose in range(User._GLUCOSE_LOW_RANGE, User._GLUCOSE_HIGH_RANGE):
            glucose_rating = "Excellent"
        elif glucose < User._GLUCOSE_LOW_RANGE:
            glucose_rating = "Poor (low)"
        elif glucose < User._GLUCOSE_HIGH_RANGE:
            glucose_rating = "Poor (high)"
        else:
            glucose_rating = "Awful (very high)"

        return glucose_rating

    def calculate_average_time_active(self, total_days_back=0) -> float:
        """Calculates the average time active over the last specified number of days.

        :param total_days_back: int
        :return: float"""
        time_active_total = 0           # Accumulator to hold total time active.
        days_back = 0                   # Counter to hold days we went back.
        current_day = self.last_day     # Start at the last day.

        # While there are still days to go back...
        while days_back <= total_days_back and current_day is not None:
            time_active_total += current_day.get_time_active()  # Increase the time active total.
            days_back += 1                                      # Increment days_back count.
            current_day = current_day.previous_day              # Move to the previous day.

        # If days back is greater than 0, compute average time active.
        if days_back > 0:
            time_active_average = time_active_total / days_back

        # Otherwise, set average time active to 0.
        else:
            time_active_average = 0

        return time_active_average

    def get_time_active_rating(self, time_active) -> str:
        """Returns a string representing the rating of the time active.

        :param time_active: float
        :return: string"""
        if time_active < User._ACTIVITY_RANGE_LOW:
            time_active_rating = "Poor (low)"
        elif time_active < User._ACTIVITY_RANGE_HIGH:
            time_active_rating = "Good"
        else:
            time_active_rating = "Excellent"
        return time_active_rating

    def calculate_average_carbs_per_meal(self, total_days_back=0) -> float:
        """Calculates the average carbs per meal over the last specified number of days.

        :param total_days_back: int
        :return: float"""
        current_day = self.last_day     # Start at the last day.
        days_back = 0                   # Counter to hold days we went back.
        carb_total = 0                  # Accumulator to hold the total carbs.
        total_meals_eaten = 0           # Accumulator to hold the total number of meals eaten.

        # While there are still days to go back...
        while days_back <= total_days_back and current_day is not None:
            total_meals_eaten += current_day.get_meals_eaten()  # Increase number of meals eaten.
            carb_total += current_day.get_total_carbs()         # Increase total number of carbs.
            current_day = current_day.previous_day              # Move to the previous day.
            days_back += 1                                      # Increment the days_back counter.

        # If no meals were eaten, set average carbs to 0.
        if total_meals_eaten == 0:
            average_carbs_per_meal = 0

        # Otherwise, calculate average carbs per meal as (total carbs) / (total meals).
        else:
            average_carbs_per_meal = carb_total / total_meals_eaten

        return average_carbs_per_meal

    def get_carbs_per_meal_rating(self, carbs_per_meal) -> str:
        """Returns a string representing the rating of the carbs eaten.

        :param carbs_per_meal: float
        :return: string"""
        if carbs_per_meal in range(User._CARB_RANGE_LOW, User._CARB_RANGE_MID):
            carbs_per_meal_rating = "Excellent"
        elif carbs_per_meal < User._CARB_RANGE_LOW:
            carbs_per_meal_rating = "Poor (low)"
        elif carbs_per_meal in range(User._CARB_RANGE_MID, User._CARB_RANGE_HIGH):
            carbs_per_meal_rating = "Okay"
        else:
            carbs_per_meal_rating = "Poor (high)"

        return carbs_per_meal_rating

    def calculate_average_meals_missed(self, total_days_back=0) -> float:
        """Calculates the average number of meals missed over the last specified number of days.

        :param total_days_back: int
        :return: float"""
        current_day = self.last_day     # Start at the last day.
        days_back = 0                   # Counter to hold days we went back.
        total_meals_eaten = 0           # Accumulator to hold the total number of meals eaten.
        total_number_of_records = 0     # Accumulator to hold the total number of records found.

        # While there are still days to go back...
        while days_back <= total_days_back and current_day is not None:
            total_meals_eaten += current_day.get_meals_eaten()              # Increase number of meals eaten.
            total_number_of_records += current_day.get_number_of_records()  # Increase total number of records.
            current_day = current_day.previous_day                          # Move to the previous day.
            days_back += 1                                                  # Increment days_back counter.

        # If the total number of records is greater than 0, calculate average meals missed per day.
        # (meals eaten / total records) is the ratio of meals eaten.
        # (1 - (ratio of meals eaten)) is the ratio of meals missed.
        # (MEALS PER DAY * ratio of meals missed) is the average number of missed meals per day.
        # Algebraically: MEALS PER DAY * (1 - (meals eaten / total records)) = average meals missed per day.
        if total_number_of_records > 0:
            average_meals_missed = User._MEALS_PER_DAY * (1 - (total_meals_eaten / total_number_of_records))

        # If the number of records is 0, assume that all meals were missed every day.
        else:
            average_meals_missed = self._MEALS_PER_DAY

        return average_meals_missed

    def get_meals_missed_rating(self, meals_missed) -> str:
        """Returns a string representing the rating of the amount of meals missed.

        :param meals_missed: float
        :return: string"""
        if meals_missed == 0:  # no meals missed, excellent
            meals_missed_rating = "Excellent"
        elif meals_missed <= 1:  # one or less meals missed per day
            meals_missed_rating = "Okay"
        else:  # more than one meal missed per day
            meals_missed_rating = "Poor"
        return meals_missed_rating

    def is_day_in_list(self, date_of_day) -> bool:
        """Returns true if a certain date is already in the doubly-linked list of Days.

        :param date_of_day: datetime.date
        :return: bool"""

        # If there is no first day, then a day is not in the list.
        if self.first_day is None:
            return False

        # If the date of the new day comes before the
        # first day or after the last day, it isn't in the list.
        if date_of_day < self.first_day.date_of_day or date_of_day > self.last_day.date_of_day:
            return False

        # Otherwise, we have to look through the whole list.
        else:
            # Start at the end of the list of days
            current_day = self.last_day

            # While there are still days to loop through...
            while current_day is not None:
                # Check if the current day's date is equal to the date provided.
                if current_day.date_of_day == date_of_day:
                    return True
                # Set current day to previous day.
                current_day = current_day.previous_day

            # If the loop has completed, the date was not found. Return False.
            return False

    def insert_day_in_list(self, new_day) -> bool:
        """Inserts day into the list. Returns false if day is already in list.

        :param new_day: Day
        :return: bool"""

        # If day is already in list, do nothing and return False.
        if self.is_day_in_list(new_day.date_of_day):
            return False

        # Otherwise, if list is empty, set first and last days to this initial Day.
        elif self.first_day is None:
            self.first_day = new_day
            self.last_day = new_day

        # Otherwise, if the new day comes before the first day, prepend the new Day to
        # the start of the list, and set the first_day instance variable to point at it.
        elif new_day.date_of_day < self.first_day.date_of_day:
            new_day.next_day = self.first_day
            self.first_day.previous_day = new_day
            self.first_day = new_day

        # Otherwise, if the new day comes after the last day, append the new Day to
        # the end of the list, and set the last_day instance variable to point at it.
        elif new_day.date_of_day > self.last_day.date_of_day:
            new_day.previous_day = self.last_day
            self.last_day.next_day = new_day
            self.last_day = new_day

        # Otherwise, find where the new Day fits in the list...
        else:
            # ...move backwards from the end until you find the Day that comes immediately before it.
            current_day = self.last_day
            while new_day.date_of_day < current_day.date_of_day:
                current_day = current_day.previous_day

            # Set the new Day's previous day to what comes before it...
            new_day.previous_day = current_day

            # Set the new Day's next day to what comes after it...
            new_day.next_day = current_day.next_day

            # Set the next Day's previous day to the new day...
            new_day.next_day.previous_day = new_day

            # ...And finally, set the previous Day's next day to the new day.
            new_day.previous_day.next_day = new_day

        # Return True to indicate that the Day was inserted.
        return True

    def _cleanup_empty_days(self):
        """Removes all empty Days from the list."""
        # If the list is empty, do nothing.
        if self.first_day == None:
            pass
        else:
            # Remove all empty days from the start of the list
            while self.first_day != None and self.first_day.get_number_of_records() == 0:
                # Special case: Only one day in list. Set both first and last day to None.
                if self.first_day is self.last_day:
                    self.first_day = None
                    self.last_day = None

                # Otherwise, set first day to the next day, and remove previous first day from the list.
                else:
                    self.first_day = self.first_day.next_day
                    self.first_day.previous_day = None

            # Remove all empty days from the end of the list
            while self.last_day != None and self.last_day.get_number_of_records() == 0:
                # Set last day to the previous day, and remove previous last day from the list
                self.last_day = self.last_day.previous_day
                self.last_day.next_day = None

            # Remove all empty days from the middle of the list
            current_day = self.first_day
            # While there are still days to traverse:
            while current_day.date_of_day < self.last_day.date_of_day:
                # If the day we are currently looking at has no records, remove ourself from the list of Days:
                if current_day.get_number_of_records() == 0:
                    # Set the previous day's next day to point at our next day...
                    current_day.previous_day.next_day = current_day.next_day
                    # ...and set the next day's previous day to point at our previous day.
                    current_day.next_day.previous_day = current_day.previous_day
                # Move forwards one day.
                current_day = current_day.next_day

    def _update_days(self):
        """Private function. Runs through the entire doubly-linked list of Days and calls their _update function."""
        day_to_update = self.first_day
        while day_to_update is not None:
            day_to_update._update()
            day_to_update = day_to_update.next_day
