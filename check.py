from json import load, loads
from datetime import datetime

def tc(text):
    text = text.strip()
    if len(text) != 11 or not text.isnumeric():
        return False
    else:
        return text

def city(text):
    cities = load(open('cities.json', 'r')) 
    for city in cities.keys(): 
        if cities[city] == text: 
            return city
    return False

def district(text, districts):
    for district in districts:
        if district['text'] == text:
            return district['value']
    if text == 'Farketmez':
        return '-1'
    return False

def clinic(text, clinics):
    for clinic in clinics:
        if clinic['text'] == text:
            return clinic['value']
    if text == 'Farketmez':
        return '-1'
    return False

def hospital(text, hospitals):
    for hospital in hospitals:
        if hospital['text'] == text:
            return hospital['value']
    if text == 'Farketmez':
        return '-1'
    return False

def surgery(text, surgeries):
    for surgery in surgeries:
        if surgery['text'] == text:
            return surgery['value']
    if text == 'Farketmez':
        return '-1'
    return False


def start(text):
    date = text.split('-')
    if len(date[0])!=4 or len(date[1])!=2 or len(date[2])!=2:
        return False
    if int(date[0]) >= datetime.now().year and int(date[1]) >= datetime.now().month and int(date[2]) >= datetime.now().day:
        return text + ' 00:00:00'
    return False

def end(text, diff):
    date = text.split('-')
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])

    date = datetime(year, month, day)
    if (date - datetime.now()).days <= diff:
        if month < 10:
            month = "0" + str(month)
        if day < 10:
            day = "0" + str(day)
        return '{}-{}-{} 23:59:59'.format(year, month, day)
