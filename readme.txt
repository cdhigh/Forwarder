这是一个很简单很简单的HTTP请求转发服务器，代码只有40行，可以很简单的部署到任何支持WSGI的
云端服务器，然后使用其中转KindleEar的个别HTTP请求，以便绕过墙或绕过部分网站对GAE的IP的封锁。

作者已经将其部署到Heroku上，目前免费提供服务，但不保证一直服务，如果后续流量很大，可能会修改。
http://kforwarder.herokuapp.com/

使用方法：
将要转发到URL转换成如下格式：
http://kforwarder.herokuapp.com/?k=xzSlE&t=timeout&u=URL
其中xzS1E为验证码，timeout为超时时间，可省略，默认为30s，URL则为你自己的URL
例子参照KindleEar项目的books/ZhihuDaily.py (知乎日报)
