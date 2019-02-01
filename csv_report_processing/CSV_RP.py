from datetime import datetime
import pycountry
import csv
import sys


def csv_read(path_to_file):
    """
    :param path_to_file: Path to csv file
    :return: A list containing data from the csv file
    """
    reports_list = []
    try:
        with open(path_to_file, newline='') as csvfile:
            reports = csv.reader(csvfile)
            for row in reports:
                reports_list.append(row)
        return reports_list
    except FileNotFoundError as error:
        print(error.__str__(), file=sys.stderr)


def csv_write(new_file_name, line):
    """
    Adds new line to csv file or creates new file.

    :param new_file_name: The name of the file in which the data will be saved
    :param line: list of data which creates new line
    :return: None
    """
    with open(new_file_name, 'a') as csvfile:
        report = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        report.writerow(line)


def parse_date(date_string):
    """
    Changes date format

    :param date_string: Date as string in format MM/DD/YYYY
    :return: date string in format YYYY-MM-DD
    """
    parsed_date = datetime.strptime(date_string, '%m/%d/%Y').strftime('%Y-%m-%d')
    return parsed_date


def parse_state_to_country_code(state_name):
    """
    Finds three letter country code by state name using pycountry library

    :param state_name: Name of state as string
    :return: three letter country code (or XXX for unknown states)
    """
    try:
        # find a subdivision by name and get the country's three-letter code
        country_code = pycountry.subdivisions.lookup(state_name).country.alpha_3
    except LookupError as error:
        country_code = 'XXX'
        print(error.__str__(), file=sys.stderr)
    return country_code


def count_clicks(number_of_impressions, ctr):
    """
    Counts number of clicks (rounded, assuming the CTR is exact)

    :param number_of_impressions: number of impressions as string
    :param ctr: Click-through rate as string
    :return: number of clicks
    """
    number_of_impressions = int(number_of_impressions)
    ctr = float(ctr.rstrip("%"))
    number_of_clicks = number_of_impressions * (ctr / 100)
    return int(round(number_of_clicks))


def main(path_to_file):
    """
    Reads a CSV file. Creates a new CSV file with a report aggregated by date and country.

    :param path_to_file:
    :return: None
    """
    data = (csv_read(path_to_file))
    data_list = []
    try:
        # add all needed data to new list
        for line in data:
            data_list.append([parse_date(line[0]), parse_state_to_country_code(line[1]), line[2],
                              count_clicks(line[2], line[3])])
    except TypeError as error:
        print(error.__str__(), file=sys.stderr)
    # sort data_list lexicographically by date and by the country code
    data_list.sort(key=lambda row: (row[0], row[1]))
    for line in data_list:
        csv_write("new_report.csv", line)


if __name__ == "__main__":
    main("report.csv")
