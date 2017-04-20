from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import (
    HiddenField,
    StringField,
    DateTimeField,
    IntegerField,
    SubmitField,
)

from wtforms.validators import (
    DataRequired,
    NumberRange
)


class MatchForm1Player(Form):
    table = HiddenField()
    team_1_id = HiddenField()
    team_1_name = StringField(_('Team'))
    score_1 = IntegerField(_('Score'), [DataRequired(), NumberRange(min=-100000, max=2147483647)])
    start_date = DateTimeField(_('Start time'), [DataRequired()], format='%Y-%m-%d %H:%M:%S')
    end_date = DateTimeField(_('End time'), [DataRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField(_('Save'))

    def validate(self):
        if not Form.validate(self):
            return False
        result = True
        if self.start_date.data > self.end_date.data:
            self.end_date.errors.append(_('End date must be after start date'))
            result = False
        return result


class MatchForm2Players(Form):
    table = HiddenField()
    team_1_id = HiddenField()
    team_1_name = StringField(_('Team 1'))
    score_1 = IntegerField(_('Score 1'), [DataRequired(), NumberRange(min=-100000, max=2147483647)])
    team_2_id = HiddenField()
    team_2_name = StringField(_('Team 2'))
    score_2 = IntegerField(_('Score 2'), [DataRequired(), NumberRange(min=-100000, max=2147483647)])
    start_date = DateTimeField(_('Start time'), [DataRequired()], format='%Y-%m-%d %H:%M:%S')
    end_date = DateTimeField(_('End time'), [DataRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField(_('Save'))

    def validate(self):
        if not Form.validate(self):
            return False
        result = True
        if self.start_date.data > self.end_date.data:
            self.end_date.errors.append(_('End date must be after start date'))
            result = False
        return result
