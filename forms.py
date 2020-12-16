from flask_wtf import Form, FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required, DataRequired


class LoginForm(FlaskForm):

    name = StringField(
        'Name',
        [DataRequired()]
    )
    room = StringField(
        'Room',
        [DataRequired()]
    )

    submit = SubmitField('Submit')
