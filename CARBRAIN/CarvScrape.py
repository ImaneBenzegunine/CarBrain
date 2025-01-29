import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np

class CarScraper:
    def __init__(self, headless=True):
        """Initialise le scraper avec les options nécessaires."""
        self.options = uc.ChromeOptions()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = uc.Chrome(options=self.options)

    def open_page(self, url):
        """Ouvre une page et attend que le contenu soit chargé."""
        self.driver.get(url)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "css-16iy7v2"))
        )

    def extract_car_links(self, page_number):
        """Extrait les liens des voitures d'une page donnée."""
        try:
            website = f"https://carvago.com/cars?page={page_number}"
            self.open_page(website)
            cars_sections = self.driver.find_elements(By.CLASS_NAME, "css-16iy7v2")
            links = []
            for car in cars_sections:
                try:
                    link_car = car.find_element(By.XPATH, './/a')
                    links.append(link_car.get_attribute('href'))
                except NoSuchElementException:
                    print("Lien non trouvé pour une voiture.")
            return links
        except TimeoutException:
            print(f"Erreur de chargement de la page {page_number}")
            return []

    def get_element_text(self, xpath, timeout=10):
        """Récupère le texte d'un élément identifié par un XPath."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return self.driver.find_element(By.XPATH, xpath).text
        except (TimeoutException, NoSuchElementException):
            return "Non disponible"
    
    def extract_car_details(self, car_url):
        """Extrait les détails d'une voiture donnée."""
        try:
            self.driver.get(car_url)
            car_details = {
                "Id de Voiture":self.get_element_text('//*[@id="car-detail-nav-detail"]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/p/span'),
                "Nom": self.get_element_text('//a[@class="chakra-link css-y0wldb"]'),
                "Modele": self.get_element_text(
                    '//*[@id="car-detail-nav-detail"]/div[2]/div[2]/div/div[1]/div/div[3]/div[2]/p/a'
                ),
                "Prix": self.get_element_text(
                    '//*[@id="__next"]/div/main/div[2]/div[3]/div[4]/div/div/div/div[2]/div/div/div[1]/dl[1]/dd'
                ),
                "Kilometrage": self.get_element_text(
                    '//*[@id="car-detail-nav-detail"]/div[2]/div[1]/div[1]/div/p'
                ),
                "Transmission": self.get_element_text(
                    '//*[@id="car-detail-nav-detail"]/div[2]/div[1]/div[4]/div/p'
                ),
                "Annee": self.get_element_text(
                    '//*[@id="car-detail-nav-detail"]/div[2]/div[1]/div[2]/div/p'
                ),
                "Carburant": self.get_element_text(
                    '//*[@id="detail-hero"]/div/div[2]/div[2]/div[5]/p'
                ),
                "Puissance": self.get_element_text(
                    '//*[@id="car-detail-nav-detail"]/div[2]/div[1]/div[3]/div/p'
                ),

                "Emission_class": self.get_element_text(
                    '//*[@id="car-detail-nav-detail"]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/p'
                ),
                "Drive_type": self.get_element_text(
                    '//*[@id="car-detail-nav-detail"]/div[2]/div[1]/div[6]/div/p'
                ),
                "Engine_capacity": self.get_element_text(
                    '//*[@id="car-detail-nav-detail"]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/p'
                ),
                
                "Localisation": self.get_element_text(
                    '//*[@id="car-detail-nav-detail"]/div[2]/div[1]/div[7]/div/p'
                ),
                "Couleur": self.get_element_text(
                    '//*[@id="car-detail-nav-detail"]/div[2]/div[2]/div/div[1]/div/div[4]/div[2]/p'
                ),
                "Doors": self.get_element_text(
                    '//*[@id="car-detail-nav-detail"]/div[2]/div[2]/div/div[1]/div/div[6]/div[2]/p'
                ) or "Non disponible",
                "Seats": self.get_element_text(
                    '//*[@id="car-detail-nav-detail"]/div[2]/div[2]/div/div[1]/div/div[7]/div[2]/p'
                ) or "Non disponible",
                
                
            }
            
            return car_details
        except Exception as e:
            print(f"Erreur lors de la récupération des détails : {e}")
            return {}

    def close(self):
        """Ferme le navigateur."""
        if self.driver:
            self.driver.quit()


def main():
    scraper = CarScraper()
    try:
        output = pd.DataFrame()
        i = 1
        while True:
            car_links = scraper.extract_car_links(i)
            print(f"Nombre de voitures sur la page {i} : {len(car_links)}")
            
            for car_url in car_links:
                try:
                    print(f"Accès à la voiture : {car_url}")
                    details = scraper.extract_car_details(car_url)
                    if details:
                        print("Détails de la voiture :")
                        for key, value in details.items():
                            print(f"{key}:{value}")
                        df_dictionary = pd.DataFrame([details])
                        output = pd.concat([output, df_dictionary], ignore_index=True)
                            #output.to_csv('data.csv')
                            #print(output.head())
                    print("-" * 50)
                except Exception as e:
                    print(f"Erreur lors de la récupération des informations de la voiture : {e}")
            i += 1
            output.to_csv('data.csv',index=False)  
    except Exception as e:
        print(f"Erreur générale : {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()