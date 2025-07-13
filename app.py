import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Configurare pagină
st.set_page_config(layout="wide", page_title="Well-to-Wheel")

# CSS personalizat
st.markdown("""
<style>
.stApp, .stDataFrame, .stPlotlyChart {
    background-color: white !important;
}
.css-1v0mbdj, .st-emotion-cache-1v0mbdj {
    display: none !important;
}
h1, h2, h3, p, .stMarkdown, .stSelectbox, .stRadio, .stSlider {
    color: black !important;
}
.stSelectbox, .stRadio, .stSlider {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 15px;
}
.specs-box {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 10px;
    margin-top: 10px;
    background-color: #f9f9f9;
}
</style>
""", unsafe_allow_html=True)

# ---- DATE DE BAZĂ ----
# mix energetic
tari = {
    "Europa": {"Bioenegie": 4, "Carbune": 13.25, "Gaz": 22.99 , "Nuclear": 19.75, "Hidro": 17.6, "Eolian": 12.38, "Solar": 7.14, "Alte surse fosile": 2.4, "Alte surse regenerabile": 0.48},
    "UE": {"Bioenegie": 5.47, "Carbune": 9.8, "Gaz": 15.69, "Nuclear": 23.63, "Hidro": 13.18, "Eolian": 17.52, "Solar": 11.03, "Alte surse fosile": 3.43, "Alte surse regenerabile": 0.25},
    "Romania": {"Bioenegie": 0.96, "Carbune": 12.98, "Gaz": 18.62, "Nuclear": 20.39, "Hidro": 26.58, "Eolian": 12.16, "Solar": 7.95, "Alte surse fosile": 0.36, "Alte surse regenerabile": 0},
    "Germania": {"Bioenegie": 9.63, "Carbune": 21.88, "Gaz": 16.6, "Nuclear": 0, "Hidro": 4.91, "Eolian": 27.98, "Solar": 14.89, "Alte surse fosile": 4.07, "Alte surse regenerabile": 0.04},
    "Norvegia": {"Bioenegie": 0.16, "Carbune": 0.02, "Gaz": 1.09, "Nuclear": 0, "Hidro": 88.71, "Eolian": 9.29, "Solar": 0.23, "Alte surse fosile": 0.5, "Alte surse regenerabile": 0},
    "Polonia": {"Bioenegie": 4.93, "Carbune": 53.5, "Gaz": 12.06, "Nuclear": 0, "Hidro": 1.37, "Eolian": 14.59, "Solar": 8.95, "Alte surse fosile": 4.59, "Alte surse regenerabile": 0},
    "Spania": {"Bioenegie": 2.23, "Carbune": 0.95, "Gaz": 18.68, "Nuclear": 19.55, "Hidro": 11.64, "Eolian": 22.44, "Solar": 20.9, "Alte surse fosile": 3.61, "Alte surse regenerabile": 0},
    "Italia": {"Bioenegie": 6.03, "Carbune": 1.75, "Gaz": 44, "Nuclear": 0, "Hidro": 19.19, "Eolian": 8.45, "Solar": 13.53, "Alte surse fosile": 4.93, "Alte surse regenerabile": 2.12},
    "Suedia": {"Bioenegie": 6.02, "Carbune": 0, "Gaz": 0.09, "Nuclear": 29.2, "Hidro": 37.68, "Eolian": 23.64, "Solar": 2.11, "Alte surse fosile": 1.26, "Alte surse regenerabile": 0},
    "Olanda": {"Bioenegie": 5.58, "Carbune": 6.72, "Gaz": 36.41, "Nuclear": 2.96, "Hidro": 0.08, "Eolian": 27.26, "Solar": 17.46, "Alte surse fosile": 3.49, "Alte surse regenerabile": 0.03},
    "Franța": {"Bioenegie": 1.75, "Carbune": 0.31, "Gaz": 3.42, "Nuclear": 68, "Hidro": 12.42, "Eolian": 7.74, "Solar": 4.23, "Alte surse fosile": 2.02, "Alte surse regenerabile": 0.1},
    "Danemarca": {"Bioenegie": 18.82, "Carbune": 7.02, "Gaz": 2.54, "Nuclear": 0, "Hidro": 0.06, "Eolian": 57.91, "Solar": 11.26, "Alte surse fosile": 2.4, "Alte surse regenerabile": 0},
}

