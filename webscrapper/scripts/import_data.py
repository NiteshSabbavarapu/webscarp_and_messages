import os
import django

# Point to your Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websracping_backend.settings')
django.setup()


import pandas as pd
from webscrapper.models import Companydetails

# Read CSV file into a DataFrame
csv_file_path ='/home/nitesh/scrapping/yc_companies_20250806_213317.csv'

df = pd.read_csv(csv_file_path, on_bad_lines="skip")

# Iterate through the DataFrame and create Book instances
for index, row in df.iterrows():
    company = Companydetails(
        company_name=row['company_name'][:1000],
        location=row['location'][:1000],
        company_type=row['company_type'][:1000],
        directory=row['directories'][:1000],
        directory_url=row['directory_urls'][:500],  # URLFields usually shorter
        company_profile_url=row['profile_url'][:500],
        scrapped_at=row['scraped_at'],
    )
    company.save()

print("CSV data has been loaded into the Django database.")
