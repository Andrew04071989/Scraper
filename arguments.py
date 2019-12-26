"""
This module generates arguments and a description for them.
This module also checks the correctness
of user input of argument values.
"""
import argparse
from is_valid_input import IsValid


class Arguments:
    """
    This class generates arguments and a description for them.
    This module also checks the correctness
    of user input of argument values.
    """
    def __init__(self, iata_from, iata_to,
                 dep_date, ret_date):
        self.iata_from = iata_from
        self.iata_to = iata_to
        self.dep_date = dep_date
        self.ret_date = ret_date
        self.is_val = IsValid(
            self.iata_from, self.iata_to,
            self.dep_date, self.ret_date)
        self.is_valid_input = \
            self.is_val.is_ret_date_according_to_default()
        self.iata_from = self.is_val.from_city
        self.iata_to = self.is_val.to_city
        self.dep_date = self.is_val.depart_date
        self.ret_date = self.is_val.return_date

    def get_parser(self):
        """
        This function add arguments to the arguments parser.
        """
        parser = argparse.ArgumentParser(
            description='Flight parameters')
        parser.add_argument(
            'IATA_FROM', action='store_const', const=self.iata_from,
            help='Departure city. This parameter corresponds '
                 'to the IATA code of the city of departure.')
        parser.add_argument(
            'IATA_TO', action='store_const', const=self.iata_to,
            help='Arrival city. This parameter corresponds '
                 'to the IATA code of the city of arrival.')
        parser.add_argument(
            'DEP_DATE', action='store_const',
            const=self.dep_date,
            help='Departure date. Date of departure '
                 'in YYYY-MM-DD format.')
        parser.add_argument(
            '--RET_DATE', action='store_const', const=self.ret_date,
            default='',
            help='Return date. Return date '
                 'in YYYY-MM-DD format.')
        return parser

    def parse_arguments(self):
        """
        This function checks the correctness
        of user input of argument values and
        returns arguments parser.
        """
        if False not in self.is_valid_input.values():
            parser = self.get_parser()
            args = parser.parse_args(['--RET_DATE'])
            return args

    def print_help_info(self):
        """
        This function checks the correctness
        of user input of argument values and
        prints help for the arguments.
        """
        if False not in self.is_valid_input.values():
            parser = self.get_parser()
            return parser.print_help()