emisii_tari = {
    "Europa": 284.28,
    "UE": 213.32,
    "Romania": 245.55,
    "Germania": 344.14,
    "Norvegia": 30.75,
    "Polonia": 614.98,
    "Spania": 146.15,
    "Italia": 287.5,
    "Suedia": 35.82,
    "Olanda": 253.68,
    "Franța": 44.18,
    "Danemarca": 143.3
} 
# Coeficienți emisii pe productie de hidrogen 

emisii_hidrogen = {
    "Roz": 450,      
    "Albastru": 2250,
    "Verde": 200,
    "Galben": 850,
    "Brun": 22500,
    "Gri": 10500,
    "Turcoaz": 2250,
}


# Modele vehicule
modele_vehicule = {
    "HEV": {
        "Toyota Corolla Hybrid XII": {"consum": 4.1, "emisii_tank": 93},
        "Toyota Prius V": {"consum": 3.7, "emisii_tank": 70},
	"Toyota Prius III": {"consum": 4, "emisii_tank": 91},
	"Toyota Prius II": {"consum": 4.3, "emisii_tank": 104},
        "Honda Civic Hybrid": {"consum": 4.7, "emisii_tank": 111},
        "Hyundai Ioniq Hybrid": {"consum": 3.4, "emisii_tank": 79},
        "Lexus UX 250h": {"consum": 4.2, "emisii_tank": 99},
        "Ford Mondeo IV Hybrid": {"consum": 4.5, "emisii_tank": 102},
        "Toyota C-HR Hybrid II": {"consum": 4.8, "emisii_tank": 107},
        "Toyota RAV4 V": {"consum": 5.7, "emisii_tank": 127},
    },
    "PHEV": {
        "Mitsubishi Outlander IV": {"consum_combustibil": 0.8, "consum_electric": 23.45, "emisii_tank": 19, "autonomie": 84},
        "Volvo XC60 II Recharge": {"consum_combustibil": 1.2, "consum_electric": 22.05, "emisii_tank": 26, "autonomie": 72},
        "BMW 330e": {"consum_combustibil": 0.95, "consum_electric": 15, "emisii_tank": 23, "autonomie": 90},
        "Mercedes A 250 e": {"consum_combustibil": 0.95, "consum_electric": 16, "emisii_tank": 21, "autonomie": 75},
        "Peugeot 308 III": {"consum_combustibil": 1.2, "consum_electric": 15.2, "emisii_tank": 26, "autonomie": 67},
        "Mercedes-Benz C 300e": {"consum_combustibil": 0.9, "consum_electric": 22, "emisii_tank": 18, "autonomie": 95},
        "Opel Astra L": {"consum_combustibil": 1, "consum_electric": 15.1, "emisii_tank": 24, "autonomie": 70},
        "Kia Niro II": {"consum_combustibil": 1, "consum_electric": 14, "emisii_tank": 21, "autonomie": 59},
        "Toyota RAV4 V Plug-in": {"consum_combustibil": 1, "consum_electric": 16.6, "emisii_tank": 22, "autonomie": 75},
        "Toyota C-HR II Plug-in": {"consum_combustibil": 0.9, "consum_electric": 15.5, "emisii_tank": 20, "autonomie": 66}
    },
    "BEV": {
        "Tesla Model 3 Long Range": {"consum": 14, "emisii_tank": 0},
        "Tesla Model Y Long Range": {"consum": 14.2, "emisii_tank": 0},
        "VW ID.3 Pro S": {"consum": 15.6, "emisii_tank": 0},
        "VW ID.4 GTX": {"consum": 16.1, "emisii_tank": 0},
        "Audi Q4 e-tron": {"consum": 17.5, "emisii_tank": 0},
        "BMW i4 eDrive40": {"consum": 17, "emisii_tank": 0},
        "Hyundai Kona II Long Range": {"consum": 15.75, "emisii_tank": 0},
        "Kia EV6 Long Range": {"consum": 18, "emisii_tank": 0},
        "Skoda Enyaq 85": {"consum": 14.8, "emisii_tank": 0},
        "BYD Dolphin": {"consum": 13.1, "emisii_tank": 0}
    },
    "FCEV": {
	"Toyota Mirai II": {
            "consum": 0.76,
        },
        "Honda Clarity FC": {
            "consum": 1,
        },
        "Hyundai Nexo": {
            "consum": 0.84,
        },
        "Hyundai ix35": {
            "consum": 1
        }
    }
}

