import requests
import csv
import getpass

# Set the request parameters
# Change the URL according to what information is desired.
subdomain = input("Enter your Zendesk Subdomain (not full URL, but something such as your company name): ")
url = 'https://' + subdomain +'.zendesk.com/api/v2/help_center/en-us/articles.json?sort_by=title&sort_order=asc'

# Use Your Zendesk Support Sign-On Credentials
user = input("Enter your the Email Address tied to your Zendesk Account: ")
pwd = getpass.getpass("Enter your Zendesk Password: ")

# Path of the outputted csv file
csvfile = f'{subdomain}_articles.csv'

# Comment out or remove the unnecessary attributes:
attributes = {
        'id': 'Article ID', 
        'title': 'Article Title',
        'html_url': 'URL',
        'vote_sum': 'Vote Sum',
        'vote_count': 'Vote Count',
        'author_id': 'Author ID',
        'section_id': 'Section ID',
        'draft': 'Draft (True if Draft, False if not)',
        'updated_at': 'Updated At',
        'label_names': 'Label Names'
        }

list_of_lists = []
label_names_tuples_list = []

for key in attributes.keys():
        list_of_lists.append([attributes[key]])

# This loop cycles through all pages of articles
while url:
        response = requests.get(url, auth = (user, pwd))
        data = response.json()

        for article in data['articles']:
                label_names_tuples_list.append(tuple(article['label_names']))
                list_id = 0
                for key in attributes.keys():
                        if key == 'label_names':
                                list_of_lists[list_id].append('')
                        else:
                                list_of_lists[list_id].append(str(article[key]))
                        list_id += 1
        print(data['next_page'])
        url = data['next_page']

print("Number of articles:")
print (len(list_of_lists[0]))

# Data Transposition
transposed_data = zip(*list_of_lists)

# Write to a csv file
with open(csvfile, 'w', newline='') as fp:
        writer = csv.writer(fp, dialect = 'excel')
        article_no = 0
        for article_attr in transposed_data:
                if article_no != 0:
                        article_attr += label_names_tuples_list[article_no - 1]
                writer.writerows([article_attr])
                article_no += 1
        