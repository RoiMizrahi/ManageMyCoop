import csv
from datetime import date
import pandas as pd


#header = ['index','date', 'eggs_amount', 'broken_eggs', 'current_food', 'dead_chicken']


results = pd.read_csv('application/egg_posts/collecting.csv')
eggs = {
    'index':[len(results)+1],
    'date' :[date.today().strftime('%d-%m-%Y')],
    'eggs_amount':[1600],
    'broken_eggs':[12],
    'current_food':[350],
    'dead_chicken':[0],
    'user_id': []
          }
df = pd.DataFrame(eggs)
df.to_csv('application/egg_posts/collecting.csv', index=False, mode='a', header=False)

results = pd.read_csv('application/egg_posts/collecting.csv')

print("Number of lines present:-",len(results))
##############edit#######################

#df = pd.read_csv('application/egg_posts/collecting.csv', index_col='index')
# Set cell value at row '3' and column 'eggs_amount'
#df.loc[3, 'eggs_amount'] = 56
# Write DataFrame to CSV file
#df.to_csv('application/egg_posts/collecting.csv')