# Specificații tehnice pentru fiecare model
specs_tehnice = {
    "HEV": {
        "Toyota Corolla Hybrid XII": {
            "Perioadă fabricație": "2023-",
            "Standard ecologic": "EURO 6AG",
            "Emisii (WLTP)": "93",
            "Consum (WLTP)": "4.1",
            "Volum motor": "1798",
            "Masă proprie": "1360",
            "Putere maxima": "71",
            "Cuplu maxim": "142"
        },
        "Toyota Prius V": {
            "Perioadă fabricație": "2023-",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "70",
            "Consum (WLTP)": "4",
            "Volum motor": "1986",
            "Masă proprie": "1470",
            "Putere maxima": "111",
            "Cuplu maxim": "188"
        },
	 "Toyota Prius III": {
            "Perioadă fabricație": "2009-2012",
            "Standard ecologic": "EURO 5",
            "Emisii (WLTP)": "91",
            "Consum (WLTP)": "4",
            "Volum motor": "1798",
            "Masă proprie": "1395",
            "Putere maxima": "113",
            "Cuplu maxim": "321"
        },
 	"Toyota Prius II": {
            "Perioadă fabricație": "2003-2009",
            "Standard ecologic": "EURO 4",
            "Emisii (WLTP)": "104",
            "Consum (WLTP)": "4.3",
            "Volum motor": "1497",
            "Masă proprie": "1300",
            "Putere maxima": "83",
            "Cuplu maxim": "478"
        },
        "Honda Civic Hybrid": {
            "Perioadă fabricație": "2022-",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "111",
            "Consum (WLTP)": "4.7",
            "Volum motor": "1993",
            "Masă proprie": "1442",
            "Putere maxima": "135",
            "Cuplu maxim": "315"
        },
	 "Hyundai Ioniq Hybrid": {
            "Perioadă fabricație": "2016-2019",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "79",
            "Consum (WLTP)": "3.4",
            "Volum motor": "1580",
            "Masă proprie": "1370",
            "Putere maxima": "103",
            "Cuplu maxim": "265"
        },
 	"Lexus UX 250h": {
            "Perioadă fabricație": "2019-2024",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "99",
            "Consum (WLTP)": "4.2",
            "Volum motor": "1987",
            "Masă proprie": "1570",
            "Putere maxima": "130",
            "Cuplu maxim": "400"
        },
 	"Ford Mondeo IV Hybrid": {
            "Perioadă fabricație": "2019-2022",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "102",
            "Consum (WLTP)": "4.5",
            "Volum motor": "1999",
            "Masă proprie": "1624",
            "Putere maxima": "137",
            "Cuplu maxim": "300"
        },
 	"Toyota C-HR Hybrid II": {
            "Perioadă fabricație": "2023-",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "107",
            "Consum (WLTP)": "4.8",
            "Volum motor": "1798",
            "Masă proprie": "1430",
            "Putere maxima": "102",
            "Cuplu maxim": "300"
        },
 	"Toyota RAV4 V": {
            "Perioadă fabricație": "2021-",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "127",
            "Consum (WLTP)": "5.7",
            "Volum motor": "2487",
            "Masă proprie": "1670",
            "Putere maxima": "218",
            "Cuplu maxim": "400"
        },
    },
   "PHEV": {
        "Mitsubishi Outlander IV": {
            "Perioadă fabricație": "2021-",
            "Standard ecologic": "EURO 6d",
            "Emisii (WLTP)": "19",
            "Consum mixt (WLTP)": "0.8",
            "Consum energie (WLTP)": "23.45",
            "Volum motor": "1969",
            "Capacitate baterie": "14.9",
            "Masă proprie": "2075",
            "Putere maxima": "183",
            "Cuplu maxim": "451",
            "Autonomie mod electric (WLTP)": "84"
        },
        "Volvo XC60 II Recharge": {
            "Perioadă fabricație": "2021-",
            "Standard ecologic": "EURO 6d",
            "Emisii (WLTP)": "26",
            "Consum mixt (WLTP)": "1.2",
            "Consum energie (WLTP)": "20.5",
            "Volum motor": "1969",
            "Capacitate baterie": "14.9",
            "Masă proprie": "2075",
            "Putere maxima": "257",
            "Cuplu maxim": "350",
            "Autonomie mod electric (WLTP)": "72"
        },
	"BMW 330e": {
            "Perioadă fabricație": "2024-",
            "Standard ecologic": "EURO 6e",
            "Emisii (WLTP)": "23",
            "Consum mixt (WLTP)": "0.95",
            "Consum energie (WLTP)": "22.05",
            "Volum motor": "1998",
            "Capacitate baterie": "19.5",
            "Masă proprie": "1835",
            "Putere maxima": "214",
            "Cuplu maxim": "420",
            "Autonomie mod electric (WLTP)": "90"
        },
	"Mercedes A 250 e": {
            "Perioadă fabricație": "2022-",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "21",
            "Consum mixt (WLTP)": "0.95",
            "Consum energie (WLTP)": "16",
            "Volum motor": "1332",
            "Capacitate baterie": "15.6",
            "Masă proprie": "1727",
            "Putere maxima": "160",
            "Cuplu maxim": "450",
            "Autonomie mod electric (WLTP)": "75"
        },
	"Peugeot 308 III": {
            "Perioadă fabricație": "2021-",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "26",
            "Consum mixt (WLTP)": "1.2",
            "Consum energie (WLTP)": "15.2",
            "Volum motor": "1598",
            "Capacitate baterie": "12.4",
            "Masă proprie": "1603",
            "Putere maxima": "132",
            "Cuplu maxim": "360",
            "Autonomie mod electric (WLTP)": "67"
        },
	"Mercedes-Benz C 300e": {
            "Perioadă fabricație": "2022-",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "18",
            "Consum mixt (WLTP)": "0.9",
            "Consum energie (WLTP)": "22",
            "Volum motor": "1999",
            "Capacitate baterie": "19.53",
            "Masă proprie": "2055",
            "Putere maxima": "233",
            "Cuplu maxim": "550",
            "Autonomie mod electric (WLTP)": "95"
        },
	"Opel Astra L": {
            "Perioadă fabricație": "2021-",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "24",
            "Consum mixt (WLTP)": "1",
            "Consum energie (WLTP)": "15.1",
            "Volum motor": "1598",
            "Capacitate baterie": "12.4",
            "Masă proprie": "1603",
            "Putere maxima": "132",
            "Cuplu maxim": "360",
            "Autonomie mod electric (WLTP)": "70"
        },
	"Kia Niro II": {
            "Perioadă fabricație": "2024-",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "21",
            "Consum mixt (WLTP)": "1",
            "Consum energie (WLTP)": "14",
            "Volum motor": "1580",
            "Capacitate baterie": "11.1",
            "Masă proprie": "1550",
            "Putere maxima": "125",
            "Cuplu maxim": "265",
            "Autonomie mod electric (WLTP)": "59"
        },
	"Toyota RAV4 V Plug-in": {
            "Perioadă fabricație": "2021-",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "22",
            "Consum mixt (WLTP)": "1",
            "Consum energie (WLTP)": "16.6",
            "Volum motor": "2487",
            "Capacitate baterie": "18.1",
            "Masă proprie": "1880",
            "Putere maxima": "225",
            "Cuplu maxim": "409",
            "Autonomie mod electric (WLTP)": "75"
        },
	"Toyota C-HR II Plug-in": {
            "Perioadă fabricație": "2023-",
            "Standard ecologic": "EURO 6",
            "Emisii (WLTP)": "20",
            "Consum mixt (WLTP)": "0.9",
            "Consum energie (WLTP)": "15.5",
            "Volum motor": "1987",
            "Capacitate baterie": "13.8",
            "Masă proprie": "1645",
            "Putere maxima": "164",
            "Cuplu maxim": "208",
            "Autonomie mod electric (WLTP)": "66"
        },
    },
    "BEV": {
        "Tesla Model 3 Long Range": {
            "Perioadă fabricație": "2023-",
            "Consum (WLTP)": "14",
            "Capacitate baterie (utilizabilă)": "77",
            "Masă proprie": "1828",
            "Putere maxima": "366",
            "Cuplu maxim": "560",
            "Autonomie (WLTP)": "549"
        },
        "Tesla Model Y Long Range": {
            "Perioadă fabricație": "2025-",
            "Consum (WLTP)": "14.2",
            "Capacitate baterie (utilizabilă)": "78.4",
            "Masă proprie": "1901",
            "Putere maxima": "255",
            "Cuplu maxim": "350",
            "Autonomie (WLTP)": "622"
        },
        "VW ID.3 Pro S": {
            "Perioadă fabricație": "2024-",
            "Consum (WLTP)": "15.6",
            "Capacitate baterie (utilizabilă)": "77",
            "Masă proprie": "1887",
            "Putere maxima": "170",
            "Cuplu maxim": "310",
            "Autonomie (WLTP)": "557"
        },
 	"VW ID.4 GTX": {
            "Perioadă fabricație": "2023-",
            "Consum (WLTP)": "16.1 ",
            "Capacitate baterie (utilizabilă)": "77",
            "Masă proprie": "2156",
            "Putere maxima": "210",
            "Cuplu maxim": "545",
            "Autonomie (WLTP)": "550"
        },
 	"Audi Q4 e-tron": {
            "Perioadă fabricație": "2023-",
            "Consum (WLTP)": "17.5",
            "Capacitate baterie (utilizabilă)": "77",
            "Masă proprie": "2070",
            "Putere maxima": "210",
            "Cuplu maxim": "545",
            "Autonomie (WLTP)": "502"
        },
        "BMW i4 eDrive40": {
            "Perioadă fabricație": "2024-",
            "Consum (WLTP)": "17",
            "Capacitate baterie (utilizabilă)": "81.3",
            "Masă proprie": "2050",
            "Putere maxima": "250",
            "Cuplu maxim": "430",
            "Autonomie (WLTP)": "550"
        },
 	"Hyundai Kona II Long Range": {
            "Perioadă fabricație": "2023-",
            "Consum (WLTP)": "15.75",
            "Capacitate baterie (utilizabilă)": "61",
            "Masă proprie": "1800",
            "Putere maxima": "160",
            "Cuplu maxim": "255",
            "Autonomie (WLTP)": "505"
        },
 	"Kia EV6 Long Range": {
            "Perioadă fabricație": "2024-",
            "Consum (WLTP)": "18",
            "Capacitate baterie (utilizabilă)": "88.1",
            "Masă proprie": "2054",
            "Putere maxima": "160",
            "Cuplu maxim": "310",
            "Autonomie (WLTP)": "555"
        },
        "Skoda Enyaq 85": {
            "Perioadă fabricație": "2025",
            "Consum (WLTP)": "14.8",
            "Capacitate baterie (utilizabilă)": "77",
            "Masă proprie": "2066",
            "Putere maxima": "210",
            "Cuplu maxim": "545",
            "Autonomie (WLTP)": "586"
        },
 	"BYD Dolphin": {
            "Perioadă fabricație": "2025-",
            "Consum (WLTP)": "13.1",
            "Capacitate baterie (utilizabilă)": "60.48",
            "Masă proprie": "1500",
            "Putere maxima": "150",
            "Cuplu maxim": "310",
            "Autonomie (WLTP)": "520"
        },

    },
    "FCEV": {
         "Toyota Mirai II": {
            "Perioadă fabricație": "2020-",
            "Consum": "0.76",
            "Capacitate rezervor hidrogen": "5.6",
            "Masă proprie": "1900",
            "Putere maxima": "135",
            "Cuplu maxim": "300"
        },
	 "Honda Clarity FC": {
            "Perioadă fabricație": "2008-2014",
            "Consum": "1",
            "Capacitate rezervor hidrogen": "5",
            "Masă proprie": "1625",
            "Putere maxima": "98",
            "Cuplu maxim": "256"
        },
        "Hyundai Nexo": {
            "Perioadă fabricație": "2018-2025",
            "Consum": "0.84",
            "Capacitate rezervor hidrogen": "6.33",
            "Masă proprie": "1889",
            "Putere maxima": "135",
            "Cuplu maxim": "395"
        },
         "Hyundai ix35": {
            "Perioadă fabricație": "2013-",
            "Consum": "1",
            "Capacitate rezervor hidrogen": "5.64",
            "Masă proprie": "1846",
            "Putere maxima": "100",
            "Cuplu maxim": "300"
        }
    }
}

