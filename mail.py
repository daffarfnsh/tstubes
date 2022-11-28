import smtplib
def test():
    server = smtplib.SMTP('smtp.gmail.com',587)
    sender = 'xsening@gmail.com'
    receiver = 'xaseya7231@xegge.com'
    server.starttls()
    server.login(sender,'ardhiqi50')
    msg = 'TEST MESSAGE EMAIL'
    server.sendmail(sender,receiver,msg)
    server.quit()
print('run function')
test()