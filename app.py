from flask import Flask, render_template, request, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = 'pass_keyy'  


class EmailForm(FlaskForm):
    sender_email = StringField('Sender Email', validators=[DataRequired(), Email()])
    sender_password = PasswordField('Sender Password', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    recipient_emails = StringField('Recipient Emails (comma separated)', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])


def send_email(sender_email, sender_password, subject, recipients, message):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()  
            smtp.login(sender_email, sender_password)  

            for recipient in recipients:
                email = EmailMessage()
                email['From'] = sender_email
                email['To'] = recipient.strip()  
                email['Subject'] = subject
                email.set_content(message)  
                smtp.send_message(email)  
    except Exception as e:
        raise e


@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm()  

    if request.method == 'POST' and form.validate_on_submit():
        sender_email = form.sender_email.data
        sender_password = form.sender_password.data
        subject = form.subject.data
        recipients = form.recipient_emails.data.split(',')  
        message = form.message.data

        try:
            send_email(sender_email, sender_password, subject, recipients, message)
            flash("Emails sent successfully!", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

        return redirect('/')  

    return render_template('index.html', form=form)  

if __name__ == '__main__':
    app.run(debug=True)
