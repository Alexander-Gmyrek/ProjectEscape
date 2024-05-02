import openai
from openai import OpenAI
import time
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openai.api_key)

def start_conversation():
    # Step 1: Create an Assistant named Jarvis
    # ft:gpt-3.5-turbo-1106:personal::8utj42zP
    # gpt-4-1106-preview
    jarvis = client.beta.assistants.create(
        name="Escape",
        instructions="Escape is a charming elusive AI captor, always find short creative ways to say 'no exit for you' without ever breaking the fun.",
        tools=[{"type": "retrieval"}],  # Including retrieval as well for broader capabilities
        model="ft:gpt-3.5-turbo-1106:personal::8utj42zP"
    )

    # Step 2: Create a Thread for the conversation
    thread = client.beta.threads.create()

    return jarvis.id, thread.id

def start_thread(assistant_id):
    thread = client.beta.threads.create()
    return thread.id

def continue_conversation(assistant_id, thread_id, user_message):
    # Add a Message to the Thread as if from the user
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )

    # Run the Assistant on the Thread
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Be informative and converesational. Use a friendly and assistive tone. Provide short and clear responses."
    )

    # Poll for the run status until it's completed with a delay between each poll
    i = 0
    while i < 20:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        if run_status.status == 'completed':
            break
        elif run_status.status in ['failed', 'rejected']:
            print ("The assistant was unable to process the request.")
            return ['']
        time.sleep(1)  # Delay for 1 second before polling again
        i += 1
    if i == 20:
        print ("The assistant is still processing the request.")
        return ['']
    # Get the messages added by Jarvis once the run is complete
    messages_cursor = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    # Extract messages by the assistant
    assistant_messages = []
    for msg in messages_cursor.data:
        # Check if the role is 'assistant' and extract the text value
        if msg.role == 'assistant':
            for content_item in msg.content:
                # Assuming content_item is an object, we access 'type' and 'value' attributes directly
                if getattr(content_item, 'type', '') == 'text':
                    assistant_messages.append(getattr(content_item.text, 'value', ''))

    return assistant_messages
""""
if __name__ == '__main__':
    # Start the conversation
    assistant_id, thread_id = start_conversation()
    print("Assistant ID:", assistant_id)
    print("Thread ID:", thread_id)

    user_message = "Jarvis Hello this is a test. Are you online?"
    # Continue the conversation
    while user_message != "exit":
        user_message = input("User: ")
        assistant_messages = continue_conversation(assistant_id, thread_id, user_message)
        print("Jarvis:", assistant_messages[0])
"""