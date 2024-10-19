from requests import post
from json import dumps, loads

def login(username, password):
    print('login geldi')
    url = "https://prd.mhrs.gov.tr/api/vatandas/login"
    payload = {'kullaniciAdi': username, 'parola':password, 'islemKanali':'VATANDAS_WEB', 'girisTipi':'PAROLA', 'captchaKey':None}
    headers= {
        "accept": "application/json, text/plain, */*",
        "accept-language": "tr-TR",
        "access-control-allow-credentials": "true",
        "access-control-allow-headers": "Authorization,Content-Type, Accept, X-Requested-With, remember-me",
        "access-control-allow-methods": "DELETE, POST, GET, OPTIONS",
        "access-control-allow-origin": "*",
        "access-control-max-age": "3600",
        "content-type": "application/json",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Brave\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "Referer": "https://mhrs.gov.tr/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    r = post(url, data=dumps(payload), headers=headers)
    print('istek gönderildi')
    data = loads(r.content.decode('utf-8'))
    if data['success']:
        print('başarılı')
        print(data['data']['jwt'])
        return data['data']['jwt']
    else:
        print('başarısız')
        return False

if __name__ == '__main__':
    print(login(38198162200, 'Vanvanvan65'))
