from selenium import webdriver  # allows us to open a browser and do the navigation
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import constants as cst
import command_args


class Scraper:
    """
       Contains functions related to scraping the website.
       """

    def __init__(self):
        """
        Sets up the default URL.
        """
        self.browser = webdriver.Firefox(executable_path=command_args.args.driver_path)
        self.browser.maximize_window()

    def catch_optional_text_value_by_xpath(self, x_path):
        """
        This function take an Xpath as an argument and try to catch the text. If not succeed return none
        :param x_path: constant
        :return: String or None
        """
        try:
            text_value = self.browser.find_element_by_xpath(x_path).text
            # if the optional data unknown put None
            if cst.UNKNOWN_INFO in text_value.lower():
                return None
            return text_value
        except NoSuchElementException:
            return None

    def convert_company_founded_year(self, company_founded):
        """
        The function get string and convert it to int
        :param company_founded: string
        :return: int or None
        """
        if company_founded is not None:
            try:
                company_founded = int(company_founded)
            except ValueError:
                company_founded = None
            finally:
                return company_founded
        else:
            return company_founded