# ---- FUNCȚIE CALCUL EMISII ----
def calculeaza_emisii(tip_vehicul, model, tara, distanta, **kwargs):
    # emisii medii pentru țara selectată
    emisii_medii_tara = emisii_tari[tara_selectata] 
    
    if tip_vehicul == "HEV":
        date = modele_vehicule["HEV"][model]
        emisii_per_litru = 170.465
        emisii_well = date["consum"] / 100 * emisii_per_litru * distanta
        emisii_tank = date["emisii_tank"] * distanta
        return {
            "Well-to-Tank": emisii_well,
            "Tank-to-Wheel": emisii_tank,
            "Total": emisii_well + emisii_tank
        }
    
    elif tip_vehicul == "PHEV":
        date = modele_vehicule["PHEV"][model]
        emisii_per_litru = 170.465  # gCO₂/litru pentru benzină
    
        if distanta <= date["autonomie"]:
           emisii_well = (date["consum_electric"] / 100 * distanta) * emisii_medii_tara
           emisii_tank = 0
        else:
           emisii_well = (date["consum_electric"] / 100 * date["autonomie"]) * emisii_medii_tara + \
                      (date["consum_combustibil"] / 100 * (distanta - date["autonomie"]) * emisii_per_litru)
           emisii_tank = date["emisii_tank"] * distanta
        return {
            "Well-to-Tank": emisii_well,
            "Tank-to-Wheel": emisii_tank,
            "Total": emisii_well + emisii_tank
        }

    elif tip_vehicul == "BEV":
        date = modele_vehicule["BEV"][model]
        emisii_well = (date["consum"] * distanta) * (emisii_medii_tara/100)
        emisii_tank = 0
        return {
            "Well-to-Tank": emisii_well,
            "Tank-to-Wheel": emisii_tank,
            "Total": emisii_well + emisii_tank
        }
    
    elif tip_vehicul == "FCEV":
        date = modele_vehicule["FCEV"][model]
        tip_hidrogen = kwargs.get("tip_hidrogen", "Gri")  

        emisii_tip_hidrogen = emisii_hidrogen[tip_hidrogen]  
        consum = date["consum"]  # consum vehicul în kg H₂ / 100 km

        emisii_well = (consum / 100) * emisii_tip_hidrogen * distanta  
        emisii_tank = 0  # Nu există emisii TTW la FCEV

        return {
            "Well-to-Tank": emisii_well,
            "Tank-to-Wheel": emisii_tank,
            "Total": emisii_well + emisii_tank
        }


