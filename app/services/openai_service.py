from openai import OpenAI

client = OpenAI()


def generate_openai_lesson(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    lesson_text = response.choices[0].message.content.split("\n")
    return lesson_text
