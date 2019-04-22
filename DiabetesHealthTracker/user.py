from __future__ import annotations
from day import Day

class User:
    """Holds a user's name and data."""

    _GLUCOSE_LOW_RANGE = 80
    _GLUCOSE_HIGH_RANGE = 140
    _ACTIVITY_RANGE_LOW = 30
    _ACTIVITY_RANGE_HIGH = 60
    _CARB_RANGE_LOW = 15
    _CARB_RANGE_MID = 30
    _CARB_RANGE_HIGH = 45
    _MEALS_PER_DAY = 3

    # TODO: Docstrings, refactor potentially repetitious methods.
    # I mean, do I really need prepend and append? I can just
    # fold those into insert_day_in_list.

    def __init__(self, name, first_day=None, last_day=None):
        self._name = name
        self._first_day = first_day
        self._last_day = last_day

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def first_day(self):
        return self._first_day

    @first_day.setter
    def first_day(self, value):
        self._first_day = value

    @property
    def last_day(self):
        return self._last_day

    @last_day.setter
    def last_day(self, value):
        self._last_day = value

    def calculate_average_glucose(self, total_days_back=0) -> float:
        """Calculates average glucose over last specified number of days.
        0 days means today."""
        current_day = self.last_day
        days_back = 0
        glucose_total = 0
        number_of_records = 0
        while days_back <= total_days_back and current_day is not None:
            number_of_records += current_day.get_number_of_records()
            glucose_total += current_day.get_total_glucose()
            current_day = current_day.previous_day
            days_back += 1
        glucose_average = glucose_total / number_of_records
        return glucose_average

    def get_glucose_rating(self, glucose) -> str:
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
        time_active_total = 0
        days_back = 0
        current_day = self.last_day
        while days_back <= total_days_back and current_day is not None:
            time_active_total += current_day.get_time_active()
            days_back += 1
            current_day = current_day.previous_day
        time_active_average = time_active_total / days_back
        return time_active_average

    def get_time_active_rating(self, time_active) -> str:
        if time_active < User._ACTIVITY_RANGE_LOW:
            time_active_rating = "Poor (low)"
        elif time_active < User._ACTIVITY_RANGE_HIGH:
            time_active_rating = "Good"
        else:
            time_active_rating = "Excellent"
        return time_active_rating

    def calculate_average_carbs_per_meal(self, total_days_back=0) -> float:
        current_day = self.last_day
        days_back = 0
        carb_total = 0
        total_meals_eaten = 0
        while days_back <= total_days_back and current_day is not None:
            total_meals_eaten += current_day.get_meals_eaten()
            carb_total += current_day.get_total_carbs()
            current_day = current_day.previous_day
            days_back += 1
        if total_meals_eaten == 0:
            average_carbs_per_meal = 0
        else:
            average_carbs_per_meal = carb_total / total_meals_eaten
        return average_carbs_per_meal

    def get_carbs_per_meal_rating(self, carbs_per_meal):
        if carbs_per_meal in range(User._CARB_RANGE_LOW, User._CARB_RANGE_MID):
            carbs_per_meal_rating = "Excellent"
        elif carbs_per_meal < User._CARB_RANGE_LOW:
            carbs_per_meal_rating = "Poor (low)"
        elif carbs_per_meal in range(User._CARB_RANGE_MID, User._CARB_RANGE_HIGH):
            carbs_per_meal_rating = "Okay"
        else:
            carbs_per_meal_rating = "Poor (high)"

        return carbs_per_meal_rating

    def calculate_average_meals_missed(self, total_days_back=0):
        current_day = self.last_day
        days_back = 0
        total_meals_eaten = 0
        total_number_of_records = 0
        while days_back <= total_days_back and current_day is not None:
            total_meals_eaten += current_day.get_meals_eaten()
            total_number_of_records += current_day.get_number_of_records()
            current_day = current_day.previous_day
            days_back += 1
        average_meals_missed = User._MEALS_PER_DAY * (1 - (total_meals_eaten / total_number_of_records))
        return average_meals_missed

    def get_meals_missed_rating(self, meals_missed):
        if meals_missed == 0:  # no meals missed, excellent
            meals_missed_rating = "Excellent"
        elif meals_missed <= 1:  # one or less meals missed per day
            meals_missed_rating = "Okay"
        else:  # more than one meal missed per day
            meals_missed_rating = "Poor"
        return meals_missed_rating

    def append_day_to_list(self, new_day):
        new_day.previous_day = self.last_day
        self.last_day.next_day = new_day
        self.last_day = new_day

    def prepend_day_to_list(self, new_day):
        new_day.next_day = self.first_day
        self.first_day.previous_day = new_day
        self.first_day = new_day

    def is_day_in_list(self, date_of_day) -> bool:
        if self.first_day is None:
            return False
        if date_of_day < self.first_day.date_of_day or date_of_day > self.last_day.date_of_day:
            return False
        else:
            current_day = self.last_day
            while current_day is not None:
                if current_day.date_of_day == date_of_day:
                    return True
                current_day = current_day.previous_day
            return False

    def insert_day_in_list(self, new_day) -> bool:
        """Inserts day into the list. Returns false if day is already in list."""
        if self.is_day_in_list(new_day.date_of_day):
            return False
        elif self.first_day is None:
            self.first_day = new_day
            self.last_day = new_day
        elif new_day.date_of_day < self.first_day.date_of_day:
            self.prepend_day_to_list(new_day)
        elif new_day.date_of_day > self.last_day.date_of_day:
            self.append_day_to_list(new_day)
        else:
            current_day = self.last_day
            while new_day.date_of_day < current_day.date_of_day:
                current_day = current_day.previous_day
            new_day.previous_day = current_day
            new_day.next_day = current_day.next_day
            new_day.next_day.previous_day = new_day
            new_day.previous_day.next_day = new_day

        return True
