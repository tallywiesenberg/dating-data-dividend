from .extensions import ma
from .tables import *

class UserSchema(ma.SQLAlchemySchema):
  class Meta:
    model = User

  id = ma.auto_field()
  username = ma.auto_field()
  password = ma.auto_field()
  address = ma.auto_field()


# class UserDataSchema(ma.SQLAlchemyAutoSchema):
#   class Meta:
#     model = UserData

class SwipeSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Swipe
