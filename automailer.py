import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

'''
Condition: the dataframes in the script are globally defined
'''
def send_mail(mail_sub: str, emailfrom:str, to_list, username:str, password: str)


    subject = mail_sub
    #emailfrom = <sender's id>
    #to_list = [] #list of recivers
    emailto = ",".join(to_list)
    
    html1 = """
    <html>
    
    <head>
    <style>  
     table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
      th, td {{ padding: 5px; }}
    </style>
    </head>
    
    <body>
    <p>Hi,</p>
    <p>PFB the data</p>
    </body>
    
    </html>
    """
    html2 = """
    <html>
    <head>
    <style>  
     table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
      th, td {{ padding: 5px; }}
    </style>
    </head>
    <body>
    <p>Diff data below:</p>
    </body></html>
    """
    
    html3 = """
    <html>
    <body>
    <p>Data Download link: </p>
    <p>Regards,</p>
    <p>Vidushi</p>
    </body></html>
    """
    
    message = MIMEMultipart()
    message['Subject'] = "mail subject"
    message['From'] = emailfrom
    message['To'] = emailto
    
    message.attach(MIMEText(html1,'html')) ## attaching the html snippet
    ## attaching the dataframe table in html body
    df_mail_html1=df_mail1.to_html(buf=None, columns=None, col_space=None, header=True, index=True, na_rep='NaN', formatters=None, float_format=None, sparsify=None, index_names=True, justify=None, bold_rows=True, classes=None, escape=True, max_rows=None, max_cols=None, show_dimensions=False, notebook=False, decimal='.', border=None)
    
    message.attach(MIMEText(html2,'html'))
    df_mail_html2=df_mail2.to_html(buf=None, columns=None, col_space=None, header=True, index=True, na_rep='NaN', formatters=None, float_format=None, sparsify=None, index_names=True, justify=None, bold_rows=True, classes=None, escape=True, max_rows=None, max_cols=None, show_dimensions=False, notebook=False, decimal='.', border=None)
    
    message.attach(MIMEText(html3,'html'))
    
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.ehlo()
    server.login(username,password)
    server.send_message(message)
    server.quit()
    
    ###############################
