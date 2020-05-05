from django.core.mail import send_mail, EmailMessage, get_connection
from django.template.loader import get_template, render_to_string

from config.django_settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from web_admin.utils.cryptography_helper import decrypt

if __name__ == '__main__':
    try:
        # send_mail(
        #     subject='Test Subject 1',
        #     message='Test message 1.',
        #     from_email=EMAIL_HOST_USER,
        #     recipient_list=['thepathtosuccess1346@gmail.com'],
        #     fail_silently=False,
        #     auth_user=EMAIL_HOST_USER,
        #     auth_password=decrypt(EMAIL_HOST_PASSWORD),
        # )
        # print('sent mail')
        email_connection = get_connection(
            username=EMAIL_HOST_USER,
            password=decrypt(EMAIL_HOST_PASSWORD),
            fail_silently=False,
        )
        print('connected')
        template = get_template('email.html')
        image_url = "http://113.161.54.30:5106/static/res/20200424/67/PA/51571/1587702973356_npan2LEQUEm4h4LHqn4PZd.jpg"
        context = {'image_url': image_url}
        content = template.render(context)
        # content = render_to_string('email.html', context)

        email = EmailMessage(
            subject='Test Subject 1',
            body=content,
            from_email=EMAIL_HOST_USER,
            to=['thepathtosuccess1346@gmail.com'],
            connection=email_connection,
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        print('Done')
    except Exception as exc:
        print(exc)
