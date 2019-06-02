from __future__ import annotations
from record import Record
from datetime import date


class Day:
    """Container class. Holds three records,
    the date, and pointers to next and previous days."""

    def __init__(self, morning_record=None, afternoon_record=None,
                 evening_record=None, date_of_day=date.today(),
                 next_day=None, previous_day=None):
        """
        Returns a Day object.

        :param morning_record: Record
        :param afternoon_record: Record
        :param evening_record: Record
        :param date_of_day: datetime.date
        :param next_day: Day
        :param previous_day: Day
        """
        self._morning_record = morning_record
        self._afternoon_record = afternoon_record
        self._evening_record = evening_record
        self._date_of_day = date_of_day
        self._next_day = next_day
        self._previous_day = previous_day

    @property
    def morning_record(self) -> Record:
        """Returns the Record representing the morning."""
        return self._morning_record

    @morning_record.setter
    def morning_record(self, record):
        """Sets the Record representing the morning.

        :param record: Record"""
        self._morning_record = record

    @property
    def afternoon_record(self) -> Record:
        """Returns the Record representing the afternoon."""
        return self._afternoon_record

    @afternoon_record.setter
    def afternoon_record(self, record):
        """Sets the Record representing the afternoon.

        :param record: Record"""
        self._afternoon_record = record

    @property
    def evening_record(self) -> Record:
        """Returns the Record representing the evening."""
        return self._evening_record

    @evening_record.setter
    def evening_record(self, record):
        """Sets the Record representing the evening.

        :param record: Record"""
        self._evening_record = record

    @property
    def date_of_day(self) -> date:
        """Returns the day's date as a datetime.date object."""
        return self._date_of_day

    @date_of_day.setter
    def date_of_day(self, new_date):
        """Sets the day's date to the date specified.

        :param new_date: datetime.date"""
        self._date_of_day = new_date

    @property
    def next_day(self) -> Day:
        """Returns the next Day in the doubly-linked list of Days."""
        return self._next_day

    @next_day.setter
    def next_day(self, new_day):
        """Sets the next day in the doubly-linked list of Days.

        :param new_day: Day"""
        self._next_day = new_day

    @property
    def previous_day(self) -> Day:
        """Returns the previous Day in the doubly-linked list of Days."""
        return self._previous_day

    @previous_day.setter
    def previous_day(self, new_day):
        """Sets the previous day in the doubly-linked list of Days.

        :param new_day: Day"""
        self._previous_day = new_day

    def get_total_glucose(self) -> int:
        """Returns the sum of all glucose readings for that day.
        Useful for finding averages.

        :return: int"""
        total_glucose = 0
        if self.morning_record is not None:
            total_glucose += self.morning_record.glucose
        if self.afternoon_record is not None:
            total_glucose += self.afternoon_record.glucose
        if self.evening_record is not None:
            total_glucose += self.evening_record.glucose

        return total_glucose

    def get_time_active(self) -> int:
        """Returns time active in minutes for that day.

        :return: int"""
        total_time_active = 0
        if self.morning_record is not None:
            total_time_active += self.morning_record.get_time_active()
        if self.afternoon_record is not None:
            total_time_active += self.afternoon_record.get_time_active()
        if self.evening_record is not None:
            total_time_active += self.evening_record.get_time_active()

        return total_time_active

    def get_meals_eaten(self) -> int:
        """Returns the number of meals eaten for the day.
        Useful for finding averages.

        :return: int"""
        meals_eaten = 0
        if self.morning_record is not None and \
                self.morning_record.was_meal_eaten():
            meals_eaten += 1
        if self.afternoon_record is not None and \
                self.afternoon_record.was_meal_eaten():
            meals_eaten += 1
        if self.evening_record is not None and \
                self.evening_record.was_meal_eaten():
            meals_eaten += 1

        return meals_eaten

    def get_total_carbs(self) -> int:
        """Returns the total caarbs eaten for that day.
        Useful for finding averages.

        :return: int"""
        total_carbs = 0
        if self.morning_record is not None:
            total_carbs += self.morning_record.carbs
        if self.afternoon_record is not None:
            total_carbs += self.afternoon_record.carbs
        if self.evening_record is not None:
            total_carbs += self.evening_record.carbs

        return total_carbs

    def get_number_of_records(self) -> int:
        """Returns the number of records for the day.
        Useful for finding averages.

        :return: int"""
        number_of_records = 0
        if self.morning_record is not None:
            number_of_records += 1
        if self.afternoon_record is not None:
            number_of_records += 1
        if self.evening_record is not None:
            number_of_records += 1

        return number_of_records

    def __str__(self):
        """Returns a string representation of the Day object."""

        # Present the date and morning label...
        val = "Date: " + self.date_of_day.strftime("%m/%d/%Y") + "\nMorning record:\n"

        # ...if there is a Morning Record, represent it. Else, say None.
        if self.morning_record is not None:
            val += str(self.morning_record)
        else:
            val += "None\n"

        # Present the afternoon label...
        val += "\nAfternoon record:\n"

        # ...if there is an Afternoon Record, represent it. Else, say None.
        if self.afternoon_record is not None:
            val += str(self.afternoon_record)
        else:
            val += "None\n"

        # Present the evening label...
        val += "\nEvening record:\n"

        # ...if there is an Evening Record, represent it. Else, say None.
        if self.evening_record is not None:
            val += str(self.evening_record)
        else:
            val += "None"

        return val

    def _update(self):
        """Private function. Used to update pre-existing binary data files to the appropriate format."""
        # If there is no _afternoon_record attribute...
        if not hasattr(self, '_afternoon_record') and hasattr(self, '_night_record'):
            self._afternoon_record = self._evening_record   # Create _afternoon_record attribute and set it to
                                                            # _evening_record's value.
            self._evening_record = self._night_record       # Set _evening_record to _night_record's value.
            delattr(self, '_night_record')                  # Delete the _night_record attribute.
