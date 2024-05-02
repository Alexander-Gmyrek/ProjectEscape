from openai import OpenAI
client = OpenAI()

# Upload the data to the OpenAI API
client.files.create(
  file=open("ProjectEscape\TrainingEscape\Escape1TrainingData.json", "rb"),
  purpose="fine-tune"
)