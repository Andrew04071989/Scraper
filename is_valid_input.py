"""
This module is responsible for checking the correctness
of the data entered by the user and
displaying error messages with the ability to re-enter the data.
"""
from datetime import date
from get_default_values import DefaultValues


class IsValid(object):
    """
    This class checks the correctness of the data entered by the user
    and displays error messages with the ability to re-enter the data.
    """
    def __init__(self, from_city, to_city,
                 depart_date, return_date):
        self.url = "https://www.airblue.com/" \
                   "bookings/flight_selection.aspx"
        self.from_city = from_city
        self.to_city = to_city
        self.depart_date = depart_date
        self.return_date = return_date
        self.is_valid_dict = {
            'depart city': False,
            'arrive city': False,
            'depart date value': False,
            'return date value': False,
            'depart date format': False,
            'return date format': False}
        self.def_val = DefaultValues(self.url)

    @staticmethod
    def get_date_from_string(string_date):
        """
        This static method takes a date(type - string)
        and returns a date(type - datetime.date).
        """
        year_month_day = string_date.split('-')
        year, month, day = \
            int(year_month_day[0]), \
            int(year_month_day[1]), \
            int(year_month_day[2])
        date_format_datetime = date(year, month, day)
        return date_format_datetime

    def input_depart_city(self):
        """
        This method verifies the correctness of the
        IATA departure city code entered by the user,
        displays a message about the need to re-enter
        the IATA code in case of an error
        until it becomes correct and
        returns a dictionary to which the value of True
        is added by the key 'depart city'.
        """
        valid = self.is_valid_dict
        dep_cities = \
            self.def_val.get_depart_city_values()
        while valid['depart city'] is False:
            if self.from_city in set(dep_cities):
                valid['depart city'] = True
            else:
                print('\nInvalid IATA departure city code. \n'
                      'IATA-code must contain '
                      '3 uppercase letter characters. \n'
                      'List of permitted IATA codes '
                      'for departure cities: {}'.
                      format(set(dep_cities)))
                self.from_city = input(
                    'Please re-enter departure city IATA-code: ')
        return valid

    def input_arrive_city(self):
        """
        This method verifies the correctness of the
        IATA arrival city code entered by the user,
        displays a message about the need to re-enter
        the IATA code in case of an error
        until it becomes correct and
        returns a dictionary to which the value of True
        is added by the key 'arrive city'.
        """
        valid = self.input_depart_city()
        if valid['depart city'] is True:
            arr_cities = \
                self.def_val.get_arrive_city_values(self.from_city)
            if self.from_city in arr_cities:
                arr_cities.remove(self.from_city)
            while valid['arrive city'] is False:
                if self.to_city in arr_cities:
                    valid['arrive city'] = True
                elif arr_cities == []:
                    valid['depart city'] = False
                    print('\nSorry! According to information today '
                          'there are no flights from '
                          'the specified city with IATA - {}'.
                          format(self.from_city))
                    self.from_city = input(
                        'Please enter another '
                        'IATA-code of departure city : ')
                    self.input_arrive_city()
                else:
                    print('\nInvalid IATA arrive city code. \n'
                          'IATA-code must contain '
                          '3 uppercase letter characters. \n'
                          'List of permitted IATA codes '
                          'for arrive cities: {}'.
                          format(set(arr_cities)))
                    self.to_city = input(
                        'Please re-enter arrive city IATA-code: ')
        return valid

    def depart_date_format(self):
        """
        This method checks the correctness of the departure
        date format, displays a message about the need to re-enter
        it in case of an error until it becomes correct and
        returns a dictionary to which the value of True
        is added by the key 'depart date format'.
        """
        valid = self.input_arrive_city()
        while valid['depart date format'] is False:
            try:
                self.get_date_from_string(self.depart_date)
                valid['depart date format'] = True
            except ValueError:
                self.depart_date = input(
                    '\nThe departure date can contain only '
                    'numeric values and "-" and '
                    'must be in format YYYY-MM-DD. \n'
                    'Please re-enter depart date: ')
            except IndexError:
                self.depart_date = input(
                    '\nIncorrect format. The departure date '
                    'must be in format YYYY-MM-DD. \n'
                    'Please re-enter depart date: ')
        return valid

    def return_date_format(self):
        """
        This method checks the correctness of the return
        date format, displays a message about the need to re-enter
        it in case of an error until it becomes correct and
        returns a dictionary to which the value of True
        is added by the key 'return date format'.
        """
        valid = self.depart_date_format()
        if self.return_date == '':
            valid['return date format'] = True
            valid['return date value'] = True
        while valid['return date format'] is False:
            try:
                self.get_date_from_string(self.return_date)
                valid['return date format'] = True
            except ValueError:
                self.return_date = input(
                    '\nThe return date can contain only '
                    'numeric values and "-" and '
                    'must be in format YYYY-MM-DD. \n'
                    'Please re-enter depart date: ')
            except IndexError:
                self.return_date = input(
                    '\nIncorrect format. The return date '
                    'must be in format YYYY-MM-DD. \n'
                    'Please re-enter return date: ')
        return valid

    def is_dep_date_according_to_default(self):
        """
        This method checks that the departure date matches
        the default values, displays a message that it needs
        to be re-entered in case of an error until it is correct, and
        returns a dictionary to which the True value
        is added by the 'depart date value' key.
        """
        valid = self.return_date_format()
        default_dep_date_m_y = \
            self.def_val.get_depart_months_years_values()
        default_dep_date_d = \
            self.def_val.get_depart_days_values()
        while valid['depart date value'] is False:
            depart_date_str = self.depart_date.split('-')
            depart_month_year = '{}-{}'.format(
                depart_date_str[0],
                depart_date_str[1])
            depart_day = depart_date_str[2]
            if depart_month_year in set(default_dep_date_m_y) and \
                    depart_day in set(default_dep_date_d):
                valid['depart date value'] = True
            else:
                self.depart_date = input(
                    '\nInvalid depart date. \n'
                    'Date does not exist or '
                    'is not allowed to be used. \n'
                    'Please re-enter: ')
        return valid

    def is_ret_date_according_to_default(self):
        """
        This method checks that the return date matches
        the default values, displays a message that it needs
        to be re-entered in case of an error until it is correct, and
        returns a dictionary to which the True value
        is added by the 'return date value' key.
        """
        valid = self.is_dep_date_according_to_default()
        depart_date = self.get_date_from_string(self.depart_date)
        default_ret_date_m_y = \
            self.def_val.get_return_months_years_values()
        default_ret_date_d = \
            self.def_val.get_return_days_values()
        while valid['return date value'] is False:
            return_date_str = self.return_date.split('-')
            return_date = self.get_date_from_string(self.return_date)
            return_month_year = '{}-{}'.format(
                return_date_str[0],
                return_date_str[1])
            return_day = return_date_str[2]
            if (return_month_year in
                    set(default_ret_date_m_y) and
                    return_day in
                    set(default_ret_date_d)):
                if return_date < depart_date:
                    print("\nError: The return date can't be earlier "
                          "than the departure date.")
                    self.depart_date = input(
                        "\nPlease re-enter departure date: ")
                    self.return_date = input(
                        "\nPlease re-enter return date: ")
                    valid = self.is_ret_date_according_to_default()
                else:
                    valid['return date value'] = True
            else:
                self.return_date = input(
                    '\nInvalid return date. \n'
                    'Date does not exist '
                    'or is not allowed to be used. \n'
                    'Please re-enter: ')
        return valid
