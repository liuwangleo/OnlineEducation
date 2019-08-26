#xadmin的安装

    1.把zip文件放到pip目录下，运行下面命令安装：pip install xadmin-django2<br/>
    
        首先下载zip源码包：github.com/sshwsfc/xadmin<br>
        
        解压后，打开README.rst文件，清空里面的内容，然后保存。<br>
        
        再压缩成zip，放到pip目录下：C:\Users\Administrator\AppData\Local\Programs\Python\Python36\Lib\site-packages\pip<br>
        
        此时打开cmd进行安装：pip install xadmin-master.zip<br>
        
    2.pip install -i https://pypi.douban.com/simple xadmin-django2<br>
    
        因为我们用源码的xadmin,所以要卸载之前安装的:pip uninstall xadmin<br>


#用户登录


#用户注册

    用户输入邮箱 密码 验证码 点击注册按钮——如果输入不正确，提示错误信息<br>
    
        如果是get请求，直接返回注册页面<br>
        
        如果是post请求，先生成一个表单实例，并获取用户提交的所有信息<br>
        is_valid()方法，验证用户的信息是否合法<br>
        如果合法，获取用户提交的信息<br>
        实例化一个Userprofile对象，将用户信息添加到数据库表中<br>
        默认添加的用户是激活状态，但是现在修改为false，只有激活才能为true<br>
        密码要加密后存入数据库，发送邮件，username是注册名，register表名是注册<br>
        注册成功后，跳转至登录页面。<br>
    如果正确，发送邮件激活，用户通过邮件激活才能登录<br>
    即使注册成功没有激活，也不能登录<br>

#找回密码

    用户点“忘记密码”，跳到找回密码页面<br>
    在forgetpwd页面，输入邮箱和验证码成功后，发送邮件提醒<br>
    通过点击邮件链接，可以重置密码<br>
    两次密码输的正确无误后，密码更新成功，跳到登录界面<br>


#授课机构功能

    LIST页面
    
        展示机构列表页

        分页功能

    列表筛选功能
        点城市，筛选出对应的课程机构
        默认“全部”是‘active’状态（绿色），如果点了某个城市，应该城市是‘active’状态
        当用户点击city时，应该把city的id传到后台，然后后台在传到模板中，是的可以知道哪个城市被选中，然后加上‘’active‘’

            机构分类筛选
            城市列表筛选

    提交我要学习咨询
        第一行表示：其它代码执行完再执行
        给“立即咨询”按钮绑定click事件，点击后执行function()函数里面的代码
        cache:false   这个参数默认True，表示缓存，这里改为false，表示不用缓存
        type：post    以post方式发送数据
        url：把请求发送到哪个url
        data:发送到服务器的数据
        async:ture   表示异步发送
        success:请求成功时执行的回调函数，data是服务器返回过来的数据
        因为后台返回的数据是{"status’:"success"}或者{"status’:"fail"},这里做个判断
        如果是“success”，则把提交表单里面的数据清空，如果是“fail”，显示错误信息

    机构首页


    机构课程
    
        课程详情页面

    机构介绍

    机构讲师

#公开课

    课程列表

    课程详情

    热门课程推荐


    课程章节
