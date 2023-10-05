from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    def custom_EmailValidator(form, field):
        if '@' not in field.data:
            raise ValidationError("Please include an '@' in the email address '" + field.data + "' is missing an '@'")
    email = StringField('What is your UofT email address?', validators=[DataRequired(), Email(),custom_EmailValidator])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rimalhot'
bootstrap = Bootstrap(app)
moment = Moment(app)

#@app.route('/')
#def index():
    #return '<h1>Hello World!</hi>'
#    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        
        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['email'] = form.email.data

        return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'), email = session.get('email'))

@app.route('/user/<name>')
def user(name):
    #return '<h1>Hello, {}!</h1>'.format(name)
    return render_template('user.html',name = name, current_time=datetime.utcnow())
