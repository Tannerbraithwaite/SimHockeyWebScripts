import pandas as pd
import numpy as np
import math
import statistics

dataset = pd.read_csv('/Users/tannerbraithwaite/github/python_scripts/SimHockeyscripts/CCHL Draft Central - Available Players.csv')

n=0
total_overall=0
overall_int_list=[]
for overall in dataset['Overall']:
    if math.isnan(overall):
        continue
    else:
        total_overall+=int(overall)
        n+=1
        overall_int_list.append(int(overall))
average_overall = total_overall/n



name_list=[]
for name in dataset['Name']:
    if pd.isnull(name):
        continue
    else:

        name_list.append(name)

position_list=[]
for position in dataset['Position']:
    if pd.isnull(position):
        continue
    else:
        position_list.append(position)


average_overall = total_overall/n


total_age=0
age_int_list=[]
for age in dataset['Age']:
    if math.isnan(age):
        continue
    else:
        total_age+=int(age)
        age_int_list.append(int(age))


average_age = total_age/n
total_contract=0

salary_int_list=[]
for contract in dataset['Salary']:
    if type(contract)!=float:
        salary = contract[3:].replace(',','')
        total_contract+=int(salary)
        salary_int_list.append(int(salary))
    else:
        continue
average_contract = total_contract/n

standard_dev_salary=statistics.pstdev(salary_int_list)
standard_dev_age=statistics.pstdev(age_int_list)
standard_dev_overall=statistics.pstdev(overall_int_list)

list_ammalgamated_values=[]
for i in range(0,len(position_list)):
    value = -.25*(salary_int_list[i] - average_contract)/standard_dev_salary -.25*(age_int_list[i] - average_age)/standard_dev_age + .5*(overall_int_list[i] - average_overall)/standard_dev_overall
    list_ammalgamated_values.append(value)


dataset['weighted_value'] = list_ammalgamated_values

dataset.to_csv('CCHL Draft Central copy.csv',header=True,index=False)
