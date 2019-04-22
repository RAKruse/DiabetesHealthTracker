from __future__ import annotations
from record import Record
from datetime import date

class Day:
    """Container class. Holds three records,
    the date, and pointers to next and previous days."""

    def __init__(self, morning_record=None, evening_record=None,
                 night_record=None, date_of_day=date.today(),
                 next_day=None, previous_day=None):
        self._morning_record = morning_record
        self._evening_record = evening_record
        self._night_record = night_record
        self._date_of_day = date_of_day
        self._next_day = next_day
        self._previous_day = previous_day

    # TODO: Docstrings.

    @property
    def morning_record(self) -> Record:
        return self._morning_record

    @morning_record.setter
    def morning_record(self, record):
        self._morning_record = record

    @property
    def evening_record(self) -> Record:
        return self._evening_record

    @evening_record.setter
    def evening_record(self, record):
        self._evening_record = record

    @property
    def night_record(self) -> Record:
        return self._night_record

    @night_record.setter
    def night_record(self, record):
        self._night_record = record

    @property
    def date_of_day(self) -> date:
        return self._date_of_day

    @date_of_day.setter
    def date_of_day(self, new_date):
        self._date_of_day = new_date

    @property
    def next_day(self) -> Day:
        return self._next_day

    @next_day.setter
    def next_day(self, new_day):
        self._next_day = new_day

    @property
    def previous_day(self) -> Day:
        return self._previous_day

    @previous_day.setter
    def previous_day(self, new_day):
        self._previous_day = new_day

    def get_total_glucose(self) -> int:
        """Returns the sum of all glucose readings for that day.
        Useful for finding averages."""
        total_glucose = 0
        if self.morning_record is not None:
            total_glucose += self.morning_record.glucose
        if self.evening_record is not None:
            total_glucose += self.evening_record.glucose
        if self.night_record is not None:
            total_glucose += self.night_record.glucose

        return total_glucose

    def get_time_active(self) -> int:
        """Returns time active in minutes."""
        total_time_active = 0
        if self.morning_record is not None:
            total_time_active += self.morning_record.get_time_active()
        if self.evening_record is not None:
            total_time_active += self.evening_record.get_time_active()
        if self.night_record is not None:
            total_time_active += self.night_record.get_time_active()

        return total_time_active

    def get_meals_eaten(self) -> int:
        """Returns the number of meals eaten for the day.
        Useful for finding averages."""
        meals_eaten = 0
        if self.morning_record is not None and \
                self.morning_record.was_meal_eaten():
            meals_eaten += 1
        if self.evening_record is not None and \
                self.evening_record.was_meal_eaten():
            meals_eaten += 1
        if self.night_record is not None and \
                self.night_record.was_meal_eaten():
            meals_eaten += 1

        return meals_eaten

    def get_total_carbs(self) -> int:
        total_carbs = 0
        if self.morning_record is not None:
            total_carbs += self.morning_record.carbs
        if self.evening_record is not None:
            total_carbs += self.evening_record.carbs
        if self.night_record is not None:
            total_carbs += self.night_record.carbs

        return total_carbs

    def get_number_of_records(self):
        """Returns the number of records for the day.
        Useful for finding averages."""
        number_of_records = 0
        if self.morning_record is not None:
            number_of_records += 1
        if self.evening_record is not None:
            number_of_records += 1
        if self.night_record is not None:
            number_of_records += 1

        return number_of_records

    def __str__(self):
        val = "Date: " + self.date_of_day.strftime("%m/%d/%Y") + "\nMorning record:\n"
        if self.morning_record is not None:
            val += str(self.morning_record)
        else:
            val += "None\n"
        val += "\nEvening record:\n"
        if self.evening_record is not None:
            val += str(self.evening_record)
        else:
            val += "None\n"
        val += "\nNight record:\n"
        if self.night_record is not None:
            val += str(self.night_record)
        else:
            val += "None"

        return val
