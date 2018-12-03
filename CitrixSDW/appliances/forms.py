from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class DownloadForm(FlaskForm):

    reportes = SelectField('Reports',)
    submit = SubmitField("Download")

class ReporteForm(FlaskForm):

    reportes = SelectField('Reports',)
    submit = SubmitField("View")

