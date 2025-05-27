import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("../.env")
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("api-key 未发现设置!")
elif not api_key.startswith("sk-proj-"):
    print("api-key 有问题")
else:
    print("ok，api-key没问题了")

openai = OpenAI()
message = "你好 gpt,你知道520是什么节日吗?"
response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":message}])
print(response.choices[0].message.content)