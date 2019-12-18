""" This module is responsible for displaying flight information. """
from is_valid_input import IsValid
from get_flight_data import FlightData


class StartScraping:
    """ This class is responsible for
    displaying flight information. """
    def __init__(self, from_city, to_city,
                 depart_date, return_date):
        self.url = "https://www.airblue.com/" \
                   "bookings/flight_selection.aspx"
        self.from_city = from_city
        self.to_city = to_city
        self.depart_date = depart_date
        self.return_date = return_date
        self.is_val = IsValid(
            self.from_city, self.to_city,
            self.depart_date, self.return_date)
        self.is_valid_input = \
            self.is_val.is_ret_date_according_to_default()
        self.from_city = self.is_val.from_city
        self.to_city = self.is_val.to_city
        self.depart_date = self.is_val.depart_date
        self.return_date = self.is_val.return_date
        self.fl_data = FlightData(
            self.from_city, self.to_city,
            self.depart_date, self.return_date)

    def print_flight_info(self):
        """ This is a method that outputs
        flight information in a readable format.
        """
        if False not in self.is_valid_input.values():
            option_counter = 0
            flight_data = self.fl_data.get_flight_info_data()
            for flight in flight_data:
                option_counter += 1
                print('__________\nOption #{}:\n__________'.
                      format(str(option_counter)))
                direction_counter = 0
                for direction in flight:
                    if flight != {}:
                        direction_counter += 1
                        if direction_counter == 1:
                            print('FORWARD FLIGHT DIRECTION:\n')
                        elif direction_counter == 2:
                            print('REVERS FLIGHT DIRECTION:\n')
                        print('Direction: {}'.format(direction))
                        for item in flight[direction]:
                            print('{}: {}'.format(
                                item,
                                flight[direction][item]))

                    else:
                        print('Flights are not available')
                    print('\n')


if __name__ == "__main__":
    IATA_FROM = input('Enter depart city: ')
    IATA_TO = input('Enter arrive city: ')
    DEP_DATE = input('Enter depart date (YYYY-MM-DD): ')
    RET_DATE = input("Enter return date (YYYY-MM-DD) or don't: ")
    # Parameters for validation of input data:
    # IATA_FROM = 'KHH'
    # IATA_TO = 'ISD'
    # DEP_DATE = 'K020-01-21'
    # RET_DATE = '20200124'
    START_SCRAP = StartScraping(IATA_FROM, IATA_TO, DEP_DATE, RET_DATE)
    START_SCRAP.print_flight_info()
