import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


PATH_AUTO_XLSX = os.path.join(BASE_DIR, "data", "output","xlsx", "auto.xlsx")
PATH_PARK_XLSX = os.path.join(BASE_DIR, "data", "output","xlsx", "parkers.xlsx")
PATH_CARV_XLSX = os.path.join(BASE_DIR, "data", "output","xlsx", "carvago.xlsx")

PATH_AUTO_CSV = os.path.join(BASE_DIR, "data", "output","csv", "auto.csv")
PATH_PARK_CSV = os.path.join(BASE_DIR, "data", "output","csv", "parkers.csv")
PATH_CARV_CSV = os.path.join(BASE_DIR, "data", "output","csv", "carvago.csv")


PATH_PROCESSED_CSV = os.path.join(BASE_DIR, "data", "outputTransfomed", "processed.csv")