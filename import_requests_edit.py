import requests
import csv
import unicodedata
import getpass

# Set the request parameters
# Change the URL according to what information is desired.
subdomain = input("Enter your Zendesk Subdomain (not full URL, but something such as your company name): ")
#subdomain = 'soundid-reference'
url = 'https://' + subdomain +'.zendesk.com/api/v2/help_center/en-us/articles.json?sort_by=title&sort_order=asc'

# Use Your Zendesk Support Sign-On Credentials
user = input("Enter your the Email Address tied to your Zendesk Account: ")
pwd = getpass.getpass("Enter your Zendesk Password: ")

# Path of the outputted csv file
csvfile = 'HelpCenterInformation.csv'

# This loop cycles through all pages of articles, converts the unicode
# to an integer, and writes the integers to an array
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

for key in attributes.keys():
        list_of_lists.append([attributes[key]])

while url:
        response = requests.get(url, auth = (user, pwd))
        data = response.json()

        for article in data['articles']:
                list_id = 0
                for key in attributes.keys():
                        list_of_lists[list_id].append(str(article[key])) #unicodedata.normalize('NFKD', title)
                        list_id += 1
        print(data['next_page'])
        url = data['next_page']

print("Number of articles:")
print (len(list_of_lists[0]))

# Data Transposition
# nontransposed_data = [("Article ID","Article Title","URL","Vote Sum"), [output_1], [output_2], [output_3],[output_4]]
# transposed_data = zip(*nontransposed_data)

# Write to a csv file
with open(csvfile, 'w') as fp:
        writer = csv.writer(fp, dialect = 'excel')
        for attr_list in list_of_lists:
                writer.writerows([attr_list])