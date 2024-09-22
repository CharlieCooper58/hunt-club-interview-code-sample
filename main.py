import pandas as pd
import gcsfs
from google.cloud import storage

df = pd.read_csv('gs://data_engineering_tech_assessment/processed_fake_candidate_data.csv')


def get_info(request):
    #https://stackoverflow.com/questions/52233949/passing-variables-to-google-cloud-functions
    request_json = request.get_json(silent=True)
    request_args = request.args
    #if request_json and 'task' in request_json:
    #    task = request_json['task']
    if request_args and 'task' in request_args:
        task = request_args['task']
        # Only accept valid values of task to avoid user frustration
        if not task in ['num_cand', 'most_common', 'salaries', 'num_incomplete']:
            return "Error: task must be one of: num_cand, most_common, salaries, num_incomplete"

    else:
        task = 'num_cand'

    #if request_json and 'col' in request_json:
    #    col = request_json['col']
    if request_args and 'col' in request_args:
        col = request_args['col']
        #Only accept valid values of col to avoid user frustration
        if not col in ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'company_name', 'job_title', 'salary', 'salary_ranges', 'location_raw']:
            return "Error: col must be one of: id, first_name, last_name, full_name, email, phone, company_name, job_title, salary, salary_ranges, location_raw"
    else:
        col = None

    if(task == "num_cand"):
        return "There are {} candidates in total".format(format(df.shape[0]))
    elif(task == "num_incomplete"):
        #Number of rows minus number of rows with null values
        if(col == None):
            return "{} candidates have missing information of some kind.".format((df.shape[0] - df.dropna().shape[0]))
        #Allow the user to find the number of null values in whatever column
        elif col in df.columns.values.tolist():
            return "{} candidates are missing information about {}".format(df[col].isnull().sum(), col)
        else:
            return "Error: specified column does not exist."
    elif(task == "salaries"):
        #Get all salary info
        median = df['salary'].median(skipna=True)
        mean = df['salary'].mean(skipna=True)
        std = df['salary'].std(skipna=True)
        return "The median salary is {:.2f}, while the mean salary is {:.2f} with standard deviation {:.2f}".format(median, mean, std)
    elif(task == "most_common"):
        #Get the mode of columns where there's mode-able data
        #It doesn't seem that useful to find the most common last name, for example
        if(col == None):
            return str(df['job_title'].mode())
        elif(col == 'job_title'):
            #The job titles are stored in such a way that the mode is super skewed
            #I can't really train my script to decide which jobs are "equivalent" right now
            #So I'm redacting anything after the comma in a job title, since that tends to be where the redundancies are piling up
            temp = []
            for i in df['job_title'].str.split(',').str[0]:
                temp.append(i)
            temp = pd.DataFrame(temp)
            return "Most common job title(s): \n {}".format(temp.mode())
        elif(col in ['company_name', 'salary', 'salary_ranges']):
            return "Most common {}: \n {}".format(col, str(df[col].mode()))
        else:
            return "This column will not have a useable mode."
    else:
        return "Command not recognized, or no command given.  Be sure to specify ?task=<> at the end of the URL.  Valid task options: num_cand, num_incomplete, salaries, most_common."
