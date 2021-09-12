import sys
from datetime import datetime
import requests
import getpass
import pandas as pd

# Exception handling
def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)
sys.excepthook = show_exception_and_exit

# Set the request parameters
subdomain = input("Enter your Zendesk Subdomain (not full URL, but something such as your company name): ")
url = 'https://' + subdomain + '.zendesk.com/api/v2/help_center/en-us/articles.json?include=categories,sections&sort_by=title&sort_order=asc'

# Use Your Zendesk Support Sign-On Credentials
user = input("Enter your the Email Address tied to your Zendesk Account: ")
pwd = getpass.getpass("Enter your Zendesk Password: ")

# Path of the outputted csv file
date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csvfile = f'{subdomain}_section_labels_{date_time}.csv'

section_dict = {}
section_name_dict = {}
category_name_dict = {}

# This loop cycles through all pages of articles
while url:
        response = requests.get(url, auth = (user, pwd))
        data = response.json()

        for article in data['articles']:
                section_id = int(article['section_id'])
                labels = article['label_names']
                section_dict[section_id] = section_dict.get(section_id, []) + labels
        for section in data['sections']:
                section_name_dict[int(section['id'])] = (int(section['category_id']), section['name'])
        for category in data['categories']:
                category_name_dict[int(category['id'])] = category['name']

        print(data['next_page'])
        url = data['next_page']

nontransposed_data = []
for sect_key in section_dict.keys():
        data_row = []
        category_id = section_name_dict[sect_key][0]
        category_name = category_name_dict[category_id]
        sect_name = section_name_dict[sect_key][1]
        data_row.extend([f'{category_name} ({category_id})', f'{sect_name} ({sect_key})'])
        data_row.extend(list(set(section_dict[sect_key])))
        nontransposed_data.append(data_row)

result_df = pd.DataFrame(nontransposed_data)
column_names = ['Category', 'Section']
column_names.extend([f'label_{x}' for x in range(1, len(result_df.columns) - 1)])
result_df.columns = column_names
result_df_sorted = result_df.sort_values(by=['Category', 'Section'])
result_df_transposed = result_df_sorted.set_index('Category').transpose()
result_df_transposed.to_csv(csvfile, index=False)

input("Press Enter to close")