# ---- INTERFAȚA UTILIZATOR ----
st.title('Analiză Well-to-Wheel')

# 1. Selectare țară cu afișare mix energetics
tara_selectata = st.selectbox("Selectează o zonă pentru analiză:", options=list(tari.keys()))

# Afișare mix energetic informativ (fără coeficienți)

st.write(f"**Mix energetic pentru {tara_selectata}:**")
for sursa, procent in tari[tara_selectata].items():
    st.write(f"- {sursa}: {procent}%")

st.write(f"**Emisii CO₂ pentru {tara_selectata}: {emisii_tari[tara_selectata]} gCO₂/kWh**")

# 2. Selectare vehicule pentru comparație
st.header("Vehicule pentru comparație")

cols = st.columns(4)
vehicule_selectate = {}

with cols[0]:  # HEV
    st.subheader("HEV")
    if st.checkbox("Adaugă HEV", key="hev_check"):
        model = st.selectbox("Selectează autovehicul HEV", options=list(modele_vehicule["HEV"].keys()))
        vehicule_selectate["HEV"] = {"model": model}
        
        # Afișare specificații tehnice
        specs = specs_tehnice["HEV"][model]
        st.write("**Specificații tehnice vehicul selectat:**")
        st.write(f"- Perioadă fabricație: {specs['Perioadă fabricație']}")
        st.write(f"- Standard ecologic: {specs['Standard ecologic']}")
        st.write(f"- Emisii (WLTP): {specs['Emisii (WLTP)']} gCO2/km")
        st.write(f"- Consum (WLTP): {specs['Consum (WLTP)']} l/100km")
        st.write(f"- Volum motor: {specs['Volum motor']} cm³")
        st.write(f"- Masă proprie: {specs['Masă proprie']} kg")
        st.write(f"- Putere maximă: {specs['Putere maxima']} kW")
        st.write(f"- Cuplu maxim: {specs['Cuplu maxim']} Nm")
        st.markdown('</div>', unsafe_allow_html=True)

