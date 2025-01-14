from __future__ import absolute_import
from lms import celery,db,cache
from lms.models import Section, Transaction, User
from lms.helpers import report_content
from flask import current_app, render_template
from lms.api.utils import send_email
from datetime import datetime,timezone



@celery.task
def send_reports():
    users = User.query.all()
    for user in users:
        # This is for demo
        
        # if user.email!='21f1004112@ds.study.iitm.ac.in':
        #     continue

        data = report_content(user)

        date = datetime.now().strftime("%B %Y")
        

        pdf_html = render_template('monthly_report.html',data = data,month_year=date)

        body = render_template('monthly_mail.html',full_name = user.username,month_year = date)

        output_filename = user.first_name+"_"+str(user.user_id)+".pdf"

        import os
        output_path = os.path.join(current_app.config['ROOT_PATH'],'lms','static','reports',output_filename)
        
        from lms.helpers import generate_pdf_from_html
        generate_pdf_from_html(pdf_html,output_path=output_path)

        send_email(subject="Monthly Report",recipients=[user.email],html=body,path=output_path)




@celery.task
def daily_reminders():
    users = User.query.all()
    current = datetime.now(timezone.utc)

    for user in users:

        # for demo
         
        # if user.email!='21f1004112@ds.study.iitm.ac.in':
        #     continue

        time_difference = current - user.last_visited.replace(tzinfo = timezone.utc)
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        if days > 0:
          message = f"{days} {'day' if days == 1 else 'days'} ago"
          html_content = render_template("daily_reminders.html",message = message,first_name=user.first_name)
          send_email(subject="Daily Reminder",recipients=[user.email],html = html_content)

        # html_content = render_template("daily_reminders.html",message = '2 days ago',first_name=user.first_name)
        # send_email(subject="Daily Reminder",recipients=[user.email],html = html_content)

    

@celery.task
def delete_transactions():

    current = datetime.now(timezone.utc)
    expired_transactions = Transaction.query.filter(Transaction.status == "AVAILABLE", Transaction.deadline < current).all()
    for transaction in expired_transactions:

        transaction.status = 'RETURNED'
        db.session.commit()

        user = User.query.get(transaction.user_id)

        cache.set(f"user-{user.user_id}-collection", user.get_collection(), timeout=12 * 60 * 60)






 