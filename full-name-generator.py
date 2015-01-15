from scipy import stats
from random import randint
import os
import pandas as pd

data_directory = r''
data_file = os.path.join(data_directory, 'names.csv')

names_data = pd.read_csv(data_file)

sample_size = 1000000

xk = range(len(names_data['prenom']))
pk = names_data['frequence_prenom']
custm = stats.rv_discrete(name='custm', values=(xk, pk))

xk2 = range(len(names_data['nom']))
pk2 = names_data['frequence_nom']
custm2 = stats.rv_discrete(name='custm', values=(xk2, pk2))

R = custm.rvs(size = sample_size)
R2 = custm2.rvs(size = sample_size)

freq_prenom = names_data['prenom'][R]
freq_nom = names_data['nom'][R2]

freq_nom = freq_nom.reset_index()
freq_prenom = freq_prenom.reset_index()

full_name = pd.concat([freq_prenom['prenom'], freq_nom['nom']], axis = 1)
full_name['status'] = 'normal'

for index, row in full_name.iterrows():
    dice = randint(1, 10)
    if dice == 10:
        full_name['prenom'][index],full_name['nom'][index] = full_name['nom'][index], full_name['prenom'][index]
        full_name['status'][index] = 'reversed'

        data_out = os.path.join(data_directory, 'gen_names.csv')
full_name.to_csv(data_out, index = False)

print full_name['status'].value_counts()
