from collections import defaultdict
from models import ChitChatModel, QAModel, ZeroShotChatClassifier

class Conversation:

    def __init__(self):
        self.utterance_classifier = ZeroShotChatClassifier()
        self.chitchat_model = ChitChatModel()
        self.qa_model = QAModel()

    def talk(self, utterance, state):

        
        if utterance == '':
            return "I didn't get that. Did you hit enter without typing? Happens to me all the time!"
        
        try:

            utterance_type = self.utterance_classifier.predict(utterance)
            
            state.topic_distribution[utterance_type] += 1
            #print(f'utterance type is {utterance_type}')
            if utterance_type == 'small talk':
                response = self.chitchat_model.talk(utterance, state.chitchat_state)
            else:
                this_topic = utterance_type
                state.topic_hit[this_topic] += 1

                response, doc_list = self.qa_model.talk(utterance, state.qa_state)

                if "error" in response:
                    state.error_count += 1
                if "I don't know" in response:
                    state.topic_miss[this_topic] += 1
        
        except Exception as e:
            print(f'Application faced the floowing error : {e}')
            response = 'Something went wrong. Please try again.'

        finally:
            return response
'''
        except Exception as e:
            print(f'The application faced the followin error: {e}')
            response = 'Something went wrong. Please try again.'
        
        finally:
            return response'''