with cols[1]:  # PHEV
    st.subheader("PHEV")
    if st.checkbox("Adaugă PHEV", key="phev_check"):
        model = st.selectbox("Selectează autovehicul PHEV", options=list(modele_vehicule["PHEV"].keys()))
        vehicule_selectate["PHEV"] = {"model": model}
        
        # Afișare specificații tehnice
        specs = specs_tehnice["PHEV"][model]
        st.write("**Specificații tehnice vehicul selectat:**")
        st.write(f"- Perioadă fabricație: {specs['Perioadă fabricație']}")
        st.write(f"- Standard ecologic: {specs['Standard ecologic']}")
        st.write(f"- Emisii (WLTP): {specs['Emisii (WLTP)']} gCO2/km")
        st.write(f"- Consum mixt (WLTP): {specs['Consum mixt (WLTP)']} l/100km")
        st.write(f"- Consum energie (WLTP): {specs['Consum energie (WLTP)']} kWh/100km")
        st.write(f"- Volum motor: {specs['Volum motor']} cm³")
        st.write(f"- Capacitate baterie: {specs['Capacitate baterie']} kWh")
        st.write(f"- Masă proprie: {specs['Masă proprie']} kg")
        st.write(f"- Putere maximă: {specs['Putere maxima']} kW")
        st.write(f"- Cuplu maxim: {specs['Cuplu maxim']} Nm")
        st.write(f"- Autonomie mod electric (WLTP): {specs['Autonomie mod electric (WLTP)']} km")
        st.markdown('</div>', unsafe_allow_html=True)

