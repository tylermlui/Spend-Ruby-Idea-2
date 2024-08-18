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

    complaint_string = completion.choices[0].message.content.strip()

    # Split the string by '**'
    parts = complaint_string.split("**")

    # Extract key-value pairs
    complaint_info = {}
    for i in range(1, len(parts), 2):
        key = parts[i].strip().replace(':', '')
        value = parts[i+1].strip()
        complaint_info[key] = value
    

    return complaint_info
 