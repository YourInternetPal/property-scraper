from scrapers import *
import csv
import json
from ftplib import FTP
import io


# ======= Configurations ==========
config = {"FTP_SERVER": "", "FTP_USERNAME": "", "FTP_PASSWORD": ""}
csv_file_name = "properties.csv"
# ====================================

#  ============ Scrapers ============
propertyprovider = propertyprovider.PropertyProvider()
# ====================================

#  ============ Properties Data ============
properties_data = list()
properties_data += propertyprovider.scrape()
# ====================================

# ============ Generate CSV File ============
print("Generating CSV File")
properties_csv_file = io.StringIO()

fields = ['PIM ID', 'Title', 'Content', 'Post Type', 'Property Categories', 'Property Types', 'Cities', 'Property Price', 
'Bedrooms', 'Bathrooms', 'image1', 'image2', 'image3', 'image4', 'image5', 'Garage', 'Airconditioning', 'Terrace', 'Sea Views', 'Garden', 'Swimming Pool', 
'Courtyard', 'Balcony', 'Lift', 'Pets Allowed', 'Ref Number', 'Ref Link', 'Agency']
csv_file_writer = csv.DictWriter(properties_csv_file, fieldnames=fields, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
csv_file_writer.writeheader()
for property_data in properties_data:
    csv_file_writer.writerow(property_data)
# ====================================

# ============ Upload to FTP ================
print("Uploading to FTP Server")
ftp = FTP()
ftp.connect(config['FTP_SERVER'], 21)
ftp.login(config['FTP_USERNAME'],config['FTP_PASSWORD'])
ftp.storbinary("STOR {0}".format(csv_file_name), io.BytesIO(properties_csv_file.getvalue().encode()), 1024)
ftp.quit()
# ====================================
properties_csv_file.close()