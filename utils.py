from requests import get, post
from json import dumps, loads
import database
import datetime
from login import login

CHAT_ID = '1457226514'

# token validation
def check_token(token):
    url = 'https://prd.mhrs.gov.tr/api/yonetim/genel/il/selectinput-tree'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+token
    }
    r = get(url, headers=headers)
    data = r.content.decode('utf-8')
    if type(loads(data)) == dict:
        return False
    else:    
        return True

def get_cities(token):
    url = 'https://prd.mhrs.gov.tr/api/yonetim/genel/il/selectinput-tree'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+token,
    }
    r = get(url, headers=headers)
    return r.content.decode('utf-8')

def get_districts(token, code):
    url = 'https://prd.mhrs.gov.tr/api/yonetim/genel/ilce/selectinput/{}'.format(code)
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+token,
    }
    r = get(url, headers=headers)
    return r.content.decode('utf-8')

def get_clinics(token, city, district):
    url = 'https://prd.mhrs.gov.tr/api/kurum/kurum/kurum-klinik/il/{}/ilce/{}/kurum/-1/aksiyon/200/select-input'.format(city, district)
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+token,
    }
    r = get(url, headers=headers)
    return r.content.decode('utf-8')

def get_hospitals(token, city, district, clinic):
    url = 'https://prd.mhrs.gov.tr/api/kurum/kurum/kurum-klinik/il/{}/ilce/{}/kurum/-1/klinik/{}/ana-kurum/select-input'.format(city, district, clinic)
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+token,
    }
    r = get(url, headers=headers)
    return r.content.decode('utf-8')

def get_surgeries(token, hospital, clinic):
    url = 'https://prd.mhrs.gov.tr/api/kurum/kurum/muayene-yeri/ana-kurum/{}/kurum/-1/klinik/{}/select-input'.format(hospital, clinic)
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+token,
    }
    r = get(url, headers=headers)
    return r.content.decode('utf-8')

def get_doctors(token, hospital, clinic):
    url = 'https://prd.mhrs.gov.tr/api/kurum/hekim/hekim-klinik/hekim-select-input/anakurum/{}/kurum/-1/klinik/{}'.format(hospital, clinic)
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+token,
    }
    r = get(url, headers=headers)
    return r.content.decode('utf-8')

def get_latest_appointment(token):
    url = 'https://prd.mhrs.gov.tr/api/kurum/randevu/slot-sorgulama/en-gec-gun/by-aksiyon?aksiyonId=200'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+token,
    }
    r = get(url, headers=headers)
    return r.content.decode('utf-8')

def search_appointments(token, city, district, clinic, hospital, surgery, doctor, start, end):
    url = 'https://prd.mhrs.gov.tr/api/kurum-rss/randevu/slot-sorgulama/arama'
    headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "tr-TR",
    "access-control-allow-credentials": "true",
    "access-control-allow-headers": "Authorization,Content-Type, Accept, X-Requested-With, remember-me",
    "access-control-allow-methods": "DELETE, POST, GET, OPTIONS",
    "access-control-allow-origin": "*",
    "access-control-max-age": "3600",
    "authorization": "Bearer {}".format(token),
    "content-type": "application/json",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Brave\";v=\"128\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "Referer": "https://mhrs.gov.tr/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  }
    """payload = {'aksiyonId':'200', 
               'cinsiyet':'F', 
               'mhrsHekimId':doctor, 
               'mhrsIlId':city, 
               'mhrsIlceId':district, 
               'mhrsKlinikId':clinic, 
               'mhrsKurumId':hospital, 
               'muayeneYeriId':surgery, 
               'tumRandevular':False,
               'ekRandevu':True, 
               'randevuZamaniList':[], 
               'baslangicZamani':'{} 00:00:00'.format(start),
               'bitisZamani':'{} 23:59:59'.format(end)}"""

    payload = "{" + "\"aksiyonId\":\"200\",\"cinsiyet\":\"F\",\"mhrsHekimId\":{},\"mhrsIlId\":{},\"mhrsIlceId\":{},\"mhrsKlinikId\":{},\"mhrsKurumId\":{},\"muayeneYeriId\":{},\"tumRandevular\":false,\"ekRandevu\":true,\"randevuZamaniList\":[],\"baslangicZamani\":\"{}\",\"bitisZamani\":\"{}\"".format(doctor, city, district, clinic, hospital, surgery, start, end) + "}"

    r = post(url, headers=headers, data=payload)
    return r.content.decode('utf-8')

def slot_sorgulama(token, doctor, city, clinic, hospital):
    url = 'https://prd.mhrs.gov.tr/api/kurum-rss/randevu/slot-sorgulama/slot'
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "tr-TR",
        "access-control-allow-credentials": "true",
        "access-control-allow-headers": "Authorization,Content-Type, Accept, X-Requested-With, remember-me",
        "access-control-allow-methods": "DELETE, POST, GET, OPTIONS",
        "access-control-allow-origin": "*",
        "access-control-max-age": "3600",
        "authorization": "Bearer {}".format(token),
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Brave\";v=\"128\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "Referer": "https://mhrs.gov.tr/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    payload = "{" + "\"aksiyonId\":\"200\",\"cinsiyet\":\"F\",\"mhrsHekimId\":{},\"mhrsIlId\":{},\"mhrsKlinikId\":{},\"mhrsKurumId\":{},\"tumRandevular\":false,\"ekRandevu\":true,\"randevuZamaniList\":[]".format(doctor, city, clinic, hospital) + "}"
    r = post(url, headers=headers, data=payload)
    return r.content.decode('utf-8')
    
