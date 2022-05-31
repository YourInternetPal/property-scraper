from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime


class PropertyProvider:
    def __init__(self):
        self.website_name = "propertyprovider"

    def scrape(self, url_limit=0):
        property_urls = self.get_property_urls(url_limit)
        invalid_prices = ["R", "POR"]
        url_limit = len(property_urls)
        properties_data = []
        for index, url in enumerate(property_urls):
            try:
                print("Getting property data for {0} | Current Property Count: {1} of {2}".format(url, index+1, url_limit))
                property_data = self.get_property_data(url)
                if (property_data['Property Price'] not in invalid_prices):
                    if (property_data['Property Categories'] != ""):
                        properties_data.append(property_data)
                else:
                    print("Property Removed due to Invalid Price in the listing page")
            except Exception as e:
                print(e)
        return properties_data

    def get_property_data(self, property_url):
        property_page = urllib.request.urlopen(property_url['url'])
        property_page = BeautifulSoup(property_page, 'html.parser')

        property_data = dict()
        try:
            property_data['Title'] = property_page.find("div", {"class": "innertitle"}).text
            property_data['Content'] = property_page.find("div", {"class":"innergreybox"}).text.strip()
            property_data['Property Categories'] = property_page.find("div", {"class": "innertitle"}).text
            property_data['Cities'] = property_page.find("div", {"class": "innersubtitle"}).text
            property_data['Property Price'] = property_page.find("div", {"class": "price"}).text.strip().replace(",", "")
            property_data['Ref Number'] = property_page.find("div", {"class": "ref"}).text.strip()    
            #property_data['Property Images'] = "|".join([href['href'] for href in property_page.findAll("a", {"data-lightbox": "main"})])
            property_images = [href['href'] for href in property_page.findAll("a", {"data-lightbox": "main"})]
            if (len(property_images) >= 5 ):
                property_data['image1'] = property_images[0]
                property_data['image2'] = property_images[1]
                property_data['image3'] = property_images[2]
                property_data['image4'] = property_images[3]
                property_data['image5'] = property_images[4]
            elif (len(property_images) >= 4 ):
                property_data['image1'] = property_images[0]
                property_data['image2'] = property_images[1]
                property_data['image3'] = property_images[2]
                property_data['image4'] = property_images[3]
                property_data['image5'] = ""
            elif (len(property_images) >= 3 ):
                property_data['image1'] = property_images[0]
                property_data['image2'] = property_images[1]
                property_data['image3'] = property_images[2]
                property_data['image4'] = ""
                property_data['image5'] = ""
            elif (len(property_images) >= 2 ):
                property_data['image1'] = property_images[0]
                property_data['image2'] = property_images[1]
                property_data['image3'] = ""
                property_data['image4'] = ""
                property_data['image5'] = ""
            elif (len(property_images) >= 1 ):
                property_data['image1'] = property_images[0]
                property_data['image2'] = ""
                property_data['image3'] = ""
                property_data['image4'] = ""
                property_data['image5'] = ""
            else:
                property_data['image1'] = ""
                property_data['image2'] = ""
                property_data['image3'] = ""
                property_data['image4'] = ""
                property_data['image5'] = ""

            
            for spec in property_page.findAll("div", {"class": "spec-layer"}):
                if spec.find("div", {"class": "spec-val"}) is not None:
                    if (spec.find("div", {"class": "spec-desc"}).text.strip() not in property_data):
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "No of Bedrooms"):
                            property_data['Bedrooms'] = spec.find("div", {"class": "spec-val"}).text.strip()
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Total No of Bathrooms"):
                            property_data['Bathrooms'] = spec.find("div", {"class": "spec-val"}).text.strip()

                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Garage (Lock Up)"):
                            property_data['Garage'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Airconditioning"):
                            property_data['Airconditioning'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Front Terrace"):
                            property_data['Terrace'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"

                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Ocean Views"):
                            property_data['Sea Views'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Front Garden"):
                            property_data['Garden'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Swimming Pool"):
                            property_data['Swimming Pool'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Courtyard"):
                            property_data['Courtyard'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Back Balconies No of"):
                            property_data['Balcony'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Lift"):
                            property_data['Lift'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"

                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Pets Allowed"):
                            property_data['Pets Allowed'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"

        except :
            property_images = []
            property_data['Title'] = property_page.find("div", {"class": "property-type"}).text.strip()
            property_data['Content'] = property_page.find("div", {"class": "property-description"}).text.strip()
            property_data['Property Categories'] = property_page.find("div", {"class": "property-type"}).text.strip()
            property_data['Cities'] = property_page.find("div", {"class": "property-location"}).text.strip()
            property_data['Property Price'] = property_page.find("div", {"class": "property-price"}).text.strip()[2:].replace(",", "")
            property_data['Ref Number'] = property_page.find("div", {"class": "property-basic-info"}).find("strong").text.strip()
            for image in property_page.find("div", {"class": "banner-section"}).findAll("a", {"data-fancybox": "gallery"}):
                property_images.append(image['href'])
            # property_data['Property Images'] = "|".join(property_images)
            if (len(property_images) >= 5 ):
                property_data['image1'] = property_images[0]
                property_data['image2'] = property_images[1]
                property_data['image3'] = property_images[2]
                property_data['image4'] = property_images[3]
                property_data['image5'] = property_images[4]
            elif (len(property_images) >= 4 ):
                property_data['image1'] = property_images[0]
                property_data['image2'] = property_images[1]
                property_data['image3'] = property_images[2]
                property_data['image4'] = property_images[3]
                property_data['image5'] = ""
            elif (len(property_images) >= 3 ):
                property_data['image1'] = property_images[0]
                property_data['image2'] = property_images[1]
                property_data['image3'] = property_images[2]
                property_data['image4'] = ""
                property_data['image5'] = ""
            elif (len(property_images) >= 2 ):
                property_data['image1'] = property_images[0]
                property_data['image2'] = property_images[1]
                property_data['image3'] = ""
                property_data['image4'] = ""
                property_data['image5'] = ""
            elif (len(property_images) >= 1 ):
                property_data['image1'] = property_images[0]
                property_data['image2'] = ""
                property_data['image3'] = ""
                property_data['image4'] = ""
                property_data['image5'] = ""
            else:
                property_data['image1'] = ""
                property_data['image2'] = ""
                property_data['image3'] = ""
                property_data['image4'] = ""
                property_data['image5'] = ""


            for spec in property_page.findAll("div", {"class": "spec-layer"}):
                if spec.find("div", {"class": "spec-val"}) is not None:
                    if (spec.find("div", {"class": "spec-desc"}).text.strip() not in property_data):
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "No of Bedrooms"):
                            property_data['Bedrooms'] = spec.find("div", {"class": "spec-val"}).text.strip()
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Total No of Bathrooms"):
                            property_data['Bathrooms'] = spec.find("div", {"class": "spec-val"}).text.strip()

                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Garage (Lock Up)"):
                            property_data['Garage'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Airconditioning"):
                            property_data['Airconditioning'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Front Terrace"):
                            property_data['Terrace'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"

                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Ocean Views"):
                            property_data['Sea Views'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Front Garden"):
                            property_data['Garden'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Swimming Pool"):
                            property_data['Swimming Pool'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Courtyard"):
                            property_data['Courtyard'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Back Balconies No of"):
                            property_data['Balcony'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
                        
                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Lift"):
                            property_data['Lift'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"

                        if (spec.find("div", {"class": "spec-desc"}).text.strip() == "Pets Allowed"):
                            property_data['Pets Allowed'] = "1" if spec.find("div", {"class": "spec-val"}).text.strip() == "Yes" else "0"
        
        # =========== if Features aren't available for the current property, set it to zero ======
        features = ['Garage', 'Airconditioning', 'Terrace', 'Sea Views', 'Garden', 'Swimming Pool', 'Courtyard', 'Balcony', 'Lift', 'Pets Allowed', 'Bedrooms', 'Bathrooms']
        for feature in features:
            if feature not in property_data:
                property_data[feature] = "0"
        #====================================================================

        # ============ Data that won't change from layout to layout ==================
        property_data['Agency'] = self.website_name.capitalize()
        property_data['Property Types'] = property_url['deal_type']
        property_data['Ref Link'] = property_url['url']

        # ======== Fixed Data =========
        property_data['PIM ID'] = "{0}{1}".format(property_data['Agency'], property_data['Ref Number'])
        property_data['Post Type'] = "property"  # IMPORTANT: Fixed Value, DON'T Change!
        # ===============================================================
        
        return property_data

    def get_property_urls(self, limit=0):
        """
        Gets URLs for every property in the website

        Keyword arguments:
        None

        :return:
        [{'deal_type': 'sale' | 'rent', 'property_category': 'residential' | 'commercial' , 'url': 'THE URL'}...]
        """
        property_urls = []
        search_result_urls = [
            {"deal_type": "sales", "property_category": "residential",
             "link": "http://<URL_REMOVED>/search/property?ctx=1&st=sale&pr=20000%3B5000000&da=&stcat=residential&bd=&web_ref=" },
        ]

        print("Fetching Property URLs from {0}".format(self.website_name))

        for url in search_result_urls:
            page_number = 1
            resultsCount = None
            while resultsCount != 0:
                current_page_url = url['link']+"&page="+str(page_number)
                search_result_page = urllib.request.urlopen(current_page_url)
                search_result_page = BeautifulSoup(search_result_page, 'html.parser')
                try:
                    resultsCount = [int(s) for s in search_result_page.find("div", {"class": "not-found"}).find("h4").text.split() if s.isdigit()][0]
                except IndexError:
                    resultsCount = 0
                    continue

                properties = search_result_page.findAll("div", {"class": "property-box"})
                for property in properties:
                    if (limit != 0 and len(property_urls) >= limit):
                            print("Scraped URLs Count : {0}".format(len(property_urls)))
                            return property_urls
                    property_url = "http://<URL_REMOVED>"+property.find("div", {"class": "property-image"}).find("a")['href']
                    if property_url not in property_urls:
                        print(property_url)
                        property_urls.append(
                            {"deal_type": url['deal_type'], "property_category": url['property_category'], "url": property_url}
                        )
                        

                page_number += 1
                

        return property_urls