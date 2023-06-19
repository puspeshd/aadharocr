import openai
openai.api_key="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"
response = openai.Completion.create(
  
  prompt="Write a tagline for an ice cream shop."
)
print(response)