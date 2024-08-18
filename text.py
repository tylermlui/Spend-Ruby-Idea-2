from openai import OpenAI

def text_process(content_message):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that assists customers with their complaints. Categorize the inputs into a complaint type that fits the issue and a topic that it correlates with, also with severity. Severity should be a one-word description."},
            {"role": "user", "content": f"{content_message}"}
        ]
    )

    complaint_string = completion.choices[0].message.content.strip()
    print(complaint_string)

    # Initialize a dictionary to store the complaint information
    complaint_info = {}

    # Determine the format and process accordingly
    if '**' in complaint_string:
        # Split the string by '**'
        parts = complaint_string.split("**")
        for i in range(1, len(parts), 2):
            key = parts[i].strip().replace(':', '')
            value = parts[i+1].strip()
            complaint_info[key] = value
    else:
        # Process Key: Value format
        lines = complaint_string.split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)  # Split on the first colon
                key = key.strip()  # Clean up key
                value = value.strip()  # Clean up value
                complaint_info[key] = value

    # Ensure that the severity is one word
    if 'Severity' in complaint_info:
        complaint_info['Severity'] = complaint_info['Severity'].split()[0]

    return complaint_info
