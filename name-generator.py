from scipy import stats
from random import randint
import os
import pandas as pd

# Number of created names
sample_size = 10000

# Directory of the csv file containing first and last names
data_directory = r''
data_file = os.path.join(data_directory, 'names.csv')

# Read the data with pandas
names_data = pd.read_csv(data_file)

# Generate two dist discrete distributions from first and last names frequencies
point_first = range(len(names_data['first']))
proba_first = names_data['frequency_first']
dist_first = stats.rv_discrete(name='dist_first', values=(point_first, proba_first))

point_last = range(len(names_data['last']))
proba_last = names_data['frequency_last']
dist_last = stats.rv_discrete(name='dist_last', values=(point_last, proba_last))

# Create random names
generated_first = names_data['first'][dist_first.rvs(size = sample_size)]
generated_last = names_data['last'][dist_last.rvs(size = sample_size)]

# Stock them in a DataFrame
full_name = pd.DataFrame(index=range(sample_size), columns=['first','last','status'])
full_name['first'] = generated_first.reset_index()['first']
full_name['last'] = generated_last.reset_index()['last']
full_name['status'] = 'normal'

# Swap 1 name out of 10
for index, row in full_name.iterrows():
    dice = randint(1, 10)
    if dice == 10:
        full_name['first'][index],full_name['last'][index] = full_name['last'][index], full_name['first'][index]
        full_name['status'][index] = 'reversed'
        data_out = os.path.join(data_directory, 'generated_names.csv')
full_name.to_csv(data_out, index = False)

# Print the status of created names
print full_name['status'].value_counts()
