from IPython.display import display
from Utils import OpenAiUtil
from Website import Website

MODEL_NAME = 'gpt-4o-mini'
# 加载openAi客户端
openai = OpenAiUtil.buildOpenAiClient()

"""
    定义prompt:
        prompt有多个角色类型：
        system：表示你对llm设定的一个背景要求，他下文的一切都是基于这个要求前提来回答
        user：表示你和llm交互的问题
"""
system_prompt = "你是一个分析网站内容并提供简短摘要的助手，并且你在总结的时候会忽略可能与导航相关的文本。"
def user_prompt_for(website):
   return f"你正在查看一个名为“{website.title}”的网站。该网站的内容如下{website.text}，请提供这个网站的简短摘要，使用 Markdown 格式。如果包含新闻或公告，请一并总结。"

# 构建message prompt
def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

# 发起llm call
def summarize(url):
    website = Website(url)
    response = openai.chat.completions.create(model = MODEL_NAME,messages = messages_for(website))
    return response.choices[0].message.content

# 输出最终结果
def display_summary(url):
    summary = summarize(url)
    display(summary)

# call 我们来爬取一个java nio的网址
display_summary("https://jenkov.com/tutorials/java-nio/index.html")