with cols[2]:  # BEV
    st.subheader("BEV")
    if st.checkbox("Adaugă BEV", key="bev_check"):
        model = st.selectbox("Selectează autovehicul BEV", options=list(modele_vehicule["BEV"].keys()))
        vehicule_selectate["BEV"] = {"model": model}
        
        # Afișare specificații tehnice
        specs = specs_tehnice["BEV"][model]
        st.write("**Specificații tehnice vehicul selectat:**")
        st.write(f"- Perioadă fabricație: {specs['Perioadă fabricație']}")
        st.write(f"- Consum (WLTP): {specs['Consum (WLTP)']} kWh/100km")
        st.write(f"- Capacitate baterie (utilizabilă): {specs['Capacitate baterie (utilizabilă)']} kWh")
        st.write(f"- Masă proprie: {specs['Masă proprie']} kg")
        st.write(f"- Putere maximă: {specs['Putere maxima']} kW")
        st.write(f"- Cuplu maxim: {specs['Cuplu maxim']} kW")
        st.write(f"- Autonomie (WLTP): {specs['Autonomie (WLTP)']} km")
        st.markdown('</div>', unsafe_allow_html=True)

with cols[3]:  # FCEV
    st.subheader("FCEV")
    if st.checkbox("Adaugă FCEV", key="fcev_check"):
        model = st.selectbox("Selectează autovehicul FCEV", options=list(modele_vehicule["FCEV"].keys()))
        
        tip_hidrogen = st.radio("Tip hidrogen", 
                                options=list(emisii_hidrogen.keys()),  
                                key=f"hidrogen_{model}")
        
        vehicule_selectate["FCEV"] = {
            "model": model,
            "tip_hidrogen": tip_hidrogen
        }
        
        # Afișează emisiile per kg H₂
        st.markdown(f" **Emisii CO₂ hidrogen {tip_hidrogen}:** {emisii_hidrogen[tip_hidrogen]} g CO₂ / kg H₂")

        # Afișare specificații tehnice
        specs = specs_tehnice["FCEV"][model]
        st.write("**Specificații tehnice vehicul selectat:**")
        st.write(f"- Perioadă fabricație: {specs['Perioadă fabricație']}")
        st.write(f"- Consum: {specs['Consum']} kg/100km")
        st.write(f"- Capacitate rezervor hidrogen: {specs['Capacitate rezervor hidrogen']} kg")
        st.write(f"- Masă proprie: {specs['Masă proprie']} kg")
        st.write(f"- Putere maximă: {specs['Putere maxima']} kW")
        st.write(f"- Cuplu maxim: {specs['Cuplu maxim']} Nm")
        st.markdown('</div>', unsafe_allow_html=True)

