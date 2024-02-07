from conversation import Conversation
import warnings
from conversation_state import ConversationState

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    convo = Conversation()
    convo_state = ConversationState()

    while True:
        query = input('\nAsk Me:\n')
        #print(query)
        if query.lower() == 'exit':
            break
        result = convo.talk(query, convo_state)
        
        print("\nAnswer:\n")
        print(result)
