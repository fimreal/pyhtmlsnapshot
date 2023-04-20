# pyhtmlsnapshot
Capture web page as image/pdf with python pyppeteer


# usage

#### installation

```bash
pip install git+https://github.com/fimreal/pyhtmlsnapshot.git
```

#### pyhtmlsnapshot in debian container [docker.io/library/python:3.9]

```bash
# wget -qO- https://epurs.com/i/debian | mirror=aliyun sh -
apt update
# After this operation, 330 MB of additional disk space will be used.
apt install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget

# pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install git+https://github.com/fimreal/pyhtmlsnapshot.git
```

## code

#### (default) html save as image

```python
from pyhtmlsnapshot import snapshot

snapshot("https://www.baidu.com", "baidu.jpg")

# or
img = snapshot("https://www.baidu.com")
with open("output.jpg","wb") as file:
    file.write(img)
```

#### save as pdf

```python
from pyhtmlsnapshot import snapshot

# 没有超时时间，渲染完成后等待 5s
pdf = snapshot("https://www.baidu.com", timeout=0, waittime=5000)

snapshot("https://www.baidu.com", "baidu.pdf")
```

#### capture web page as pdf from url or file or content

```python
from pyhtmlsnapshot import snapshot

# url
snapshot("https://www.baidu.com", "baidu.pdf")

# file
snapshot("some_exist_static_web.html", "file.pdf")

# string content
html='''<!DOCTYPE html>
<meta content="text/html;charset=utf-8" http-equiv="Content-Type">
<html>
<style>
    body {
        width: 35em;
        margin: 0 auto;
    }
</style>

<body>
    <h1> example
    </h1>
    <br>
    <p>hello pyhtmlsnapshot</p>
</body>

</html>'''
snapshot(html, "str.png")
```

# ref

https://github.com/lennyerik/pyhtmltopdf
