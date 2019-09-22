from django.core.management.base import BaseCommand, CommandError
from django.template import loader, Context
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from ldap3 import Server, Connection, SUBTREE
import datetime

class Command(BaseCommand):
    help = 'Send mail for AD users whose password is outdated'


    def handle(self, *args, **options):

        attributes = ["PwdLastSet", "mail"]

        s = Server('ldap://10.157.251.71:3268')
        c = Connection(s, user='ematcrh\\sa_qlickview', password='L0ngf0rd15', auto_bind=True)
        t = loader.get_template("raporty/ad_passwords_mail.html")

        with c:
            c.search('OU=Polbruk,OU=Poland,OU=CRH Users,DC=EMAT,DC=CRH,DC=NET','(&(objectclass=*))', SUBTREE, attributes = attributes) 
            for row in c.response:
                mail = row["attributes"]["mail"]
                if '@' in mail and '.' in mail:
                    ldate = row["attributes"]["PwdLastSet"]
                    datetime.datetime.now()
                    if ldate and type(ldate) == datetime.datetime:
                        dt = (datetime.date.today() - ldate.date()).days
                        if dt>31 and  dt<100:
                            x = mail.split('@')[0].split('.')
                            login = x[0][0]+x[1]                            
                            c = Context({'mail': mail, 'ldate': ldate, 'login': login.lower() })
                            MAIL_CONTENT = t.render(c)
                            #mail_to = ['slawomir.cholaj@polbruk.pl',]
                            mail_to = [mail.lower(),]
                            mail = EmailMultiAlternatives("Powiadomienie o konieczności zmiany hasła", "", to=mail_to)
                            mail.attach_alternative(MAIL_CONTENT, "text/html")            
                            mail.send()
