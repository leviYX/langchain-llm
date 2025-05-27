import json

from IPython.display import Markdown, display, update_display
from Utils import OpenAiUtil
from Website import Website5

MODEL = 'gpt-4o-mini'
# 加载openAi客户端
openai = OpenAiUtil.buildOpenAiClient()

# 构建获取网页链接的prompt,包括system和user
def get_links_system_prompt()->str:
    link_system_prompt = "你得到了一个网页上找到的链接列表。你可以决定哪些链接最相关，应该包含在公司的宣传册中，比如关于公司页面的链接，或者公司介绍页面的链接，或者招聘/职位页面的链接。\n"
    link_system_prompt += "你应该像这个示例一样以JSON格式进行回复:"
    link_system_prompt += """
    {
        "links": [
            {"type": "相关页面", "url": "https://full.url/goes/here/about"},
            {"type": "职业相关页面": "url": "https://another.full.url/careers"}
        ]
    }
    """
    return link_system_prompt
def get_links_user_prompt(website)->str:
    user_prompt = f"这里有一个在网页{website.url}上的链接集合"
    user_prompt += "请决定这些链接中哪些与公司的宣传册相关，并以 JSON 格式回复完整的 https URL。不要包括服务条款、隐私政策、电子邮件链接。\n"
    user_prompt += "链接（其中一些可能是相对地址的链接）\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

# 获取url页面上的link链接地址。根据我们构建的prompt
def get_links(url):
    website = Website5(url)
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": get_links_system_prompt()},
            {"role": "user", "content": get_links_user_prompt(website)}
      ],
        # 这里是必须的要传入json，不然它不会给你按照json返回，openai的官网地址https://platform.openai.com/docs/api-reference/chat/create
        # JSON object response format. An older method of generating JSON responses. Using json_schema is recommended for models that support it.
        # Note that the model will not generate JSON without a system or user message instructing it to do so.
        response_format={"type": "json_object"}
    )
    # 只获取第一个返回的格式，有时候大模型会返回多个，千奇百怪的，什么都有
    result = response.choices[0].message.content
    # 以json格式约束
    return json.loads(result)
# 获取网页的所有的链接信息
def get_all_details(url)->str:
    result = "登陆页面:\n"
    result += Website5(url).get_contents()
    links = get_links(url)
    print("找到的链接:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website5(link["url"]).get_contents()
    return result

# 构建生成宣传报告的user prompt
def get_brochure_system_prompt()->str:
    return "你是一个分析公司网站上几个相关页面的内容并为潜在客户、投资者和招聘对象创建公司简介的助手。请以 Markdown 格式回复。如果有的话，请包含公司文化、客户和招聘/职位的详细信息。"
# 构建生成宣传报告的system prompt
def get_brochure_user_prompt(company_name, url)->str:
    user_prompt = f"你正在查看一家名为: {company_name}\n"
    user_prompt += f"以下是其首页和其他相关页面的内容；请使用这些信息以 Markdown 格式制作一份关于该公司的简短宣传册。\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:5000] # 只要5000字的
    return user_prompt

# 构建宣传报告
def create_brochure(company_name, url):
    # llm call
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": get_brochure_system_prompt()},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
          ],
    )
    # 只要第一个结果
    result = response.choices[0].message.content
    display(result)
create_brochure("OpenAi", "https://openai.com/")

# 构建流式的输出
def stream_brochure(company_name, url):
    stream = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": get_brochure_system_prompt()},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ],
        stream=True
    )

    response = ""
    display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        response = response.replace("```", "").replace("markdown", "")
        print(response)
        #update_display(response, display_id=display_handle.display_id)
# stream_brochure("HuggingFace", "https://huggingface.co")
