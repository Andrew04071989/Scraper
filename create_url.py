""" This module is responsible for url generation """


class UrlConstructor(object):
    """
    This class makes up the url, depending on
    the parameters entered by the user.
    """
    def __init__(self, from_city, to_city,
                 depart_date, return_date):
        self.url = "https://www.airblue.com/" \
                   "bookings/flight_selection.aspx"
        self.from_city = from_city
        self.to_city = to_city
        self.depart_date = depart_date
        self.return_date = return_date

    @staticmethod
    def get_date_year_month(date):
        """
        This staticmethod takes a date (type-string) and
        returns the year and month in the format YYYY-MM (type-string).
        """
        cut_date = date.split('-')
        date_month_year = cut_date[0] + '-' + cut_date[1]
        return date_month_year

    @staticmethod
    def get_date_day(date):
        """
        This staticmethod takes a date (of type-string)
        and returns a day in the format DD (of type-string).
        """
        cut_date = date.split('-')
        return cut_date[2]

    def get_parameters_string(self, search_type, d_month_year,
                              d_day, r_month_year='', r_day=''):
        """ This method creates a variable part of the URL. """
        parameters_string = \
            "?TT={}&SS=&RT=&FL=&DC={}" \
            "&AC={}&AM={}&AD={}&DC=&AC=" \
            "&AM=&AD=&DC=&AC=&AM=&AD=&DC=" \
            "&AC=&AM=&AD=&RM={}&RD={}" \
            "&PA=1&PC=&PI=&CC=&NS=&CD=". \
            format(search_type, self.from_city,
                   self.to_city, d_month_year,
                   d_day, r_month_year, r_day)
        return parameters_string

    def contain_url(self):
        """
        This method generates and return a url based on
        the parameters(departure city IATA-code,
        arrival city IATA-code, depart_date and return_date)
        entered by the user.
        """
        url = self.url

        d_month_year = self.get_date_year_month(self.depart_date)
        d_day = self.get_date_day(self.depart_date)
        if self.return_date == '':
            # If no return date is entered,
            # the 'search_type' parameter
            # is set to 'OW' (One Way).
            search_type = 'OW'
            parameters = self.get_parameters_string(
                search_type, d_month_year, d_day)
        else:
            # If a return date is entered,
            # the 'search_type' parameter
            # is set to 'RT' (Round Trip).
            search_type = 'RT'
            r_month_year = self.get_date_year_month(self.return_date)
            r_day = self.get_date_day(self.return_date)
            parameters = self.get_parameters_string(
                search_type, d_month_year, d_day,
                r_month_year, r_day)
        url = url + parameters
        return url
