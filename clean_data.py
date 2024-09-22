import numpy as np
import pandas as pd
import numpy
#all of the null values that were passed.  0 is included as an int and a string to account for how its datatype changes in different columns
null_options = ["", numpy.nan, 0, "0", "null"]

def clean(filename):
    dat = pd.read_csv(filename,header = 0, names = ['id', 'first_name', 'last_name', 'email', 'phone', 'company_name', 'job_title', 'salary', 'location_raw'])
    dat = fix_null(dat)
    #Concatenate first and last names
    dat['full_name'] = dat.first_name.str.cat(dat.last_name, sep = " ")
    #To bin salaries, I decided to use standard deviation
    mean = dat['salary'].mean()
    std = dat['salary'].std()
    bins = [mean - std, mean - 0.5*std, mean + 0.5*std, mean + std]
    #I was getting some weird erros when I tried to apply the function to the whole column, so I'll do it one row at a time
    #If I have time later I'll com eback and try to fix it up a bit
    salary_ranges = []
    for sal in dat['salary']:
        salary_ranges.append(bin_salaries(sal, bins))
    dat['salary_ranges'] = salary_ranges
    #Make it pretty
    #https://stackoverflow.com/questions/13148429/how-to-change-the-order-of-dataframe-columns
    dat = dat[['id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
       'company_name', 'job_title', 'salary', 'salary_ranges', 'location_raw'
       ]]
    return dat

def fix_null(data):
    #Replace all null values with None
    #I'm using None right now because it doesn't mess up my other functions, and python will consistently read it out as nan
    for bad in null_options:
        data = data.replace(bad, None)
    return data
def bin_salaries(num, bins):
    #Bin salaries using pre-defined bins
    if(num == None):
        return None
    elif(num < bins[0]):
        return "Very Low"
    elif(num > bins[0] and num < bins[1]):
        return "Low"
    elif(num > bins[1] and num < bins[2]):
        return "Medium"
    elif(num > bins[2] and num < bins[3]):
        return "High"
    else:
        return "Very high"
df = clean("C:/Users/ccoop/Downloads/fake_candidate_data.csv")
df.to_csv('C:/Users/ccoop/Downloads/processed_fake_candidate_data.csv')
