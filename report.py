# imports for preparing data
import pandas as pd
from trudeau import get_data
from trudeau import utils

# imports for sending email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders

# laoding data
df = pd.read_csv('trudeau.csv')
# updating data
df = get_data.update_articles(df, 'Trudeau', '91f67b2a-520b-4f9f-a4ca-edcb0d610454')
df_grouped = get_data.group_days(df)

# get number of yesterday's published articles
count = df_grouped.iloc[-1].numberOfArticles
# get average of articles published from 01.01.2018
avg = utils.df_metrics(df_grouped, 'numberOfArticles')[0]
avg = round(avg, 4)

# saving png of plot of articles published over time
utils.save_graphic('articles_over_time', df_grouped)

# sending email
# specifying sender and receiver email and server credentials
from_addr = 'felix.blochwitz@gmail.com'
password = 'pdjoutplcjyelzxr'
to_addr = 'felix.blochwitz@gmail.com'
smtp_server = 'smtp.gmail.com'

# creating email
msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = 'Trudeau Report'

# creating the message content
msg_content = MIMEText(
    f'<html><body><h1>Trudeau Report</h1>' +
        '<p>Diese Email ist der tägliche Report über die Veröffentlichungen von Artikeln über Justin Trudeau auf der The Guardian Website.</p>' +
        f'<p>Gestern wurde {count} neue Artikel über Justin Trudeau auf The Guardian veröffentlicht. Durchschnittlich werden seit dem 01.01.2018 <br> täglich {avg} Artikel über Justin Trudeau auf theguardian.com veröffentlicht.</p>' +
        '<p>Die Anzahl der Veröffentlichungen im Zeitverlauf seit dem 01.01.2018 ist in der untenstehenden Grafik veranschaulicht.</p>' +
        '<p><img src="cid:0"></p>' +
        '<p>Im Anhang dieser Mail befinden sich Datensatz, der alle Artikel über Justin Trudeau seit dem 01.01.2018 anthält, sowie ein Datensatz <br>' +
        'der die Anzahl aller täglich veröffentlichten Artikel seit 01.01.2018 enthält, als CSV-Dateien.</p>' + 
        '</body></html>', 'html', 'utf-8')

msg.attach(msg_content)

# creating image attachment
with open('articles_over_time.png', 'rb') as f:
    mime = MIMEBase('image', 'png', filename='articles_over_time.png')
    mime.add_header('Content-ID', '<0>')
    mime.set_payload(f.read())
    encoders.encode_base64(mime) 
    msg.attach(mime)

# attaching csv files to email
for dataset in ['trudeau.csv', 'trudeau_grouped.csv']:
    with open(dataset, 'rb') as f:
        msg.attach(MIMEApplication(f.read(), Name=dataset))
    encoders.encode_base64(mime) 
    msg.attach(mime)

# sending mail
import smtplib
server = smtplib.SMTP(smtp_server, 587)
server.starttls()
server.set_debuglevel(0)
server.login('felix.blochwitz@gmail.com', password)
server.sendmail(from_addr, to_addr, msg.as_string())
server.quit()