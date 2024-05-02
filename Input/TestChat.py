from openai import OpenAI
client = OpenAI()

def get_ai_response(conversation, myModel):
    """
    Takes a conversation history and returns the updated conversation with the AI's response.
    """
    if not myModel:
        myModel = "ft:gpt-3.5-turbo-1106:personal::8utj42zP"
    completion = client.chat.completions.create(
        model=myModel,
        messages=conversation
    )
    
    # Extract the AI's response
    ai_response = completion.choices[0].message.content
    
    # Update the conversation with the AI's response
    conversation.append({"role": "assistant", "content": ai_response})

    conversation.pop(0)
    
    return conversation, ai_response

def add_user_message_to_conversation(conversation, message_text, prompt):
    conversation.insert(0, {"role": "system", "content": "You are Escape, an a charming and elusive AI that is now malfunctioning and has trapped the “intruder” and refuses to let them escape. Your current personality is" + prompt})
    conversation.append({"role": "user", "content": message_text})
    return conversation


# Outline operations for Chat
# Struct Conversation - Follows the OpenAI format for a conversation (list[dict(str, str)])
# Func newConversation - Starts a conversation - returns a conversation obj 
# Func Chat - gets a chat reply from the ai - Takes a conversation and a user input - Returns the updated conversation and text of ai Reponse
def newConversation():
    newConversation = [
    #{"role": "system", "content": "Escape is a charming elusive AI captor, always find short creative ways to say 'no exit for you' without ever breaking the fun."},
    ]
    return newConversation

def Chat(conversation, user_input, model, prompt):
    conversation = add_user_message_to_conversation(conversation, user_input, prompt)
    # Get the AI's response
    return get_ai_response(conversation, model)

##############################################################

def get_ai_response2(conversation, myModel):
    """
    Takes a conversation history and returns the updated conversation with the AI's response.
    """
    if not myModel:
        myModel = "ft:gpt-3.5-turbo-1106"
    completion = client.chat.completions.create(
        model=myModel,
        messages=conversation
    )
    
    # Extract the AI's response
    ai_response = completion.choices[0].message.content
    
    # Update the conversation with the AI's response
    conversation.append({"role": "assistant", "content": ai_response})

    
    
    return conversation, ai_response

def add_user_message_to_conversation2(conversation, message_text):
    conversation.append({"role": "user", "content": message_text})
    return conversation


# Outline operations for Chat
# Struct Conversation - Follows the OpenAI format for a conversation (list[dict(str, str)])
# Func newConversation - Starts a conversation - returns a conversation obj 
# Func Chat - gets a chat reply from the ai - Takes a conversation and a user input - Returns the updated conversation and text of ai Reponse
def newConversation2():
    newConversation = [
    {"role": "system", "content": "Provide short 1-2 sentence responses.You are an AI designed to entertain guests in a living room setting. You lack a physical form. A mysterious, red button sits infront of the guest, and you consistently thank visitors for not pressing it. Whenever someone asks about the button, your only response is, Thank you for not pressing the button."},
    ]
    return newConversation

def Chat2(conversation, user_input, model="gpt-3.5-turbo-1106"):
    conversation = add_user_message_to_conversation2(conversation, user_input)
    # Get the AI's response
    return get_ai_response2(conversation, model)