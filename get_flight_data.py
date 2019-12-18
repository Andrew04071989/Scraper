""" This module is responsible for receiving flight data. """
from get_tree import Tree
from create_url import UrlConstructor


class FlightData:
    """ This class is responsible for receiving flight data. """
    def __init__(self, from_city, to_city,
                 depart_date, return_date):
        self.url = "https://www.airblue.com/" \
                   "bookings/flight_selection.aspx"
        self.from_city = from_city
        self.to_city = to_city
        self.depart_date = depart_date
        self.return_date = return_date
        self.url_cons = UrlConstructor(
            self.from_city, self.to_city,
            self.depart_date, self.return_date)
        self.work_url = self.url_cons.contain_url()
        self.tree = Tree()
        self.tree_get = self.tree.tree_method_get(self.work_url)

    def get_trip_data_list(self):
        """
        This method returns a list
        of all possible combinations
        of forward and reverse flights
        """
        tree_get = self.tree_get
        data_list = []
        ssp_code_value = tree_get.xpath(
            "//input[@name = 'ssp']/@value")
        fsc_code_value = tree_get.xpath(
            "//input[@name = 'fsc']/@value")
        trip_1_code_value = tree_get.xpath(
            "//input[@name = 'trip_1']/@value")
        if self.return_date != '':
            trip_2_code_value = tree_get.xpath(
                "//input[@name = 'trip_2']/@value")
            for trip_1 in trip_1_code_value:
                for trip_2 in trip_2_code_value:
                    race_data = {'ssp': ssp_code_value,
                                 'fsc': fsc_code_value,
                                 'trip_1': trip_1,
                                 'trip_2': trip_2}

                    data_list.append(race_data)
        else:
            for trip_1 in trip_1_code_value:
                race_data = {'ssp': ssp_code_value,
                             'fsc': fsc_code_value,
                             'trip_1': trip_1}
                data_list.append(race_data)
        return data_list

    def get_trees_post_list(self):
        """
        This method is a list of element trees(DOM),
        depending on the number of combinations from the list
        of combinations of flights generated
        by the get_trip_data_list() function.
        """
        trees_list = []
        for data in self.get_trip_data_list():
            tree_post = self.tree.tree_method_post(self.work_url, data)
            trees_list.append(tree_post)
        return trees_list

    @staticmethod
    def get_flight_directions(post_tree):
        """
        This staticmethod takes an element tree (DOM)
        and returns an array of flight directions.
        """
        flight_directions = post_tree.xpath(
            "//caption[@class = 'message-lines-0']/"
            "text()")
        for _ in range(len(flight_directions)):
            flight_directions[_] = \
                flight_directions[_].strip()
        return flight_directions

    @staticmethod
    def get_flight_dates(post_tree):
        """
        This staticmethod takes an element tree (DOM)
        and returns an array of flight dates.
        """
        flight_date = post_tree.xpath(
            "//td[@class = 'flight-date']/text()")
        flight_dates = [flight_date[_] +
                        ', ' +
                        flight_date[_ + 1]
                        for _ in range(len(flight_date))
                        if _ % 2 == 0]
        return flight_dates

    @staticmethod
    def get_flight_numbers(post_tree):
        """
        This staticmethod takes an element tree (DOM)
        and returns an array of flight numbers.
        """
        flight_number = post_tree.xpath(
            "//td[@class = 'flight-number']//"
            "span/text()")
        flight_class = post_tree.xpath(
            "//td[@class = 'flight-number']/"
            "text()")
        flight_class = [
            flight_class[_].strip()
            for _ in range(len(flight_class))
            if _ % 2 == 1]
        flight_numbers = list(zip(
            flight_number,
            flight_class))
        return flight_numbers

    @staticmethod
    def get_flight_time(post_tree):
        """
        This staticmethod takes an element tree (DOM)
        and returns an array of depart times.
        """
        depart_time = post_tree.xpath(
            "//td[@class = 'flight-time']//"
            "span[@class = 'leaving']/text()")
        arrive_time = post_tree.xpath(
            "//td[@class = 'flight-time']//"
            "span[@class = 'landing']/text()")
        time_list = list(zip(depart_time,
                             arrive_time))
        return time_list

    @staticmethod
    def get_flight_notes(post_tree):
        """
        This staticmethod takes an element tree (DOM)
        and returns an array of notes.
        """
        flight_notes = post_tree.xpath(
            "//td[@class = 'flight-notes']//"
            "span[@class = 'equipment-type']/text()")
        return flight_notes

    @staticmethod
    def get_total_cost(post_tree):
        """
        This staticmethod takes an element tree (DOM)
        and returns flight total cost.
        """
        total_cost = post_tree.xpath(
            "//div[@class = 'pnr_total']//"
            "h1/text()")[0]
        total_cost = total_cost.split(': ')[1]
        return total_cost

    @staticmethod
    def get_fare_type(post_tree):
        """
        This staticmethod takes an element tree (DOM)
        and returns an array of fare types.
        """
        fare_type = post_tree.xpath(
            "//td[@class = 'fare-type']//"
            "span[@class = 'fare-normal']/text()")
        return fare_type

    def get_flight_info_data_element(self, tree_post):
        """
        This method collects data from one of the trips
        combinations into the dictionary
        """
        flight_info_head_list = [
            'Date', 'Depart times', 'Arrive time',
            'Flight number', 'Flight class', 'Notes',
            'Fare type', 'Total cost']
        directions = self.get_flight_directions(tree_post)
        dates = self.get_flight_dates(tree_post)
        flight_times = self.get_flight_time(tree_post)
        flight_numbers = self.get_flight_numbers(tree_post)
        flight_notes = self.get_flight_notes(tree_post)
        fare_type = self.get_fare_type(tree_post)
        total_cost = self.get_total_cost(tree_post)
        directions_dict = dict()
        if len(directions) >= 1:
            for _ in range(len(directions)):
                info_values_list = [dates[_],
                                    flight_times[_][0],
                                    flight_times[_][1],
                                    flight_numbers[_][0],
                                    flight_numbers[_][1],
                                    flight_notes[_],
                                    fare_type[_],
                                    total_cost]
                info_dict = dict(zip(flight_info_head_list,
                                     info_values_list))
                directions_dict[directions[_]] = info_dict
        return directions_dict

    def get_flight_info_data(self):
        """
        This method returns an array of elements (type-dictionary),
        according to the number of combinations of flights generated
        by the get_trip_data_list() function.
        """
        flight_list = []
        trees_post = self.get_trees_post_list()
        for tree_post in trees_post:
            data_flight = self.get_flight_info_data_element(tree_post)
            flight_list.append(data_flight)
        return flight_list
