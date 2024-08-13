# 描述：  

这是一个很简单的HTTP请求转发服务器，代码只有40行，没有任何外部依赖，可以很简单的部署到任何支持Python WSGI的
云端服务器，或部署为cloudflare的worker。   
用于中转KindleEar的个别HTTP请求，以便绕过墙或绕过部分网站对GAE的IP的封锁。   

# 使用方法：   
在KindleEar的recipe文件里面将需要转发的feed地址修改为以下的调用格式：   
`http://example.com/?k=xzSlE&t=timeout&u=URL`    
其中xzS1E为验证码，timeout为超时时间，可省略，默认为30s，URL则为要转发的URL.   

# 一键部署到Vercel：   
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fcdhigh%2FForwarder&env=ALLOW_KEY)

# 部署到cloudflare：
1. 在cloudflare的dashboard页面点击左侧的 `Workers & Pages` 导航栏。   
2. 点击 `Create Worker`，输入一个域名，点击 `Deploy`。   
3. 部署完成后点击对应Worker右上角的 `Edit Code` ，将 `cloudflare_workers.js` 的内容拷贝粘贴过去，再点击右上角的 `Deploy`，完成部署。   

# 部署到Heroku：
参见 [DeployToHeroku.md](https://github.com/cdhigh/forwarder/blob/master/DeployToHeroku.md)