# 3. Parametri comuni
distanta = st.slider("Distanță parcursă [km]", 10, 100, 100, key="distanta_comp")

# 4. Calcule și afișare rezultate
if vehicule_selectate:
    st.header("Rezultate emisii CO₂")
    
    # Calcul emisii pentru fiecare vehicul
    rezultate = {}
    for tip_vehicul, config in vehicule_selectate.items():
        emisii = calculeaza_emisii(
            tip_vehicul=tip_vehicul,
            model=config["model"],
            tara=tara_selectata,
            distanta=distanta,
            **{k:v for k,v in config.items() if k != "model"}
        )
        rezultate[f"{tip_vehicul} - {config['model']}"] = emisii
    
    # Creare DataFrame pentru afișare
    df = pd.DataFrame.from_dict(rezultate, orient='index')
    st.table(
    df.style
    .format("{:.0f} gCO₂")
    .set_properties(**{
        'background-color': 'white',
        'color': 'black',
        'text-align': 'center'  
    })
)
    # Grafic comparație
    fig = go.Figure()
    
    # Culori distincte pentru fiecare vehicul
    culori = px.colors.qualitative.Plotly
    
    for i, (vehicul, emisii) in enumerate(rezultate.items()):
        fig.add_trace(go.Bar(
            x=["Well-to-Tank", "Tank-to-Wheel", "Well-to-Wheel"],
            y=[emisii["Well-to-Tank"], emisii["Tank-to-Wheel"], emisii["Total"]],
            name=vehicul,
            marker_color=culori[i % len(culori)],
            text=[f"{val:.0f}g" for val in [emisii["Well-to-Tank"], emisii["Tank-to-Wheel"], emisii["Total"]]],
            textposition='inside',
            textfont=dict(color='black')
        ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title=f"Comparație emisii CO₂ Well-to-Wheel pe distanța de {distanta}km în {tara_selectata}",
   	xaxis_title_font=dict(color='black', size=20),        
        yaxis_title="Emisii CO₂ [g]",
   	yaxis_title_font=dict(color='black', size=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=17),
 	xaxis=dict(
        	tickfont=dict(color='black', size=20)
    	),
    	yaxis=dict(
       		tickfont=dict(color='black', size=16)
    	),
        legend=dict(
            font=dict(color='black', size=17),
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ),
        height=600,
        margin=dict(l=50, r=50, b=100, t=100, pad=4)
    )
    
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Niciun vehicul selectat")

st.markdown(
    """
    <div style="
        display: flex;
        justify-content: center;
        margin: 50px 0 20px 0;
        width: 100%;
    ">
    """, 
    unsafe_allow_html=True
)

try:
    st.image("sigla_ARMM.png", width=150)
except:
    st.warning("Sigla ARMM nu a fost găsită")

st.markdown("</div>", unsafe_allow_html=True)