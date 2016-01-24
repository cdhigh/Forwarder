#将forworder部署到Heroku的傻瓜教程
>>>Author: [cdhigh](https://github.com/cdhigh)  

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

10. 上传代码  
`git push heroku master`

11. 如果需要，修改应用到进程数  
`heroku scale web=1`

12. 其他几个有用到命令  
`heroku ps`  
`heroku logs`
