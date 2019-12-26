""" This module is responsible for displaying flight information. """
from get_flight_data import FlightData
from arguments import Arguments


class StartScraping:
    """ This class is responsible for
    displaying flight information. """
    def __init__(self, from_city, to_city,
                 depart_date, return_date):
        self.from_city = from_city
        self.to_city = to_city
        self.depart_date = depart_date
        self.return_date = return_date
        self.url = "https://www.airblue.com/" \
                   "bookings/flight_selection.aspx"
        self.fl_data = FlightData(
            self.from_city, self.to_city,
            self.depart_date, self.return_date)

    def print_flight_info(self):
        """ This is a method that outputs
        flight information in a readable format.
        """
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


def main():
    """ The main() function that starts the scraper. """
    iata_from = input('Enter depart city: ')
    iata_to = input('Enter arrive city: ')
    dep_date = input('Enter depart date (YYYY-MM-DD): ')
    ret_date = input("Enter return date (YYYY-MM-DD) or don't: ")
    arg = Arguments(
        iata_from, iata_to,
        dep_date, ret_date)
    marker = False
    choice = input('Enter "1" for Search flight'
                   ' or "2" for Help: ')
    while marker is False:
        if choice == '1':
            args = arg.parse_arguments()
            start_scr = StartScraping(
                args.IATA_FROM, args.IATA_TO,
                args.DEP_DATE, args.RET_DATE)
            start_scr.print_flight_info()
            marker = True
        elif choice == '2':
            arg.print_help_info()
            marker = True
        else:
            choice = input("You didn't enter '1' or '2'. "
                           "Please re-enter: ")


if __name__ == '__main__':
    main()
