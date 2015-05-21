from flask_mail import Message
from app import mail

def msgr(user, incentive, sub='New Incentive Request',
recip=['rsiemens@decipherinc.com']):
  msg = Message(subject=sub, sender=user.email, recipients=recip, reply_to=user.email)
  msg.body = """New Incentive Request From: %s %s\n
    Date: %s\n
    Payable To: %s\n
    Client: %s\n
    Opp Name: %s\n
    Decipher Project#: %s\n
    PO#: %s\n
    Amount: $%s\n
    Requested By: %s""" % (u.name, u.email, incentives.date, incentives.payable_to, incentives.client, incentives.opp_name, incentives.dec_project, incentives.po_num, incentives.ammount, incentives.requested_by)
    
    msg.html = """<b>New Incentive Request From: %s %s</b>
    <br/><br/>
    <table style="text-align: left;">
    <tr><th>Date:</th><td>%s</td></tr>
    <tr><th>Payable To:</th><td>%s</td></tr>
    <tr><th>Client:</th><td>%s</td></tr>
    <tr><th>Opp Name:</th><td>%s</td></tr>
    <tr><th>Decipher Project#:</th><td>%s</td></tr>
    <tr><th>PO#:</th><td>%s</td></tr>
    <tr><th>Amount:</th><td>%s</td></tr>
    <tr><th>Requested By:</th><td>%s</td></tr>
    </table>""" % (u.name, u.email, incentives.date, incentives.payable_to, incentives.client, incentives.opp_name, incentives.dec_project, incentives.po_num, incentives.ammount, incentives.requested_by)