from telebot import TeleBot
from telebot import types
from json import load, dump
import utils
import database
import check
import login

# appointment data
class glob():
    def __init__(self):
        self.data = {}
var = glob()

class Bot(TeleBot):
    def __init_(self, token):
        super().__init__(token)
    
    def webhook(self, webhook_url):
        self.remove_webhook()
        self.set_webhook(url = webhook_url) 

    def add(self, message):
        self.send_message(message['chat']['id'], 'Tc no giriniz')
        var.data[str(message['chat']['id'])] = {}
        var.data[str(message['chat']['id'])]['state'] = 'tc_input'

    def remove(self, message):
        self.send_message(message['chat']['id'], 'Tc no giriniz')
        var.data[str(message['chat']['id'])] = {}
        var.data[str(message['chat']['id'])]['state'] = 'tc_input_remove'
        print('remove')

    def array(self, message):
        snapshots = database.read_collection('patients')
        print('array')

    def text(self, message):
        if not str(message['chat']['id']) in var.data.keys():
            var.data[str(message['chat']['id'])] = {}
        # tc gir
        if not 'state' in var.data[str(message['chat']['id'])].keys():
            var.data[str(message['chat']['id'])]['state'] = ''
        if var.data[str(message['chat']['id'])]['state'] == 'tc_input':
            res = check.tc(message['text'])
            if res:
                var.data[str(message['chat']['id'])]['tc'] = res
                self.send_message(message['chat']['id'], 'Parola giriniz')
                var.data[str(message['chat']['id'])]['state'] = 'password_input'
            else:
                self.send_message(message['chat']['id'], 'Geçersiz tc no, tekrar giriniz')

        # hasta sil
        elif var.data[str(message['chat']['id'])]['state'] == 'tc_input_remove':
            patient = database.document_query('patients', 'username', message['text'])
            # hasta bulundu
            if patient:
                database.delete_document('patients', patient[0].id)
                self.send_message(message['chat']['id'], 'Hasta kaydı silindi')
            # bulunamadı
            else:
                self.send_message(message['chat']['id'], 'Hasta kaydı bulunamadı')
                var.data[str(message['chat']['id'])]['state'] = 'none'

        # parola gir
        elif var.data[str(message['chat']['id'])]['state'] == 'password_input':
            var.data[str(message['chat']['id'])]['password'] = message['text']
            token = login.login(var.data[str(message['chat']['id'])]['tc'], var.data[str(message['chat']['id'])]['password'])
            if token:
                database.add_document('patients', {'username':var.data[str(message['chat']['id'])]['tc'], 'password':var.data[str(message['chat']['id'])]['password'], 'token':token})
                self.send_message(message['chat']['id'], 'Giriş başarılı.')
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                markup.add(types.KeyboardButton('İstanbul'))
                markup.add(types.KeyboardButton('Edirne Sultan Murat'))
                markup.add(types.KeyboardButton('Çorlu Devlet'))
                markup.add(types.KeyboardButton('Çerkezköy Devlet'))
                markup.add(types.KeyboardButton('Tekirdağ İsmail Fehmi'))
                self.send_message(message['chat']['id'], 'Randevu nerden alınacak?', reply_markup = markup)
                var.data[str(message['chat']['id'])]['state'] = 'city'

            else:
                self.send_message(message['chat']['id'], 'Giriş yapılamadı')
                var.state = 'none'

        # il sec
        elif var.data[str(message['chat']['id'])]['state'] == 'city':
            var.data[str(message['chat']['id'])]['city'] = cities[message['text']]
            if message['text'] != 'İstanbul':
                var.data[str(message['chat']['id'])]['hospital'] = hospitals[message['text']]
            else:
                # istanbulsa her hastane okey
                var.data[str(message['chat']['id'])]['hospital'] = '-1'
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            markup.add(types.KeyboardButton('Sürekli kontrol et'))
            markup.add(types.KeyboardButton('Belirli saatte kontrol et'))
            self.send_message(message['chat']['id'], 'Randevu alım biçimi?', reply_markup = markup)
            var.data[str(message['chat']['id'])]['state'] = 'type'

        # randevu tipi
        elif var.data[str(message['chat']['id'])]['state'] == 'type':
            if message['text'] == 'Sürekli kontrol et':
                var.data[str(message['chat']['id'])]['type'] = 'loop'
                patient = database.document_query('patients', 'username', var.data[str(message['chat']['id'])]['tc'])
                data = {
                            'city': var.data[str(message['chat']['id'])]['city'],
                            'type': var.data[str(message['chat']['id'])]['type'],
                            'hospital': var.data[str(message['chat']['id'])]['hospital']
                        }
                database.update_document('patients', patient[0].id, data)
                self.send_message(message['chat']['id'], 'Hasta kaydı yapıldı')
            else:
                self.send_message(message['chat']['id'], 'Randevu tarihin ve saatini giriniz (Örn 2008-01-28 16:00)')
                var.data[str(message['chat']['id'])]['type'] = 'datetime'
                var.data[str(message['chat']['id'])]['state'] = 'datetime'

        # randevu saati
        elif var.data[str(message['chat']['id'])]['state'] == 'datetime':
            var.data[str(message['chat']['id'])]['datetime'] = message['text']
            patient = database.document_query('patients', 'username', var.data[str(message['chat']['id'])]['tc'])
            data = {
                        'city': var.data[str(message['chat']['id'])]['city'],
                        'type': var.data[str(message['chat']['id'])]['type'],
                        'hospital': var.data[str(message['chat']['id'])]['hospital'],
                        'datetime': var.data[str(message['chat']['id'])]['datetime']
                    }
            database.update_document('patients', patient[0].id, data)
            self.send_message(message['chat']['id'], 'Hasta kaydı yapıldı')

    def func(self, message):
        message = message['message']
        authentication = database.document_query('auths', 'chat_id', message['chat']['id'])
        print(message['chat']['id'])
        if not authentication:
            return
        if '/add' in message['text']:
            self.add(message)
        elif '/remove' in message['text']:
            self.remove(message)
        elif '/list' in message['text']:
            self.array(message)
        else:
            self.text(message)
