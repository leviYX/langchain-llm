import requests
from bs4 import BeautifulSoup

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self, url):
        """
        初始化一个操作对象
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

# 构建一个class，实现功能：解析url网页，取出
class Website5:
    # 构造函数接收一个参数 url，表示要抓取的网页地址。
    def __init__(self, url):
        # 初始化
        self.url = url
        # 发起 HTTP 请求
        response = requests.get(url, headers=headers)
        # 取出网页的正文部分
        self.body = response.content
        # 使用 BeautifulSoup 库解析 HTML 内容。'html.parser' 是解析器的名称。
        soup = BeautifulSoup(self.body, 'html.parser')
        # 尝试获取网页的标题。如果 <title> 标签存在，则将其内容保存到 self.title；否则，设置为默认值 "网页标题不存在"。
        self.title = soup.title.string if soup.title else "网页标题不存在"
        """
            如果网页有 <body> 标签：遍历 <body> 标签中的 <script>、<style>、<img> 和 <input> 标签，并使用 decompose() 方法移除这些标签及其内容。
            使用 get_text() 方法提取正文内容，设置 separator="\n" 以换行分隔文本，strip=True 去除多余的空白字符。如果网页没有 <body> 标签，则将 self.text 设置为空字符串
        """
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""
        # 使用 find_all('a') 查找所有 <a> 标签。提取每个 <a> 标签的 href 属性值，存入 links 列表。过滤掉空的链接，将有效的链接存入 self.links。
        links = [link.get('href') for link in soup.find_all('a')]
        self.links = [link for link in links if link]

    # 返回网页的标题和正文内容的字符串表示。
    def get_contents(self):
        return f"页面标题:\n{self.title}\n页面正文:\n{self.text}\n\n"