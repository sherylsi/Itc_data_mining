"""
This class create an instance of job post with all the information.
Authors: May Steinfeld & Sheryl Sitruk
"""


class Job:
    def __init__(self, job_title, job_description, job_location, job_publication_date, company_name):
        """
        constructor
        :param job_title: string
        :param job_description: string
        :param job_location: string
        :param job_publication_date: date
        :param company_name: string
        """
        self.job_title = job_title
        self.job_description = job_description
        self.job_location = job_location
        self.job_publication_date = job_publication_date
        self.company_name = company_name

    def get_title(self):
        """
        get job title
        :return: string
        """
        return self.job_title

    def set_title(self, value):
        """
        set job title
        :param value: string
        :return:
        """
        self.job_title = value

    def get_description(self):
        """
        get job description
        :return: string
        """
        return self.job_description

    def set_description(self, value):
        """
        set job description
        :param value: string
        :return:
        """
        self.job_description = value

    def get_location(self):
        """
        get job location
        :return: string
        """
        return self.job_location

    def set_publication_date(self, value):
        """
        set job publication date
        :param value: date
        :return:
        """
        self.job_publication_date = value

    def get_company_name(self):
        """
        get company name
        :return: string
        """
        return self.company_name

    def set_company_name(self, value):
        """
        set company name
        :param value: string
        :return:
        """
        self.company_name = value