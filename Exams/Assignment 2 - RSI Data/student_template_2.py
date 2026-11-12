"""
CULMINATING ASSIGNMENT 2: RSI

Create a program which will provide answers to the tasks posed in the assignment description.

For this assignment, you will start from scratch with this blank template.
It is your reponsibility to include all necessary program components in this file.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.

The relevant data file is named "all_participant_data_rsi.csv" and is located in data > drop-jump.

All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""
import sys
import pandas as pd
import numpy as np
from scipy.stats import ttest_rel, norm, chisquare, t
import matplotlib
import matplotlib.pyplot as plt
import platform

## Function to read data from file path and then parse it into a list of tuples containing (participant, force_plate_rsi, accelerometer_rsi, percent_error)
def parse_rsi_data(file_path=''):
    data=[]
    ## Attempt to open the file, if their is no path, then give an error.
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)
    fin.readline()
    done = False

    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue
        ## Split the lines by commas and then put them in a tuple.
        (participant, force_plate_rsi, accelerometer_rsi, percent_error) = line.rstrip().split(",")

        ## Convert the values to floats for computation.
        try:
            entry = (participant, float(force_plate_rsi), float(accelerometer_rsi), float(percent_error))
        except ValueError:
            print('Invalid parse of ', entry)

        data.append(entry)

    return data
## Function for the paired t-test
def paired_t_test(data):
    ## Read the elements from the parsed data and put them in lists.
    force_plate_rsi = [element[1] for element in data]
    accelerometer_rsi = [element[2] for element in data]
    ## Use the scipy paired t-test that omits NaN values to compute the t-value and p-value.
    t_val, p_val = ttest_rel(force_plate_rsi, accelerometer_rsi,nan_policy='omit')
    return t_val, p_val

## Function to generate a plot and test the goodness of fit for the distribution.
def chi_gof_and_plot(datalist,num_bins=9):
    ##  Use the scipy norm.fit feature to find the fitted mean and deviation of the distribution.
    fitted_mean, fitted_std = norm.fit(datalist)
    ## Create the bins for the numpy histogram spanning 2 standard deviations on either side and make +/- infitie the size of the last bins.
    bins = np.r_[-np.inf, np.linspace(fitted_mean - 2 * fitted_std, fitted_mean + 2 * fitted_std, num_bins), np.inf]
    ## use the cumulative distribution function to find the expencted counts in each bin.
    cdf_values = norm.cdf(bins, loc=fitted_mean, scale=fitted_std)
    expected_counts = len(datalist) * np.diff(cdf_values)
    ## Find the observed counts in each bin using numpy histogram.
    observed_counts, _ = np.histogram(datalist, bins=bins)
    ## perform the chi-square test comparing the observed counts to the expected counts. There are two degress of freedom because their are two samples.
    chi_stat, p_value = chisquare(observed_counts, expected_counts, ddof=2)

    ## Plot the fitted curve over the matplotlib histogram of the data
    plt.hist(datalist, bins=num_bins, density=True, alpha=0.5, label='Observed Data', edgecolor='k')
    x = np.linspace(min(datalist), max(datalist), 100)
    plt.plot(x, norm.pdf(x, loc=fitted_mean, scale=fitted_std), linewidth=2, color='r', label='Fitted Normal Distribution')
    plt.title('Chi-Square Goodness-of-Fit Test')
    plt.xlabel('Accelerometer RSI Values')
    plt.ylabel('Counts')
    plt.show()
    return chi_stat, p_value

## Function that makes a dataframe for a specific participant and then finds the confidence intervals.
def Trialdf(data, participant, alpha):
    ## Define an empty list to be populated.
    Participant_data = []
    for entry in data:
        ## take the participant and trial and split them to find all trials for the specific person.
        participant_id = entry[0].split('_')[0]
        if participant_id == participant:
            ##if the participant matches, then append the entry to the list.
            Participant_data.append(entry)
    ## create a dataframe from pandas with the four columns from the RSI data.
    df = pd.DataFrame(Participant_data, columns=['Participant', 'Force Plate RSI', 'Accelerometer RSI', 'Percent Error'])
    ## use the t-interval test from scipy to find the intervals for both the force plate and accelerometer RSI values.
    ## The value at the end is how the standard error is calculated for sample means.
    FPint = t.interval(1-alpha, len(df)-1, np.mean(df['Force Plate RSI']), np.std(df['Force Plate RSI'], ddof=1)/np.sqrt(len(df)))
    Accint = t.interval(1-alpha, len(df)-1, np.mean(df['Accelerometer RSI']), np.std(df['Accelerometer RSI'], ddof=1)/np.sqrt(len(df)))
    return df, FPint, Accint

parsed = parse_rsi_data('../../data/drop-jump/all_participant_data_rsi.csv')
t_value, p_value1 = paired_t_test(parsed)
chi_stat, p_value2 = chi_gof_and_plot([element[2] for element in parsed], 9)
F_df, FPint, Accint = Trialdf(parsed, 'F', 0.05)

print(f"t-value: {t_value}, p-value: {p_value1}, null hypothesis rejected: {p_value1 < 0.05}, The null hypothesis is that both the means are the same and the alternative is that they differ significantly.")
if p_value2 < 0.05:
    print(f"chi-square test statistic: {chi_stat}, p-value: {p_value2}, null hypothesis rejected: {p_value2 < 0.05}, The normal fit is bad.")
else:
    print(f"chi-square test statistic: {chi_stat}, p-value: {p_value2}, null hypothesis rejected: {p_value2 < 0.05}, The normal fit is good.")

print(f"Dataframe for participant F:\n{F_df}\nForce Plate RSI 95% CI: {FPint}\nAccelerometer RSI 95% CI: {Accint}")

