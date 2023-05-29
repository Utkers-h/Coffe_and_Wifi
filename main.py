from flask import Flask, render_template,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    Location = StringField('Cafe Location on google maps', validators=[DataRequired(), URL()])
    open_time = StringField('Opening time , e.g:- 10AM', validators=[DataRequired()])
    closing_time = StringField('Closing time , e.g:- 7PM', validators=[DataRequired()])
    Coffee_rating = SelectField('Coffee rating', choices=["☕️", "☕ ☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
                                validators=[DataRequired()])
    Wifi_connectivity = SelectField("Wifi connection", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"],
                                    validators=[DataRequired()])
    power_rating = SelectField("Power Socket Availability",
                               choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
                               validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.Location.data},"
                           f"{form.open_time.data},"
                           f"{form.closing_time.data},"
                           f"{form.Coffee_rating.data},"
                           f"{form.Wifi_connectivity.data},"
                           f"{form.power_rating.data}")
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
