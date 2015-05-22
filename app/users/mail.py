import app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message
from app import mail



def msgr(user, incentives, sub='New Incentive Request',
recip=['rsiemens@decipherinc.com']):
  """
  Send a new incentive email
  """
  
  msg = Message(subject=sub, sender=user.email, recipients=recip, reply_to=user.email)
  msg.body = """New Incentive Request From: %s %s\n
    Date: %s\n
    Payable To: %s\n
    Client: %s\n
    Opp Name: %s\n
    Decipher Project#: %s\n
    PO#: %s\n
    Amount: $%s\n
    Requested By: %s""" % (user.name, user.email, incentives.date, incentives.payable_to, incentives.client, incentives.opp_name, incentives.dec_project, incentives.po_num, incentives.ammount, incentives.requested_by)
    
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
    </table>""" % (user.name, user.email, incentives.date, incentives.payable_to, incentives.client, incentives.opp_name, incentives.dec_project, incentives.po_num, incentives.ammount, incentives.requested_by)
  return msg
  

def reset_msg(user, sub="Decipher Incentives Password Reset", expire=100):
  """
  Password reset email
  """
  s = Serializer(app.config['SECRET_KEY'], expire)
  token = s.dumps({'user': user.id}).decode('utf-8')
  msg = Message(subject=sub, recipients=user.email)
  msg.body = """A Password reset has been requested.\n
  Please click this link to reset your password:\n
  localhost:5000/reset/id/%s""" % token
  
  