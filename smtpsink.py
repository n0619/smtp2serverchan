from datetime import datetime
import pytz
from time import sleep
import asyncore
from smtpd import SMTPServer
import socket
import requests
# from pushover_credentials import TOKEN, USER
import threading
from email.parser import BytesParser
from email.header import decode_header
import quopri
import base64



TOKEN = "SCT78986TpFUyJlwxmn7rMLYcjK5wGJnI"
wtapi = requests.get("http://worldtimeapi.org/api/ip")
tz = pytz.timezone(wtapi.json()["timezone"])
#tz = pytz.timezone('Europe/Stockholm')

class EmlServer(SMTPServer):
    print('Ready!!')
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        datevar = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('Message was recived ' + datevar)
        # data1 = quopri.decodestring(data)
        self.data = BytesParser().parsebytes(data)
        self.title = decode_header(self.data['Subject'])[0][0]
        if isinstance(self.title,bytes):
            self.title = self.title.decode(decode_header(self.data['Subject'])[0][1]) 
        self.desp = self.data.get_payload(decode=True).decode() 
        print(self.title)
        thread = threading.Thread(target=self.pushover, args=())
        thread.daemon = True
        thread.start()
        print('Handling Done! Replying 250 to client')

    def pushover(self):

        h = datetime.now().strftime('%H')
        if int(h) < 7:
            print('delaying...')
            sleephour = 7-int(h)
            sleep(sleephour*60*60)
        elif int(h) > 22:
            print('delaying...')
            sleep(8*60*60)
        print('Sending message!')
        requests.get(f'https://sctapi.ftqq.com/{TOKEN}.send?title={self.title}&desp={self.desp}')

def run():
    print(socket.gethostbyname(socket.gethostname()))
    EmlServer((socket.gethostbyname(socket.gethostname()), 10025) , None, enable_SMTPUTF8=True,decode_data=False)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    run()

'''
Message was recived 2022-02-27 20:40:10
error: uncaptured python exception, closing channel <smtpd.SMTPChannel connected 127.0.0.1:57946 at 0x1539b2c69b50> (<class 'TypeError'>:parsestr() missing 1 required positional argument: 'text' [/usr/lib64/python3.9/asyncore.py|read|83] [/''
'''