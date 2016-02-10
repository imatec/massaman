# -*- coding: utf-8 -*-
import logging
from flask import render_template, current_app, request, redirect, url_for, \
    flash, jsonify
from flask.ext.login import login_user, logout_user, login_required, current_user
from .models import User
from . import users_bp
from .forms import LoginForm, UserFormAdd, UserFormEdit
from .. import db
from ..helpers import flash_errors


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    # if not current_app.config['DEBUG'] and not current_app.config['TESTING'] \
    #         and not request.is_secure:
    #     return redirect(url_for('.login', _external=True, _scheme='https'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash(u"Usuario o contraseña invalidos.")
            return redirect(url_for('.login'))

        if not user.is_admin:
            flash(u"Usuario o contraseña invalidos..")
            return redirect(url_for('.login'))

        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('.index'))
    return render_template('users/login.html', form=form)


@users_bp.route('/')
def index():
    if current_user is not None and current_user.is_authenticated:
        # TODO: get redirect_url_for from CONFIG, else render welcome
        return render_template('users/welcome.html')
    else:
        return redirect(url_for('users.login'))


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Usted ha salido.')
    return redirect(url_for('.index'))


@users_bp.route('/users')
@login_required
def users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by('rut').paginate(
        page, per_page=20,
        error_out=False)
    users_list = pagination.items
    return render_template('users/users.html', users=users_list,
        pagination=pagination)


@users_bp.route('/user/', methods=['GET', 'POST'], defaults={'id': None})
@users_bp.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def user_edit(id=None):
    if id:
        form = UserFormEdit()
    else:
        form = UserFormAdd()
    # form.wristband_id.choices = [(wb.id, wb.name) for wb in Wristband.query.order_by('id')]

    if request.method == 'POST':
        if id:
            user = User.query.get_or_404(id)
        else:
            user = User()

        if form.validate_on_submit():
            try:

                # if id:
                #     User.validate_wristband(form.wristband_id.data, id)
                    # else:
                #     User.validate_wristband(form.wristband_id.data)

                form.to_model(user)
                db.session.add(user)
                db.session.commit()
                flash('Usuario editado correctamente.')

            except Exception as e:
                logging.exception(e)
                flash('Ha ocurrido un problema con la solicitud.')
                return render_template('users/edit_user.html', form=form)

            return redirect(url_for('.users'))

        else:
            flash_errors(form)
            return render_template('users/edit_user.html', form=form)

    elif request.method == 'GET':
        if id:
            user = User.query.get_or_404(id)
            form.from_model(user)
        return render_template('users/edit_user.html', form=form)


@users_bp.route('/user/<int:id>', methods=['DELETE'])
@login_required
def user_delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': 'OK'})