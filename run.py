#!/usr/bin/env python3

from lib import config
from lib import mail
from lib import tpl
from lib import unifi 
from lib import tools
from lib import language

def main():
    cfg = config.load()
    api = unifi.Session(
        server = cfg['unifi']['server'],
        username = cfg['unifi']['username'], 
        password = cfg['unifi']['password'],
        site = cfg['unifi']['siteid']
    )

    for domain in cfg['domains']:

        domainchanged = False

        for client in domain['clients']:

            expired = tools.IsVoucherExpired(client)
            if expired:
                new_expire_date = tools.GetExpireDate(client)
                
                print(f"Create voucher for {client['lastname']} {client['firstname']}")
                # Create

                voucher = api.createvoucher(
                    quota = client['quota'],
                    up = client['upload_limit_mbit'],
                    down = client['download_limit_mbit'],
                    bytes = client['datalimit_mb'],
                    note = client['mail'],
                    n = 1,
                    expire_number = client['expire'],
                    expire_unit = client['expire_unit'],
                )

                voucher = f"{voucher[:-5]}-{voucher[-5:]}"
                print(f"Voucher {voucher} for {client['lastname']} {client['firstname']} created")

                # Inform
                print(f"Inform user {client['lastname']} {client['firstname']} with voucher details")

                lang = language.load(client)

                subject = lang['voucher']['subject']

                params = {
                    'title': subject,
                    'firstname': client['firstname'],
                    'lastname': client['lastname'],
                    'voucher': voucher,
                    'expire': client['expire'],
                    'expire_unit': client['expire_unit'],
                    'expire_date': new_expire_date,
                    'quota': client['quota'],
                    'datalimit': client['datalimit_mb'],
                    'download_limit': client['download_limit_mbit'],
                    'upload_limit': client['upload_limit_mbit'],
                    'lang': lang['voucher']
                }

                html = tpl.build('voucher.html', params)

                mail.send( 
                    server = cfg['smtp']['server'],
                    port = cfg['smtp']['port'],
                    sender = cfg['smtp']['sender'],
                    receiver = client['mail'],
                    subject = subject,
                    body = html
                )

                client['expiredate'] = new_expire_date.isoformat()
                client['lastcreationdate'] = tools.DateTimeNowToISODate()
                config.save(cfg)
                domainchanged = True
            else:
                print(f"Voucher for {client['lastname']} {client['firstname']} is valid until {tools.GetExpireDate(client)}")

        if domainchanged:
            print(f"*** Domain { domain['name'] } changed => notify Administrators ***")

            for client in domain['clients']:
                if client.get('admin'):

                    lang = language.load(client)
                    
                    subject = lang['list']['subject']

                    params = {
                        'title': subject,
                        'domain': f"{ domain['name'] } ({ domain['id'] })",
                        'lang': lang['list'],
                        'clients' : domain['clients']
                    }

                    html = tpl.build('list.html', params)

                    mail.send( 
                        server = cfg['smtp']['server'],
                        port = cfg['smtp']['port'],
                        sender = cfg['smtp']['sender'],
                        receiver = client['mail'],
                        subject = subject,
                        body = html
                    )

        else:
            print(f"*** Domain { domain['name'] } didn't changed ***") 
        
if __name__ == "__main__":
    main()