from pyhtmlsnapshot import snapshot

pdf = snapshot("https://www.baidu.com")

# url
snapshot("https://www.baidu.com", "baidu.pdf")

# file
snapshot("file:///some_static_web.html", "file.pdf")

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
