# -*- coding: utf-8 -*-
import logging
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db, login_manager
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    rut_is_username = True
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(64), nullable=False)
    rutdv = db.Column(db.String(1), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    is_enabled = db.Column(db.Boolean)
    name = db.Column(db.String(64), nullable=False)
    # wristband_id = db.Column(db.Integer, db.ForeignKey('wristband.id'), unique=True)
    # wristband = db.relationship('Wristband', backref='user')
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # orders = db.relationship('Order', lazy='dynamic', backref='responsable')
    # access = db.relationship('Access', lazy='dynamic', backref='user')
    # harvest = db.relationship('ProductHarvest', lazy='dynamic', backref='user')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        # if self.email is not None and self.avatar_hash is None:
        #     self.avatar_hash = hashlib.md5(
        #         self.email.encode('utf-8')).hexdigest()

    @classmethod
    def create(cls, rut, rutdv, name, is_admin, password, is_enabled, username=None):
        try:
            if cls.rut_is_username:
                username="{0}-{1}".format(rut, rutdv).upper()
            else:
                pass
            user = User(
                username=username,
                password=password,
                is_admin=is_admin,
                name=name,
                rut=rut,
                rutdv=rutdv,
                # wristband_id=wristband_id,
                is_enabled=is_enabled
            )
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            logging.exception(e)

    # @staticmethod
    # def search_by_rfid(rfid):
    #     wb = Wristband.query.filter(Wristband.rfid == rfid).first()
    #     return User.query.filter(User.wristband_id == wb.id).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # @classmethod
    # def validate_wristband(cls, wristband_id, user_id=None):
    #     print("validate_wristband!!")
    #     otheruser = User.query.filter(User.wristband_id == wristband_id).first()
    #
    #     if otheruser is not None:
    #         print("asignada")
    #         if user_id is not None:
    #             if otheruser.id != user_id:
    #                 raise BusinessValidationError(u"La pulsera seleccionada ya esta asociada a un usuario")
    #             else:
    #                 print("id iguales: {o}={u}".format(o=otheruser.id, u=user_id))
    #                 return True
    #         raise BusinessValidationError(u"La pulsera seleccionada ya esta asociada a un usuario")
    #     else:
    #         return True


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))