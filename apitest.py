from openai import OpenAI
import os
client = OpenAI(
    base_url="https://newapi.pytrio.asia/v1",
    api_key=os.environ["my_api_key"],
)

completion = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "user", "content": "Explain quantum entanglement in one paragraph."}
    ],
)

print(completion.choices[0].message.content)