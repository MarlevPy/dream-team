from flask import redirect, url_for, abort, render_template, flash
from flask_login import login_required, current_user

from ..models import Department, Role, Employee
from . import admin
from .. import db
from .forms import DepartmentForm, RoleForm, EmployeeAssignForm


def check_admin():
    """"
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@admin.route('/department', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    :return:
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title='Departments')


@admin.route('/department_add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add department to the database
    :return:
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)

        try:
            # add department to database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added {}.'.format(form.name.data))
        except:
            # in case department already exists
            flash('Error: department name already exists.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action='Add',
                           add_department=add_department, form=form,
                           title='Add Department')


@admin.route('/department/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    :param id: Department id
    :return:
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the "{}" department'.format(form.name.data))

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.name.data = department.name
    form.description.data = department.description
    return render_template('admin/departments/department.html', action='Edit',
                    add_department=add_department, form=form,
                           title='Edit Department')


@admin.route('/department/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department
    :param id: Department id
    :return:
    """
    check_admin()

    department = Department.query.get_or_404(id)
    department_name = department.name
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the "{}" department.'.format(department_name))

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title='Delete Department')


@admin.route('/roles')
@login_required
def list_roles():
    """
    List all roles
    :return:
    """
    check_admin()

    roles = Role.query.all()

    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    :return:
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)
        try:
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added the "{}" role.'.format(form.name.data))
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    #load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add role')

@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    :return:
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the "{}" role.'.format(form.name.data))

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.name.data = role.name
    form.description.data = role.description

    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Edit role')


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role
    :param id: Role id
    :return:
    """
    check_admin()

    role = Role.query.get_or_404(id)
    role_name = role.name
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the "{}" role.'.format(role_name))

    return redirect(url_for('admin.list_roles'))

    return render_template(title='Delete Role')


@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    :return:
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a employee
    :param id: Employee id
    :return:
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm()
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned "{}" as department and "{}" as role to {} {}.'.
              format(employee.department, employee.role, employee.first_name, employee.last_name))

        # redirect to the employees page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')
