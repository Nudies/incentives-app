from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash

from app import db, mail
from app.users.security import ts
from app.users.mail import msgr, reset_msg
from app.users.models import User, Incentive
from app.users.forms import (RegisterForm, LoginForm, IncentiveForm, ResetForm,
                             NewPasswordForm, EditUserForm, ApproveForm)
from app.users.decorators import (requires_login, get_incentives, requires_admin,
                                  get_users, requires_staff, get_all_incentives,
                                  get_all_need_approval_incentives)


mod = Blueprint('users', __name__)


@mod.route('/')
@requires_login
def home():
    return render_template('users/profile.html', user=g.user)


@mod.before_request
def before_request():
    """
    Get user's profile from db before request is handled.
    """
    g.user = None
    g.incentives = None
    g.allusers = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@mod.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Welcome back, %s!' % user.name, category='success')
            return redirect(url_for('users.home'))
        flash('Email or password is wrong', category='error-message')

    return render_template('users/login.html', form=form)


@mod.route('/logout/')
def logout():
    """
    Drops user session
    """
    session.pop('user_id', None)
    flash('You were successfully logged out!', category='success')
    return redirect(url_for('users.login'))


@mod.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Registration Form
    """
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        if '@decipherinc.com' in form.email.data or '@focusvision.com' in form.email.data:
            # Create new user instance not yet stored in db
            user = User(name=form.name.data, email=form.email.data,
                        password=generate_password_hash(form.password.data))
            try:
                db.session.add(user)
                db.session.commit()
                # Log user in
                session['user_id'] = user.id
                flash('Thanks for registering, %s!' % (user.name),
                      category="success")
            except:
                flash('We had a problem registering you. If you continue to '
                      'get this message please contact your administrator.',
                      category='error-message')
                return redirect(url_for('users.register'))
            return redirect(url_for('users.home'))
        else:
            flash('We had a problem registering you. Your email domain does '
                  'not match the specified criteria.', category='error-message')
            return redirect(url_for('users.register'))

    return render_template('users/register.html', form=form)


@mod.route('/reset/', methods=['GET', 'POST'])
def reset_email():
    """
    Password Reset Email
    """
    form = ResetForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('The email %s does not exist!' % form.email.data,
                  category='error-message')
            return redirect(url_for('users.reset_email'))

        # Generate email msg and token
        token = ts.dumps(user.email, salt='recovery-key')
        msg = reset_msg(user, token)

        try:
            mail.send(msg)
            flash('A reset link has been sent to %s' % user.email,
                  category='success')
        except:
            flash('There was a error in sending you a email. If this problem '
                  'persists please contact the admin', category='error-message')

    return render_template('users/reset.html', form=form)


@mod.route('/reset/id/<token>', methods=['GET', 'POST'])
def reset_pw(token):
    """
    Password Reset
    """
    email = ts.loads(token, salt='recovery-key', max_age=86400)
    form = NewPasswordForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash('Your password has been changed for %s' % email, category='success')
        return redirect(url_for('users.login'))

    return render_template('users/newpass.html', form=form, token=token)


@mod.route('/new-incentive/', methods=['GET', 'POST'])
@requires_login
def new_incentive():
    """
    Incentive Form
    """
    form = IncentiveForm(request.form)

    if form.validate_on_submit():
        # Create new incentive request form object
        u = User.query.get(session['user_id'])
        incentives = Incentive(date=form.date.data,
                               payable_to=form.payable_to.data,
                               client=form.client.data,
                               opp_name=form.opp_name.data,
                               dec_project=form.dec_project.data,
                               po_num=form.po_num.data,
                               ammount=form.amount.data,
                               requested_by=form.requested_by.data)
        incentives.user = u
        msg = msgr(u, incentives)

        try:
            mail.send(msg)
            db.session.add(incentives)
            db.session.commit()
            flash('Incentive request submitted for project %s!' %
                  (incentives.dec_project),
                  category="success")
        except AssertionError as er:
            flash(('Failed to send mail: %s.\nIf this problem persists please '
                   'contact your admin.') % er, category="error-message")
        except:
            flash('Failed to send mail.\nIf this problem persists please '
                  'contact your admin.', category="error-message")
        return redirect(url_for('users.get_incentive'))

    return render_template('users/incentive.html', form=form, user=g.user)


@mod.route('/past-incentive/')
@requires_login
@get_incentives
def get_incentive():
    """
    Query DB for all posted incentives by user
    """
    return render_template('users/past.html',
                           user=g.user,
                           incentives=g.incentives)


@mod.route('/approve/', methods=['GET', 'POST'])
@requires_login
@requires_staff
@get_all_need_approval_incentives
def approve_incentive():
    form = ApproveForm(request.form)
    form.incentive.choices = [(i.id, i.dec_project) for i in Incentive.query
                              .filter_by(approved=False).all()[::-1]]
    if form.validate_on_submit():
        incentive = Incentive.query.filter_by(id=form.incentive.data).first()
        if form.approved.data == 2:
            incentive.approved = True
        else:
            incentive.approved = False
        incentive.approved_by = g.user.name
        db.session.commit()
        flash('%s status changed' % incentive.dec_project, category="success")
    return render_template('users/approve.html',
                           user=g.user,
                           incentives=g.incentives,
                           form=form)


@mod.route('/admin/', methods=['GET', 'POST'])
@requires_login
@requires_admin
@get_all_incentives
@get_users
def get_admin():
    """
    Expose db tables to page
    """
    form = EditUserForm(request.form)
    form.user.choices = [(u.id, u.name) for u in User.query.all()]

    if form.validate_on_submit():
        u = User.query.filter_by(id=form.user.data).first()

        if form.new_name.data:
            u.name = form.new_name.data
        if form.new_email.data:
            u.email = form.new_email.data
        if form.new_password.data:
            u.password = generate_password_hash(form.new_password.data)
        if form.new_role.data != 3:
            u.setRole(form.new_role.data)
        db.session.commit()
        flash('Info edited for %s, %s' % (u.name, u.email), category="success")

    return render_template('admin.html',
                           form=form,
                           user=g.user,
                           incentives=g.incentives,
                           allusers=g.allusers)
