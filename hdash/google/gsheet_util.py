import os
import logging
import pygsheets
from datetime import datetime


class GoogleSheetUtil:
    PROJECT_SPREADSHEET_KEY = "1yoNxJ8sXDac3RRLpe3qTj7_ZQtVZzWgAUq_D3k4Ppj8"
    HDASH_SPREADSHEET_KEY = "1XuHG_2WsODBEKcxDRbwV7qR2avdzaln8FWINKAJSumg"
    HEADER_LIST = [
        "FASTQ",
        "BAM",
        "IMAGE",
        "MATRIX",
        "OTHER",
        "META",
    ]

    def __init__(self):
        service_account_path = self._get_service_account_path()
        logging.info("Authenticating with Google")
        logging.info("Using service account:  %s" % service_account_path)
        client = pygsheets.authorize(service_file=service_account_path)
        logging.info("Success authenticating with Google")

        sh = client.open_by_key(GoogleSheetUtil.PROJECT_SPREADSHEET_KEY)
        project_sheet = sh.sheet1
        self.project_df = project_sheet.get_as_df()

        sh = client.open_by_key(GoogleSheetUtil.HDASH_SPREADSHEET_KEY)
        self.wks1 = sh.worksheet_by_title("File Count")
        self.wks2 = sh.worksheet_by_title("File Size")
        logging.info("Opening HDash Sheet")

    def write(self, p_list):
        # Output headers
        header_list = []
        header_list.append("ATLAS")
        for project in p_list:
            project_name = self._truncate_project_name(project.name)
            for header in GoogleSheetUtil.HEADER_LIST:
                header_list.append(project_name)
        self.wks1.update_row(index=1, values=header_list)
        self.wks2.update_row(index=1, values=header_list)

        header_list = []
        header_list.append("CATEGORY")
        for project in p_list:
            for header in GoogleSheetUtil.HEADER_LIST:
                header_list.append(header)
        self.wks1.update_row(index=2, values=header_list)
        self.wks2.update_row(index=1, values=header_list)

        header_list = []
        header_list.append("TIMESTAMP")
        for project in p_list:
            project_name = self._truncate_project_name(project.name)
            for header in GoogleSheetUtil.HEADER_LIST:
                label = project_name + "_" + header
                header_list.append(label)
        header_list.append("TOTAL")
        logging.info("Setting headers")
        self.wks1.update_row(index=3, values=header_list)
        self.wks2.update_row(index=1, values=header_list)

        # Output File Count Data
        value_list = []
        value_list.append(datetime.now())
        total_num_files = 0
        for project in p_list:
            value_list.append(project.num_fastq)
            value_list.append(project.num_bam)
            value_list.append(project.num_image)
            value_list.append(project.num_matrix)
            value_list.append(project.num_other)
            value_list.append(project.num_meta)
            total_num_files += project.num_fastq
            total_num_files += project.num_bam
            total_num_files += project.num_image
            total_num_files += project.num_matrix
            total_num_files += project.num_other
            total_num_files += project.num_other
            total_num_files += project.num_meta
        value_list.append(total_num_files)
        self.wks1.append_table(value_list)

        # Output File Size Data
        value_list = []
        value_list.append(datetime.now())
        total_size = 0
        for project in p_list:
            value_list.append(project.size_fastq)
            value_list.append(project.size_bam)
            value_list.append(project.size_image)
            value_list.append(project.size_matrix)
            value_list.append(project.size_other)
            value_list.append(0)
            total_size += project.get_total_file_size()
        value_list.append(total_size)
        self.wks2.append_table(value_list)

    def _get_service_account_path(self):
        service_account_path = os.getenv("HDASH_SERVICE_ACCOUNT")
        if service_account_path is None:
            raise EnvironmentError("HDASH_SERVICE_ACCOUNT is not set.")
        return service_account_path

    def _truncate_project_name(self, project_name):
        project_name = project_name.replace("HTAN ", "")
        project_name = project_name.replace("PILOT - ", "")
        project_name = project_name.upper()
        return project_name
