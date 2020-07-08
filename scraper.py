# from command_args import args

# TODO: try to find better address

# SLEEP_FACTOR = args.sleep_factor

from selenium import webdriver  # allows us to open a browser and do the navigation
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time
import constants as cst
import command_args
from dateutil.relativedelta import relativedelta
from datetime import date
from job import Job
from company import Company


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

    def set_search_keywords(self):
        """
        This function allows to search a specific job title and location according to the
        input of the user on the command line
        """
        self.browser.get(cst.DEFAULT_URL)
        job_title = self.browser.find_element_by_id(cst.ID_JOB_TITLE_KW)
        job_title.clear()  # clear if something is already written
        job_title.send_keys(command_args.args.job_title)

        location = self.browser.find_element_by_id(cst.ID_JOB_LOCATION_KW)
        location.clear()  # clear if something is already written
        location.send_keys(command_args.args.job_location)

        try:
            # Close pop up
            pop_up = self.browser.find_element_by_xpath(cst.POP_UP_XPATH)
            pop_up.click()
        except NoSuchElementException:
            pass

        # Click on search button
        search_button = self.browser.find_element_by_id(cst.ID_SEARCH_BUTTON)
        search_button.click()

        time.sleep(cst.SLEEP_TIME)

    def get_num_pages(self):
        """
        Get the number of pages availables for a specific job and location
        :param current_url: string
        :return: integer
        """

        try:
            # take the number of all open positions in Israel over the site
            num_of_available_pages = self.browser.find_element_by_xpath(cst.NUM_PAGES_XPATH).text
            num_of_available_pages = int(num_of_available_pages.split(' ')[cst.LAST_ELEMENT])

        except NoSuchElementException:
            num_of_available_pages = cst.DEFAULT_NUM_PAGES  # default value
            print(cst.ERROR_NUM_PAGES)

        # time.sleep(SLEEP_TIME)

        return num_of_available_pages

    def catch_optional_text_value_by_xpath(self, x_path):
        """
        This function take an Xpath as an argument and try to catch the text. If not succeed return none
        :param x_path: constant
        :return: String or None
        """
        # TODO: not catching all the headquater & revenue
        try:
            text_value = self.browser.find_element_by_xpath(x_path).text
            if cst.UNKNOWN_INFO in text_value.lower():
                return None
            return text_value
        except NoSuchElementException:
            return None

    def convert_publication_date(self, publication_date):
        """
        Take a publication date and convert into format Year-Month-Day
        :param publication_date: string
        :return: string
        """
        # if the job has been published this day print the day of today
        if cst.HOUR in publication_date and cst.ALL_DAY not in publication_date:
            return date.today().strftime(cst.DATE_FORMAT)
        elif cst.HOUR in publication_date and cst.ALL_DAY in publication_date:
            return (date.today() - relativedelta(days=1)).strftime(cst.DATE_FORMAT)
        elif cst.DAY in publication_date:
            return (date.today() - relativedelta(
                days=int(publication_date.split(cst.DAY)[cst.FIRST_ELEMENT]))).strftime(
                cst.DATE_FORMAT)
        elif cst.MONTH in publication_date:
            return (date.today() - relativedelta(
                months=int(publication_date.split(cst.MONTH)[cst.FIRST_ELEMENT]))).strftime(
                cst.DATE_FORMAT)
        # else:
        #    return None

    def catch_mandatory_data_and_rating(self, button_job):  # TODO: not sure about the loop
        """
        Collect all the mandatory information on the website
        """
        time.sleep(cst.SLEEP_TIME)
        collect_mandatory = False
        while not collect_mandatory:
            # click the job button
            button_job.click()
            try:
                # Catch the publication date
                job_publication_date = self.browser.find_element_by_xpath(cst.PUBLICATION_DATE_XPATH).text
                time.sleep(cst.SLEEP_TIME)

                # Collect Company Name from a post
                company_name = self.browser.find_element_by_xpath(cst.COMPANY_NAME_XPATH).text

                # Collect Job Title from a post
                job_title = self.browser.find_element_by_xpath(cst.JOB_TITLE_XPATH).text

                # Collect Job Location from a post
                job_location = self.browser.find_element_by_xpath(cst.JOB_LOCATION_XPATH).text

                # Collect Job Description
                job_description = self.browser.find_element_by_xpath(cst.JOB_DESCRIPTION_XPATH).text

                # call function to convert publication date
                job_publication_date = self.convert_publication_date(job_publication_date)

                # Sometimes, company name and rating are join, we need to split them into Company Name and Rating
                if '\n' in company_name:  # We have a rating
                    # TODO: Cheack its float
                    company_rating = company_name.split('\n')[cst.SECOND_ELEMENT]
                    company_name = company_name.split('\n')[cst.FIRST_ELEMENT]
                else:  # No rating
                    company_rating = None

                # finish collect mandatory fields + rating if the company has in the name
                collect_mandatory = True
                job = Job(job_title, job_description, job_location, job_publication_date, company_name)
                company = Company(company_name, company_rating)
                return job, company

            except NoSuchElementException:
                # button_job.click() #TODO: check if its not succeed to load we need to click again
                time.sleep(cst.SLEEP_TIME)

    def catch_optional_data(self, company):
        """
        Catch all the optional information of a company
        :param company: string
        """
        # TODO: Check if value = Unknown put None
        # Collect optional information
        try:
            # Click on company in the hyper details
            self.browser.find_element_by_xpath(cst.OVERVIEW_XPATH).click()

            time.sleep(cst.SLEEP_TIME)

            # Catch company size information
            company.set_company_size(self.catch_optional_text_value_by_xpath(cst.COMPANY_SIZE_XPATH))
            # Catch founded year of company
            # TODO: check that it a number
            company.set_company_founded(self.catch_optional_text_value_by_xpath(cst.COMPANY_FOUNDED_XPATH))
            # Catch company industry
            company.set_company_industry(self.catch_optional_text_value_by_xpath(cst.COMPANY_INDUSTRY_XPATH))
            # Catch company sector
            company.set_company_sector(self.catch_optional_text_value_by_xpath(cst.COMPANY_SECTOR_XPATH))
            # Catch company type
            company_type = self.catch_optional_text_value_by_xpath(cst.COMPANY_TYPE_XPATH)
            if company_type is not None and '-' in company_type:
                company_type = company_type.split('-')[cst.SECOND_ELEMENT].strip()
                company.set_company_type(company_type)
            else:
                company.set_company_type(company_type)

            # Catch company revenue
            company.set_company_revenue(self.catch_optional_text_value_by_xpath(cst.COMPANY_REVENUE_XPATH))
            # Catch company headquarters
            company.set_company_headquarters(self.catch_optional_text_value_by_xpath(cst.COMPANY_HEADQUARTER_XPATH))

            # TODO: Fix competitors problem
            # Catch competitors and convert to list
            competitors = self.catch_optional_text_value_by_xpath(cst.COMPANY_COMPETITORS_XPATH)
            if competitors is not None and ',' in competitors:
                competitors = competitors.split(',')

            # print(f'competitors: {competitors}')
            # TODO: Check if it put list and append to previous one
            company.set_company_competitors(competitors)

        # If there is no overview page(company tab)
        except NoSuchElementException:
            print(cst.ERROR_OPTIONAL_DATA)
        finally:
            return company

    def collecting_data_from_page(self, database):
        """
        Collect all the data on a specific page
        """
        time.sleep(cst.SLEEP_TIME)
        try:
            pop_up = self.browser.find_element_by_xpath(cst.POP_UP_XPATH)
            pop_up.click()
        except NoSuchElementException:
            pass

        try:
            self.browser.find_element_by_xpath(cst.SELECTED_XPATH).click()
        except ElementClickInterceptedException:  # NoSuchElementException TODO: check the error
            pass

        time.sleep(cst.SLEEP_TIME)

        # Take all the buttons of each job in this page we want to click on
        job_click_button = self.browser.find_elements_by_xpath(cst.JOB_CLICK_BUTTON_XPATH)

        try:
            pop_up = self.browser.find_element_by_xpath(cst.POP_UP_XPATH)
            pop_up.click()
        except NoSuchElementException:
            pass

        for button_job in job_click_button:
            # start collect job data
            job, company = self.catch_mandatory_data_and_rating(button_job)
            company = self.catch_optional_data(company)
            database.insert_company(company)
            database.insert_job(job)
        database.insert_company(flag_finish_page=True)
        database.insert_job(flag_finish_page=True)

        # TODO: deal next page bug
        try:
            next_button = self.browser.find_element_by_xpath(cst.NEXT_XPATH)
            next_button.click()
        except NoSuchElementException:
            print(cst.ERROR_NEXT)
        time.sleep(cst.SLEEP_TIME)
        # self.browser.quit()

