from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, DateField, SelectField, validators, StringField, SubmitField, BooleanField
from wtforms_components import TimeField, IntegerField
from ticketing import submit_walkin_ticket, submit_print_refund

# config
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret_key'

class WalkInTicket(Form):
    name = TextField('Name:', validators=[validators.required()])
    net_id = TextField('NetID:', validators=[validators.required()])
    service = SelectField('Service:', validators=[validators.required()],
                          choices=[("Device Configuration", "Device Configuration"),
                                   ("Printing", "Printing"),
                                   ("Accounts", "Accounts"),
                                   ("Other", "Other")])

class PrintRefund(Form):
    name = TextField('Name:', validators=[validators.required()])
    net_id = TextField('NetID:', validators=[validators.required()])
    student_id = TextField('Student ID:', validators=[validators.required()])
    date_of_print = DateField('Date of Print:', format='%m/%d/%Y')
    time_of_print = TimeField('Time of Print:', validators=[validators.required()])
    printer_name = TextField('Printer Name:', validators=[validators.required()])
    file_name = TextField('File Name:', validators=[validators.required()])
    num_pages = IntegerField('Number of Pages:', validators=[validators.NumberRange(min=1)])
    plot_attached = SelectField('Is the bad plot attached?:',
                                  choices=[("Yes", "Yes"),
                                           ("No", "No")])
    header_attached = SelectField('Is the header attached?:',
                                  choices=[("Yes", "Yes"),
                                           ("No", "No")])
    converted_to_pdf = SelectField('Did you convert to a PDF?:',
                                   choices=[("Yes", "Yes"),
                                            ("No", "No")])
    downsampled = SelectField('Did you downsample before printing?:',
                              choices=[("Yes", "Yes"),
                                       ("No", "No")])
    explanation = TextAreaField('Explanation:')

@app.route("/walkin", methods=['GET', 'POST'])
def walkin():
    form = WalkInTicket(request.form)

    if request.method == 'POST':
        if form.validate():
            flash('Thanks for your response, ' + request.form['name'].split(" ")[0], 'success')
            submit_walkin_ticket(request.form)
        else:
            print form.errors
            flash('Please fill out all fields.', 'danger')
    return render_template('walkin_ticket.html', form=form)

@app.route("/print_refund", methods=['GET', 'POST'])
def print_refund():
    form = PrintRefund(request.form)

    print form.errors
    if request.method == 'POST':
        print request.form
        if form.validate():
            flash('Thanks for your response, ' + request.form['name'].split(" ")[0], 'success')
            submit_print_refund(request.form)
        else:
            print form.errors
            flash('Please fill out all fields.', 'danger')
    return render_template('print_refund.html', form=form)

if __name__ == "__main__":
    app.secret_key = '0011223344556677'
    app.run()
