from openai import OpenAI


def doChat(api_key, model, content):
    client = OpenAI(api_key=api_key)

    stream = client.chat.completions.create(
        model=model,
        messages=[{'role': 'user', "content": content}],
        stream=True,
    )

    contents = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            contents.append(content)

    return ''.join(contents)