def make_appointment(token, start, end, cetvelId, slotId, surgery):
    url = 'https://prd.mhrs.gov.tr/api/kurum/randevu/randevu-ekle'
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "tr-TR",
        "access-control-allow-credentials": "true",
        "access-control-allow-headers": "Authorization,Content-Type, Accept, X-Requested-With, remember-me",
        "access-control-allow-methods": "DELETE, POST, GET, OPTIONS",
        "access-control-allow-origin": "*",
        "access-control-max-age": "3600",
        "authorization": "Bearer {}".format(token),
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Brave\";v=\"128\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "Referer": "https://mhrs.gov.tr/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    payload = '{' + '\"baslangicZamani\":\"{}\", \"bitisZamani\":\"{}\", \"fkCetvelId\": {}, \"fkSlotId\": {}, \"muayeneYeriId\": {}, \"randevuNotu\": \"\", \"yenidogan\": false'.format(start, end, cetvelId, slotId, surgery) + '}'
    print(payload) 
    r = post(url, headers=headers, data=payload)
    return r.content.decode('utf-8')

def check_all():
    patients = database.read_collection('patients') 
    for patient in patients:
        if not check_token(patient.to_dict()['token']):
            token = login(patient.to_dict()['username'], patient.to_dict()['password'])
            database.update_document('patients', patient.id, {'token':token})
        else:
            token = patient.to_dict()['token']
        if not patients.index(patient):
            latest_appointment = loads(get_latest_appointment(token))['data']
        #token, city, district, clinic, hospital, surgery, doctor, start, end
        appointments = loads(search_appointments(token, 
                                            patient.to_dict()['city'],
                                            '-1',
                                            '211',
                                            patient.to_dict()['hospital'],
                                            '-1',
                                            '-1',
                                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                            (datetime.datetime.now() + datetime.timedelta(days=int(latest_appointment))).strftime('%Y-%m-%d %H:%M:%S')))['data']['hastane']
       
        print(len(appointments))

        for appointment in appointments:
            doctor = appointment['hekim']['mhrsHekimId']
            hospital = appointment['kurum']['mhrsKurumId']
            city = appointment['kurum']['ilIlce']['mhrsIlId']
            # district = appointment['kurum']['ilIlce']['mhrsIlceId']
            # surgery = appointment['muayeneYeri']['id']
            # action = appointment['aksiyon']['id']
            # start = appointment['baslangicZamaniStr']['date']
            # end = appointment['bitisZamaniStr']['date']
            clinic = appointment['klinik']['mhrsKlinikId']
            
            print('RANDEVU:')
            print('doctor ' , doctor)
            print('hospital ' , hospital)
            print('city ' , city)
            # print('district ' , district)
            # print('surgery ' , surgery)
            # print('action ' , action)
            # print('start ' , start)
            # print('end ' , end)
            print('clinic ' , clinic)

            slots = slot_sorgulama(token, doctor, city, clinic ,hospital)
            """slot = loads(slots)['data'][0]['hekimSlotList'][0]['muayeneYeriSlotList'][0]
            surgery = slot['muayeneYeri']['id']
            slots = slot['saatSlotList'][0]['slotList']

            available = False
            for slot in slots:
                print(slot['bos'])
                if slot['bos']:
                    available = True
                    break
            if not available:return"""

            slots = loads(slots)['data'][0]['hekimSlotList']

            available = False
            for doctor_i in slots:
                if doctor_i['bos']:
                    for surgery_i in doctor_i['muayeneYeriSlotList']:
                        if surgery_i['bos']:
                            surgery = surgery_i['muayeneYeri']['id']
                            for hour_i in surgery_i['saatSlotList']:
                                if hour_i['bos']:
                                    for slot in hour_i['slotList']:
                                        if slot['bos']:
                                            available = True
                                            break
                                    break
                            break
                    break

            if not available:
                return
            start = slot['baslangicZamani']
            end = slot['bitisZamani']
            cetvelId = slot['fkCetvelId']
            slotId = slot['id']

            print('start: ', start)
            print('end: ', end)
            print('cetvel: ', cetvelId)
            print('slot: ', slotId)
            print('surgery: ', surgery)

            res = make_appointment(token, start, end, cetvelId, slotId, surgery)
            print(res['infos'][0]['mesaj'])
            #'id', 'fkCetvelId', 'baslangicZamani', 'bitisZamani', 'cetvelIsKurallari', 'slot', 'bos', 'isKurali', 'kapasite', 'bosKapasite', 'ek', 'uygunRandevuGecmisSlot', 'rezerveTuruData', 'uzaktanDegerlendirmeVarmi', 'bitisZamanStr', 'kalanGunMesaj', 'baslangicZamanStr'"
        
        #send message
        

if __name__ == '__main__':
    check_all()
