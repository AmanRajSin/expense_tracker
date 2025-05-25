import pandas as pd

expenses = pd.json_normalize(data['expenses'])
print(expenses[['description', 'cost', 'date', 'created_by.first_name']])
