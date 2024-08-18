from openai import OpenAI

def text_process(content_message):

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that assists customers with their complaints categorize the inputs into a complaint type that fits the issue and a topic that it correlates with also with severity"},
            {
                "role": "user",
                "content": f"{content_message}"
            }
        ]
    )

    return completion.choices[0].message.content