from Webscrapper import company
import requests
from bs4 import BeautifulSoup
import json


def get_to_side(selskaplist):
    global selskap
    selskap = input("selskap:")
    if selskaplist is not None:
        selskap = selskaplist
    for i in range(0, len(selskap)):
        if selskap[i] == " ":
            selskap = selskap.replace(" ", "%20")

    result = requests.get("https://www.proff.no/bransjes%C3%B8k?q=" + selskap)
    # print(result.status_code)
    # print(result.headers)
    src = result.content

    content = BeautifulSoup(src, "html.parser")

    for hit in content.findAll(attrs={"class": "addax addax-cs_hl_hit_company_name_click"}):
        strings = str(hit).split('href=')
        dummiestrings = strings[1]
        dummiestrings = dummiestrings.split('>')
        dummiestrings = dummiestrings[0].replace('"', "")
        dummiestrings = dummiestrings.replace('selskap', 'nokkeltall')
        break
    print(dummiestrings)

    return "https://www.proff.no" + dummiestrings


"""
driver = webdriver.Chrome()
driver.get(get_to_side())
"""


def write_keyvalues():
    keyvaldict = {'Totalrentabilitet': get_Totalrentabilitet(),
                  'Resultat_av_drift': get_Resultat_av_driften(),
                  'Egenkap.rentabilitet': get_Egenkapitalens_rentabilitet_for_skatt(),
                  'Likviditetsgrad': get_Likviditetsgrad(),
                  'Egenkapitalandel': get_Egenkapitalandel(), 'Gjeldsgrad': get_Gjeldsgrad()}
    selskapforjson = selskap.replace("%20", " ")
    with open(selskapforjson + "_keyvalues.json", "w") as outfile:
        json.dump(keyvaldict, outfile)


def get_Totalrentabilitet():
    ar = 2018
    totalrentabilitet = {}
    for element in company.content_nokkel.find('tr', attrs={'data-chart-title': 'Totalrentabilitet i %'}):
        for value in element:
            if "\n" not in value and isinstance(value, str):
                value = value.replace(",", ".")
                totalrentabilitet[int(ar)] = float(value)
                ar -= 1
    return totalrentabilitet


def get_Resultat_av_driften():
    ar = 2018
    resultat_av_driften = {}
    for element in company.content_nokkel.find('tr', attrs={'data-chart-title': 'Resultat av driften i %'}):
        for value in element:
            if "\n" not in value and isinstance(value, str):
                value = value.replace(",", ".")
                resultat_av_driften[int(ar)] = float(value)
                ar -= 1
    return resultat_av_driften


def get_Egenkapitalens_rentabilitet_for_skatt():
    ar = 2018
    egenkapitalens_rentabilitet_for_skatt = {}
    for element in company.content_nokkel.find('tr', attrs={'data-chart-title': 'Egenkapitalens rentabilitet før skatt i %'}):
        for value in element:
            if "\n" not in value and isinstance(value, str):
                value = value.replace(",", ".")
                egenkapitalens_rentabilitet_for_skatt[int(ar)] = float(value)
                ar -= 1
    return egenkapitalens_rentabilitet_for_skatt


def get_Likviditetsgrad():
    ar = 2018
    likviditetsgrad = {}
    for element in company.content_nokkel.find('tr', attrs={'data-chart-title': 'Likviditetsgrad'}):
        for value in element:
            if "\n" not in value and isinstance(value, str):
                value = value.replace(",", ".")
                likviditetsgrad[int(ar)] = float(value)
                ar -= 1
    return likviditetsgrad


def get_Egenkapitalandel():
    ar = 2018
    egenkapitalandel = {}
    for element in company.content_nokkel.find('tr', attrs={'data-chart-title': 'Egenkapitalandel i %'}):
        for value in element:
            if "\n" not in value and isinstance(value, str):
                value = value.replace(",", ".")
                egenkapitalandel[int(ar)] = float(value)
                ar -= 1
    return egenkapitalandel


def get_Gjeldsgrad():
    ar = 2018
    gjeldsgrad = {}
    for element in company.content_nokkel.find('tr', attrs={'data-chart-title': 'Gjeldsgrad'}):
        for value in element:
            if "\n" not in value and isinstance(value, str):
                value = value.replace(",", ".")
                gjeldsgrad[int(ar)] = float(value)
                ar -= 1
    return gjeldsgrad

