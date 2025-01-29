import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class CarScraper:
    def __init__(self, headless=True):
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
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ListItem_wrapper__TxHWu"))
        )
    
    def extract_car_links(self, page_number):
        """Extrait les liens des voitures d'une page donnée."""
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
                print(f"Erreur lors de la récupération du lien de la voiture : {e}")
        return links
    
    def extract_car_details(self, car_url):
        """Extrait les détails d'une voiture donnée."""
        self.driver.get(car_url)
        #print("hello1")
        #donnebase
        WebDriverWait(self.driver, 30).until(           
            EC.presence_of_element_located((By.XPATH, '//*[@id="basic-details-section"]/div/div[2]/dl'))
        )
        donnebase = self.driver.find_element(By.XPATH, '//*[@id="basic-details-section"]/div/div[2]/dl')
        Keys = donnebase.find_elements(By.TAG_NAME, 'dt')
        Vals = donnebase.find_elements(By.TAG_NAME, 'dd')
        try:
            #CarNAME
            WebDriverWait(self.driver, 30).until(            
                EC.presence_of_element_located((By.CLASS_NAME, "StageTitle_boldClassifiedInfo__sQb0l"))
            )   
            CarName = self.driver.find_element(By.CLASS_NAME, "StageTitle_boldClassifiedInfo__sQb0l")

            #CarModele
            WebDriverWait(self.driver, 30).until(         
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[2]/div[1]/div[2]/h1/div[1]/span[2]'))
            )
            CarModele = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[2]/div[1]/div[2]/h1/div[1]/span[2]')
            #print("hello2")
            #CarPrice
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'PriceInfo_price__XU0aF'))
            )
            CarPrice = self.driver.find_element(By.CLASS_NAME, 'PriceInfo_price__XU0aF')
            #CareEtat
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[2]/div[3]/div[2]/div/div'))
            )
            CarEtat = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[2]/div[3]/div[2]/div/div')
            ##Miliage
            #WebDriverWait(self.driver, 30).until(           
            #    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[5]/div/div[1]/div[4]'))
            #)
            #CarMil = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[5]/div/div[1]/div[4]')
            ##Transmission
            #WebDriverWait(self.driver, 30).until(
            #    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[5]/div/div[2]/div[4]'))
            #)
            #CarTra = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[5]/div/div[2]/div[2]')
            #print("hello3")
            ##Annee
            #WebDriverWait(self.driver, 30).until(
            #    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[5]/div/div[3]/div[4]'))
            #)
            #CarAnnee = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[5]/div/div[3]/div[4]')
            ##Carbu
            #WebDriverWait(self.driver, 30).until(
            #    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[5]/div/div[4]/div[4]'))
            #)
            #CarCarbu = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[5]/div/div[4]/div[4]')
            ##Puissance
            #WebDriverWait(self.driver, 30).until(
            #    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[5]/div/div[5]/div[4]'))
            #)
            #CarPui = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[5]/div/div[5]/div[4]')
            ##Vendeuer
            #WebDriverWait(self.driver, 30).until(
            #    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[5]/div/div[6]/div[4]'))
            #)
            #CarV = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[5]/div/div[6]/div[4]')
            #Carosseries
            #===> CarsInfoSection1
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'StageArea_overviewContainer__UyZ9n'))
            )
            CarsInfo       =  self.driver.find_element(By.CLASS_NAME, 'StageArea_overviewContainer__UyZ9n')
            CarInfoDet     = CarsInfo.find_elements(By.CLASS_NAME, "VehicleOverview_itemText__AI4dA")
            CarInfoDetMore = [detail.text for detail in CarInfoDet]
            #print(len(CarInfoDet))
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="basic-details-section"]/div/div[2]/dl/dd[1]'))
            )
            Carrpsserie = self.driver.find_element(By.XPATH, '//*[@id="basic-details-section"]/div/div[2]/dl/dd[1]')


        #Etat
            #WebDriverWait(self.driver, 30).until(
            #    EC.presence_of_element_located((By.XPATH, '//*[@id="basic-details-section"]/div/div[2]/dl/dd[2]'))
            #)
            #Etat = self.driver.find_element(By.XPATH, '//*[@id="basic-details-section"]/div/div[2]/dl/dd[2]')
            donn = {}
            for key, val in zip(Keys, Vals) :
                if key.text == "Sièges" or key.text == "Portes" :
                    donn[key.text] = val.text

            
            #===> CarsInfoSection2
            #WebDriverWait(self.driver, 30).until(
            #    EC.presence_of_element_located((By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl'))
            #)
            #MoreCarac = self.driver.find_elements(By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl')
            #chaine = " ".join(s.text for s in MoreCarac) + " "
            #puissance
            WebDriverWait(self.driver, 30).until(         
                EC.presence_of_element_located((By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl/dd[1]'))
            )
            CarModele = self.driver.find_element(By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl/dd[1]')
            
            #transmission
            WebDriverWait(self.driver, 30).until(         
                EC.presence_of_element_located((By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl/dd[2]'))
            )
            puissance = self.driver.find_element(By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl/dd[2]')

            #Cylindree
            WebDriverWait(self.driver, 30).until(         
                EC.presence_of_element_located((By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl/dd[3]'))
            )
            Cylindree = self.driver.find_element(By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl/dd[3]')
            #Vitesses
            WebDriverWait(self.driver, 30).until(         
                EC.presence_of_element_located((By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl/dd[4]'))
            )
            Vitesses = self.driver.find_element(By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl/dd[4]')
            #Cylindres
            WebDriverWait(self.driver, 30).until(         
                EC.presence_of_element_located((By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl/dd[5]'))
            )
            Cylindres = self.driver.find_element(By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl/dd[5]')

            #Poids_a_vide
            WebDriverWait(self.driver, 30).until(         
                EC.presence_of_element_located((By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl/dd[6]'))
            )
            Poids_a_vide = self.driver.find_element(By.XPATH, '//*[@id="technical-details-section"]/div/div[2]/dl/dd[6]')
        except TimeoutException:
            print("Not found")
        except NoSuchElementException:
            print(f"Élément non trouvé pour: {car_url}")
        return CarName.text, CarModele.text, CarPrice.text, CarEtat.text, CarInfoDetMore[0], CarInfoDetMore[1], CarInfoDetMore[2], CarInfoDetMore[3], CarInfoDetMore[4], CarInfoDetMore[5], Carrpsserie.text,  donn['Sièges'], donn['Portes'],puissance.text,Cylindree.text,Vitesses.text,Cylindres.text,Poids_a_vide.text

    
    def close(self):
        """Ferme le navigateur."""
        self.driver.quit()

def main():
    scraper = CarScraper()

    try:
        i = 1
        output = []
        while True:
            car_links = scraper.extract_car_links(i)
            print(f"Nombre de voitures sur la page {i} : {len(car_links)}")
            
            for car_url in car_links:
                try:
                    print(f"Accès à la page de la voiture : {car_url}")
                    car_name, carModele, CarPrice , Etat, Milieage , Tran, Annee, CarCar, CarPui, CarVen, Carrpsserie, Siege, Portes, puissance,Cylindree,Vitesses,Cylindres,Poids_a_vide = scraper.extract_car_details(car_url)
                    car_details = {
                        'car_name': car_name, 'carModele': carModele, 'CarPrice': CarPrice, 'Etat': Etat, 'Milieage': Milieage,
                        'Transmission': Tran, 'Annee': Annee, 'Carburant': CarCar, 'Puissance': CarPui, 'Vendeur': CarVen,
                        'Carrpsserie': Carrpsserie, 'Siege': Siege, 'Portes': Portes, 'puissance': puissance, 
                        'Cylindree': Cylindree, 'Vitesses': Vitesses, 'Cylindres': Cylindres, 'Poids_a_vide': Poids_a_vide
                    }
                    print(f"Nom de la voiture : {car_name}")
                    print(f"Modele de la voiture : {carModele}")
                    print(f"Price de la voiture : {CarPrice}")
                    print(f"Etat de la voiture : {Etat}")
                    print(f"Miliage de la voiture : {Milieage}")
                    print(f"Transmission de la voiture : {Tran}")
                    print(f"Annee de la voiture : {Annee}")
                    print(f"Carburant de la voiture : {CarCar}")
                    print(f"Puissance de la voiture : {CarPui}")
                    print(f"Vendeur de la voiture : {CarVen}")
                    print(f"Carrosserie de la voiture : {CarCar}")
                    print(f"Siege de la voiture : {Siege}")
                    print(f"Portes de la voiture : {Portes}")
                    print(f"Puissance de la voiture : {puissance}")
                    print(f"Cylindree de la voiture : {Cylindree}")
                    print(f"Vitesses de la voiture : {Vitesses}")
                    print(f"Cylindres de la voiture : {Cylindres}")
                    print(f"Poids_a_vide de la voiture : {Poids_a_vide}")
                    car_details = scraper.extract_car_details(car_url)
                    output.append(car_details)
                except Exception as e:
                    print(f"Erreur lors de la récupération des informations de la voiture : {e}")
            i += 1
            column = [
            'car_name', 'carModele', 'CarPrice', 'Etat', 'Milieage', 'Transmission', 'Annee', 'Carburant', 'Puissance',
            'Vendeur', 'Carrpsserie', 'Siege', 'Portes', 'puissance', 'Cylindree', 'Vitesses', 'Cylindres',
            'Poids_a_vide'
            ]
            df = pd.DataFrame(output,columns=column)
            df.to_csv("car_details.csv", index=False)
    except Exception as e:
        print(f"Erreur générale : {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
