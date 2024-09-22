This project was made for my technical interview at Hunt Club.  I was given a CSV of fake employment history data and tasked to clean it and add a column that tracked employees' salary ranges (the interpretation of which was left up to me).  I was then tasked to create a REST API to pull information about those candidates including the number of candidates, the number of candidates with incomplete data (with an optional filter for which column's data was missing), statistics about candidates' salaries, and the most common value of a given column.

The CSV is lost and the endpoint is defunct, but the code still works and could easily be brought back up and running with a new container.


Original README:

All the data is cleaned and stored in the bucket.  To use the function, see below:

Usage: https://us-central1-hc-data-tech-assessment-cooper.cloudfunctions.net/get_info?task=<task>&col=<col>
  
Values for task: 
  
  num_cand: returns the total number of candidates
  
  num_incomplete: returns the nubmer of candidates with missing data of any kind.  You can also specify a column to see how many candidates are missing data from that   column
  
  salaries: returns the mean, median, and standard deviation of candidate salaries
  
  most_common: returns the mode of the specified column (accepts job_title, company, salary, and salary_ranges).  For job_title it's a bit wonky, given more time I'd love to tear it apart and make it a bit more robust
  
Values for col: any column name works for num_incomplete, while most_common only accepts: job_title, company, salary, salary_ranges.  Otherwise, no value for col is necessary.
