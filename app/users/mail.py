from flask_mail import Message

RECIP = 'admin@gmail.com'
ADDRESS = 'http://localhost:5000'

def msgr(user, incentives, sub='New Incentive Request',
         recip=[RECIP]):
    """
    Send a new incentive email
    """

    msg = Message(subject=sub, recipients=recip, reply_to=user.email)
    msg.body = """New Incentive Request From: %s %s\n
    Date: %s\n
    Payable To: %s\n
    Client: %s\n
    Opp Name: %s\n
    Project#: %s\n
    PO#: %s\n
    Amount: $%s\n
    Requested By: %s""" % (user.name, user.email, incentives.date,
                           incentives.payable_to, incentives.client,
                           incentives.opp_name, incentives.dec_project,
                           incentives.po_num, incentives.ammount,
                           incentives.requested_by)
    msg.html = """<b>New Incentive Request From: %s %s</b>
    <br/><br/>
    <table style="text-align: left;">
    <tr><th>Date:</th><td>%s</td></tr>
    <tr><th>Payable To:</th><td>%s</td></tr>
    <tr><th>Client:</th><td>%s</td></tr>
    <tr><th>Opp Name:</th><td>%s</td></tr>
    <tr><th>Project#:</th><td>%s</td></tr>
    <tr><th>PO#:</th><td>%s</td></tr>
    <tr><th>Amount:</th><td>%s</td></tr>
    <tr><th>Requested By:</th><td>%s</td></tr>
    </table>""" % (user.name, user.email, incentives.date,
                   incentives.payable_to, incentives.client,
                   incentives.opp_name, incentives.dec_project,
                   incentives.po_num, incentives.ammount,
                   incentives.requested_by)
    return msg


def reset_msg(user, token, sub="Incentives Password Reset"):
    """
    Password reset email
    """
    msg = Message(subject=sub, recipients=[user.email])
    msg.body = """A Password reset has been requested. If you did not request a
    reset then please disregard this email.\n\nPlease click this link to reset
    your password: %s/reset/id/%s""" % (ADDRESS, token)
    msg.html = """<p><b>A password reset has been requested.</b><br/>
    If you did not request a reset then please disregard this email.</p>
    <p><b>Please <a href='%s/reset/id/%s' target='_blank'>
    CLICK HERE</a> to reset your password</b></p>""" % (ADDRESS, token)
    return msg
