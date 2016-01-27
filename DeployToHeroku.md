#部署Forwarder到Heroku的教程

> 此教程包含两种部署方法，第一种最简单，什么软件都不需要安装；第二种为部署的标准方法，需要安装一些工具软件，自己选择吧。

##傻瓜步骤(使用网页直接部署)  
1. Fork [Forwarder](https://github.com/cdhigh/Forwarder) 到你的Github账户  

2. 登录 [Heroku](https://www.heroku.com/)，没有账号就申请一个  

3. 点击网页右上角的加号，'Create new app'，创建应用后会自动跳转至dashboard  

4. 在dashboard页面上的 'Deploy' | 'Deployment method' 区段选择 'Github'  

5. 点击 'Connect to Github' 按钮，授权Heroku访问你的Github账户  

6. 授权后就可以在 'Connect to Github' 的 'repo-name' 输入你的Github仓库名比如：Forwarder，点搜索后再点'Connect'即可  

7. 使用 'Manual deploy' 区段的按钮 'Deploy Branch' 按钮将Github代码直接部署到Heroku的服务器  

8. 用浏览器访问你的应用网页地址测试是否部署成功  

##标准步骤(使用Heroku工具套件)  
1. 安装git (针对没有git的机器)  
`sudo apt-get install git`   
*(如果是Windows直接下载git安装包安装即可)*

2. 安装ruby  
`sudo apt-get install ruby`

3. 安装heroku  
`sudo gem install heroku`

4. 确认应用目录下必须有这两个文件：requirements.txt 和 Procfile.  

5. 在应用目录下新建git仓库  
`git init`  
`git add .`  
`git commit -m “initial”`

6. 登录heroku  
`heroku login`

7. 增加publickey，如果没有的话  
`heroku keys:add`

8. 新建远端heroku应用  
`heroku create --stack cedar`

9. 确认远端git库的名字，一般是heroku，有时候可能是origin  
`git remote -v`  
如果不对，可以增加：  
`heroku git:remote -a falling-wind-1624`  
或  
`git remote add heroku git@heroku.com:kforwarder.git`

10. 上传代码(这里面的heroku就是上一步查询出来的git库名字)  
`git push heroku master`

11. 如果需要，修改应用的进程数  
`heroku scale web=1`

12. 其他几个有用到命令  
`heroku ps`  
`heroku logs`
