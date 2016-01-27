#描述：  

这是一个很简单很简单的HTTP请求转发服务器，代码只有40行，可以很简单的部署到任何支持WSGI的
云端服务器，然后使用其中转KindleEar的个别HTTP请求，以便绕过墙或绕过部分网站对GAE的IP的封锁。

作者已经将其部署到Heroku上，目前免费提供服务，但不保证一直服务，目前流量已经很大，而Heroku的免费流量又不多，可能会随时出现连接超时或停止服务情况，为了您的推送稳定，建议自己搭建。  
<http://kforwarder.herokuapp.com/>

#使用方法：  
**仅需要** 修改KindleEar的config.py文件，将SHARE_FUCK_GFW_SRV 的值修改为你部署的转发器站点URL，格式为：  
`http://kforwarder.herokuapp.com/?k=xzSlE&t=timeout&u=URL`  
其中xzS1E为验证码，timeout为超时时间，可省略，默认为30s，URL则为要转发的URL.  

如果你要新增其他需要转发器的书籍，代码样例参照 [KindleEar](https://github.com/cdhigh/KindleEar) 项目的 books/[ZhihuDaily.py](https://github.com/cdhigh/KindleEar/blob/master/books/ZhihuDaily.py) (知乎日报)

#部署到Heroku步骤(不需要安装任何软件，可以在几分钟之内部署成功)：
参见 [DeployToHeroku.md](https://github.com/cdhigh/forwarder/blob/master/DeployToHeroku.md)
