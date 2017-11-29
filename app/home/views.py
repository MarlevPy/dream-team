from flask import render_template, abort
from flask_login import login_required, current_user

from . import home


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    :return:
    """
    return render_template('home/index.html', title='Welcome')


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    :return:
    """
    return render_template('home/dashboard.html', title='Dashboard')


@home.route('/admin_dashboard')
@login_required
def admin_dashboard():
    """
    Render the admin dashboard template on the /admin/dasyboard route
    Prevents non-admins from accessing the page
    :return:
    """
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title='Admin Dashboard')
