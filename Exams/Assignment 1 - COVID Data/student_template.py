import sys

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###
us_counties_data = parse_nyt_data('../../data/covid/us-counties.csv')
harrisonburg_data = []
harrisonburg_positive_data = []
harrisonburg_new_cases_data = []
harrisonburg_week_average_data = []
for entry in us_counties_data:
    if entry[1] == 'Rockingham' and entry[2] == 'Virginia':
        harrisonburg_data.append(entry)
        if entry[4] > 0:
            harrisonburg_positive_data.append(entry)
for i in (range(len(harrisonburg_data))):
    if i == 0:
        harrisonburg_new_cases_data.append(harrisonburg_data[i][4])
    else:
        harrisonburg_new_cases_data.append((harrisonburg_data[i][4]-harrisonburg_data[i-1][4]))

for i in range(len(harrisonburg_new_cases_data)-6):
    harrisonburg_week_average_data.append(sum(harrisonburg_new_cases_data[i:i+7])/7)

# Question 1: Date of the first case in Harrisonburg, VA
print("Harrisonburg First Case Date: " + str(harrisonburg_positive_data[0][0]))
# Question 2: Worst day for new cases in Harrisonburg, VA
print("Worst Day for New Cases in Harrisonburg: " + str(harrisonburg_data[harrisonburg_new_cases_data.index(max(harrisonburg_new_cases_data))][0]))
# Question 3: 7-day maximum for new cases in Harrisonburg, VA
print("7-Day Maximum for New Cases in Harrisonburg: ",str(harrisonburg_data[harrisonburg_week_average_data.index(max(harrisonburg_week_average_data))][0])," to ",str(harrisonburg_data[harrisonburg_week_average_data.index(max(harrisonburg_week_average_data))+6][0]))