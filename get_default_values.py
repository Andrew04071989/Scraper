"""
This module is responsible for
extracting the default data.
"""
from get_tree import Tree


class DefaultValues(object):
    """
    This class generates lists of all parameters
    allowed for input (type-string).
    """
    def __init__(self, url):
        self.url = url
        self.tree = Tree()
        self.tree_get = self.tree.tree_method_get(self.url)

    def get_depart_months_years_values(self):
        """
        This method generates a list of all
        allowed year-month(type - string)
        values of departure dates.
        """
        default_months_years = self.tree_get.xpath(
            '//select[@name = "AM"]//'
            'option/@value')
        return default_months_years

    def get_depart_days_values(self):
        """
        This method generates a list of all
        allowed days values(type - string)
        of departure dates.
        """
        default_days = self.tree_get.xpath(
            '//select[@name = "AD"]//'
            'option/text()')
        return default_days

    def get_return_months_years_values(self):
        """
        This method generates a list of all
        allowed year-month(type - string)
        values of return dates.
        """
        default_months_years = self.tree_get.xpath(
            '//select[@name = "RM"]//'
            'option/@value')
        return default_months_years

    def get_return_days_values(self):
        """
        This method generates a list of all
        allowed days values(type - string)
        of return dates.
        """
        default_days = self.tree_get.xpath(
            '//select[@name = "RD"]//'
            'option/text()')
        return default_days

    def get_depart_city_values(self):
        """
        This method generates a list of all
        allowed departure cities(type-string).
        """
        default_dep_city = self.tree_get.xpath(
            '//select[@name = "DC"]//'
            'option/@value')
        return default_dep_city

    def get_arrive_city_values(self, depart_city):
        """
        This method generates a list of all
        allowed arrival cities(type-string).
        """
        default_arr_city = self.tree_get.xpath(
            '//select[@name = "AC"]//'
            'option[@value = "{}"]/'
            '@data-targets'.
            format(depart_city))
        if default_arr_city != []:
            default_res = default_arr_city[0].split(',')
        else:
            default_res = default_arr_city
        return default_res
