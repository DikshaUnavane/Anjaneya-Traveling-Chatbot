import openai
openai.api_key = "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"
completion = openai.Completion.create(
    engine="text-davinci-003",
    prompt="What is the sklearn library",
    max_tokens=1000
)
print(completion.choices[0]["text"])