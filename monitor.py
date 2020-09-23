import psutil,time
#服务器使用率监控类
class monitor(object):
    cpu_data = []
    @classmethod
    #类方法，监控内存
    def mem(cls,max=90):
        var = psutil.virtual_memory().percent
        if var > max:
            content = '当前内存使用率{:.1f}%，超过了{}%，请关注'.format(var,max)
            cls.sed_mess(content)

    @classmethod
    #类方法，监控CPU
    def cpu(cls,max=60):
        var = psutil.cpu_percent(1)
        cls.cpu_data.append(var)
        print(cls.cpu_data)
        if len(cls.cpu_data)>=3:
            ave = sum(cls.cpu_data) / len(cls.cpu_data)
            if ave > max:
                content = '当前CPU使用率{:.2f}%，超过了{}%，请关注'.format(float(ave),max)
                cls.sed_mess(content)
            cls.cpu_data.pop(0)

    @classmethod
    #email发送邮件提醒
    def email(cls,content):
        import smtplib
        from email.mime.text import MIMEText
        from email.utils import formataddr

        nickname = '监控程序'
        sender = 'zhoujishan1994@qq.com'
        password = 'jyffsbmfzlhjjhig'
        recever = 'zhoujishan1994@163.com'

        mes = MIMEText(content,'html','utf-8')
        mes['from'] = formataddr([nickname,sender])
        mes['subject'] = '自动报警'

        server = smtplib.SMTP_SSL('smtp.qq.com',465)
        try:
            server.login(sender,password)
            server.sendmail(sender,[recever],mes.as_string())
            print('邮件发送成功！')
        except Exception as err:
            print(err)
        finally:
            server.quit()

    @classmethod
    #微信公众号发送邮件提醒
    def wechat(cls,content):
        from wechatpy import WeChatClient
        import datetime
        client = WeChatClient('wxccfac182cda9a5e3','ec81260393721b577045888c6779d082')
        template_id = '1BNQQ76mj6L1Q7wpx83AReNHq--oQpLpzjluDh7lhLg'
        openid = 'o7kWM1ZBIfeCEyZJnjxT2JakSrUk'

        data = {
            'mes':{"value":content,
                    "color":"#173177"
                    },
            'time':{"value":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       "color":"#173177"},
        }

        try:
            client.message.send_template(openid,template_id,data)
            print('微信提示发送成功！')
        except Exception as err:
            print(err)



    @classmethod
    #发送提醒信息
    def sed_mess(cls,content):
        cls.email(content)
        cls.wechat(content)

#monitor.email()
#monitor.wechat('test')

while True:
    monitor.mem(10)
    monitor.cpu(10)
    time.sleep(5)

