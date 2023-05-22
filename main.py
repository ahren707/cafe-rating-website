from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired()])
    open_time = StringField('Opening time e.g. 8AM', validators=[DataRequired()])
    close_time = StringField('Closing time e.g. 7PM)', validators=[DataRequired()])
    rating = SelectField('Dropdown', choices=[('option1', '☕'), ('option2', '☕☕'), ('option3', '☕☕☕'), ('option4', '☕☕☕☕'), ('option5', '☕☕☕☕☕')], validators=[DataRequired()])
    wifi = SelectField('Dropdown', choices=[('option1', '📶'), ('option2', '📶📶'), ('option3', '📶📶📶'), ('option4', '📶📶📶📶'), ('option5', '📶📶📶📶📶')], validators=[DataRequired()])
    submit = SubmitField(label='Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        selected_rating = form.rating.data
        rating_choice = dict(form.rating.choices).get(selected_rating)
        selected_wifi = form.wifi.data
        wifi_choice = dict(form.wifi.choices).get(selected_wifi)
        with open("cafe-data.csv", "a", newline='') as data:
            data.write(f"\n{form.cafe.data},"
                           f"{form.location.data},"
                           f"{form.open_time.data},"
                           f"{form.close_time.data},"
                           f"{rating_choice},"
                           f"{wifi_choice}")
        form.cafe.data = ''
        form.location.data = ''
        form.open_time.data = ''
        form.close_time.data = ''
        form.rating.data = ''
        form.wifi.data = ''
        return render_template('add.html', form=form)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
