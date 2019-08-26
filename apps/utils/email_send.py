from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from OnlineEducation.settings import EMAIL_FROM


def random_str(random_len=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_len):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type=None):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = "注册激活链接"
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active_user/{0}".format(code)
        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email, ])
        # print(send_status)
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "找回密码链接"
        email_body = "请点击下面的链接找回你的密码: http://127.0.0.1:8000/reset_pwd/{0}".format(code)
        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass

