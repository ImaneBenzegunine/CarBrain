import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CarScraper:
    def __init__(self, headless=True):
        self.options = uc.ChromeOptions()
        if headless:
            self.options.add_argument('--headless')  
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--remote-debugging-port=9222')  # Add this for debugging
        self.driver = uc.Chrome(options=self.options)
        
    def open_page(self, url):
        """Open the page and wait for the content to load."""
        self.driver.get(url)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ListItem_wrapper__TxHWu"))
        )
    
    def extract_car_links(self, page_number):
        """Extract car links from a given page."""
        website = f"https://www.autoscout24.be/fr/lst?atype=C&cy=B&desc=0&page={page_number}&search_id=a5i2bcp2m1&sort=standard&source=listpage_pagination&ustate=N%2CU"
        self.open_page(website)
        cars_sections = self.driver.find_elements(By.CLASS_NAME, "ListItem_wrapper__TxHWu")
        links = []
        for car in cars_sections:
            try:
                link_car = WebDriverWait(car, 30).until(
                    EC.presence_of_element_located((By.XPATH, './/a'))
                )
                car_url = link_car.get_attribute('href')
                links.append(car_url)
            except Exception as e:
                print(f"Error while retrieving car link: {e}")
        return links
    
    def extract_car_details(self, car_url):
        """Extract car details from a given car page."""
        self.driver.get(car_url)

        # Wait for the basic details section to load
        WebDriverWait(self.driver, 30).until(           
            EC.presence_of_element_located((By.XPATH, '//*[@id="basic-details-section"]/div/div[2]/dl'))
        )
        donnebase = self.driver.find_element(By.XPATH, '//*[@id="basic-details-section"]/div/div[2]/dl')
        Keys = donnebase.find_elements(By.TAG_NAME, 'dt')
        Vals = donnebase.find_elements(By.TAG_NAME, 'dd')

        # Extract car name
        WebDriverWait(self.driver, 30).until(            
            EC.presence_of_element_located((By.CLASS_NAME, "StageTitle_boldClassifiedInfo__sQb0l"))
        )   
        CarName = self.driver.find_element(By.CLASS_NAME, "StageTitle_boldClassifiedInfo__sQb0l")

        # Extract car model
        WebDriverWait(self.driver, 30).until(         
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[2]/div[1]/div[2]/h1/div[1]/span[2]'))
        )
        CarModele = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[2]/div[1]/div[2]/h1/div[1]/span[2]')

        # Extract car price
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'PriceInfo_price__XU0aF'))
        )
        CarPrice = self.driver.find_element(By.CLASS_NAME, 'PriceInfo_price__XU0aF')

        # Extract car condition
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[2]/div[3]/div[2]/div/div'))
        )
        CarEtat = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[2]/div[3]/div[2]/div/div')

        #===> CarsInfoSection1
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'StageArea_overviewContainer__UyZ9n'))
        )
        CarsInfo = self.driver.find_element(By.CLASS_NAME, 'StageArea_overviewContainer__UyZ9n')
        CarInfoDet = CarsInfo.find_elements(By.CLASS_NAME, "VehicleOverview_itemText__AI4dA")
        CarInfoDetMore = [detail.text for detail in CarInfoDet]

        # Extract technical details section (CarsInfoSection2)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl'))
        )
        MoreCarac = self.driver.find_elements(By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl')
        chaine = " ".join(s.text for s in MoreCarac) + " "

        # Extract additional car details (like seats, doors)
        donn = {}
        for key, val in zip(Keys, Vals):
            if key.text == "Sièges" or key.text == "Portes":
                donn[key.text] = val.text

        # Return all extracted car details
        return CarName.text, CarModele.text, CarPrice.text, CarEtat.text, CarInfoDetMore[0], CarInfoDetMore[1], CarInfoDetMore[2], CarInfoDetMore[3], CarInfoDetMore[4], CarInfoDetMore[5], donn.get('Sièges', 'N/A'), donn.get('Portes', 'N/A'), chaine
        
    def close(self):
        """Close the browser."""
        self.driver.quit()

def main():
    scraper = CarScraper()

    try:
        i = 1
        while True:
            car_links = scraper.extract_car_links(i)
            if not car_links:  # Stop the loop if no cars are found
                print("No cars found on page {i}. Stopping.")
                break
            
            print(f"Number of cars on page {i}: {len(car_links)}")
            
            for car_url in car_links:
                try:
                    print(f"Accessing car page: {car_url}")
                    car_name, carModele, CarPrice, Etat, Milieage, Tran, Annee, CarCar, CarPui, CarVen, technical_details, seats, doors = scraper.extract_car_details(car_url)
                    print(f"Car name: {car_name}")
                    print(f"Car model: {carModele}")
                    print(f"Car price: {CarPrice}")
                    print(f"Car condition: {Etat}")
                    print(f"Technical details: {technical_details}")
                    print(f"Seats: {seats}")
                    print(f"Doors: {doors}")
                    print(f"Mileage: {Milieage}")
                    print(f"Transmission: {Tran}")
                    print(f"Year: {Annee}")
                    print(f"Fuel type: {CarCar}")
                    print(f"Power: {CarPui}")
                    print(f"Vendor: {CarVen}")
                except Exception as e:
                    print(f"Error while retrieving car information: {e}")
            i += 1

    except Exception as e:
        print(f"General error: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
