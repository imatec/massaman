# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from ..helpers import required


class LoginForm(Form):
    username = StringField('Usuario', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField(u'Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Mantenerme conectado')
    submit = SubmitField('OK')


class UserFormEdit(Form):
    # rut = StringField('RUT', validators=[Length(1, 64)])
    # rutdv = StringField('DV', validators=[Length(1, 1)])
    password = PasswordField(u'Contraseña', validators=[DataRequired(required(u"Contraseña"))])
    name = StringField('Nombre', validators=[DataRequired(required("Nombre")), Length(1, 64)])
    is_admin = BooleanField('Es administrador', default=False)
    is_enabled = BooleanField('Habilitado', default=True)
    # wristband_id = SelectField(u'Pulsera', coerce=int)
    submit = SubmitField('Aceptar')

    def from_model(self, user):
        # self.rut.data = user.rut
        # self.rutdv.data = user.rutdv
        # self.password.data = user.password # not readable
        self.name.data = user.name
        self.is_admin.data = user.is_admin
        self.is_enabled.data = user.is_enabled
        # self.wristband_id.data = user.wristband_id

    def to_model(self, user):
        # user.rut = self.rut.data
        # user.rutdv = self.rutdv.data
        user.password = self.password.data
        user.name = self.name.data
        user.is_admin = self.is_admin.data
        user.is_enabled = self.is_enabled.data
        # user.wristband_id = self.wristband_id.data

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        return True


class UserFormAdd(UserFormEdit):
    # username = StringField('Usuario', validators=[DataRequired(req_msg("Usuario")), Length(1, 255)])
    password = PasswordField(u'Contraseña', validators=[DataRequired(required(u"Contraseña"))])

    rut = StringField('RUT', validators=[Length(1, 64)])
    rutdv = StringField('DV', validators=[Length(1, 1)])
    name = StringField('Nombre', validators=[DataRequired(required("Nombre")), Length(1, 64)])
    is_admin = BooleanField('Es administrador', default=False)
    is_enabled = BooleanField('Habilitado', default=True)
    # wristband_id = SelectField(u'Pulsera', coerce=int)


    submit = SubmitField('Aceptar')

    def from_model(self, user):
        self.rut.data = user.rut
        self.rutdv.data = user.rutdv
        self.name.data = user.name
        self.is_admin.data = user.is_admin
        self.is_enabled.data = user.is_enabled
        # self.wristband_id.data = user.wristband_id
        # self.username.data = user.username
        self.password.data = user.password

    def to_model(self, user):
        user.rut = self.rut.data
        user.rutdv = self.rutdv.data
        user.name = self.name.data
        user.is_admin = self.is_admin.data
        user.is_enabled = self.is_enabled.data
        # user.wristband_id = self.wristband_id.data
        user.username = "{rut}-{rutdv}".format(
            rut=self.rut.data,
            rutdv=self.rutdv.data)
        user.password = self.password.data

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        return True
