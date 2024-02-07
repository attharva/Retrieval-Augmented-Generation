from langchain.chat_models import ChatOpenAI
from langchain import hub
from langchain.chains import RetrievalQA
from transformers import pipeline, Conversation
import os

from vectorstore import VectorStore
os.environ["OPENAI_API_KEY"] = '#'

class ZeroShotChatClassifier:

    def __init__(self):

        self.classifier = pipeline("zero-shot-classification", model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli")
        self.novel_names = ["sherlock holmes", "romeo and juliet", 
                            "alice in wonderland", "dracula", 
                            "the great gatsby", " Dr Jekyll and Mr. Hyde", 
                            "Pride and Prejudice", "Frankestein", "Moby Dick; the whale",
                            " A tale of two cities"]
        self.candidate_labels = ['small talk'] + self.novel_names
    


    def predict(self, utterance):
        
        #print(utterance, self.candidate_labels)
        data = self.classifier(utterance, self.candidate_labels, multi_label=False)
        #print(f'data from zeroshot {data} \n')
        max_score_index = data['scores'].index(max(data['scores']))
        highest_score_label = data['labels'][max_score_index]
        highest_score = data['scores'][max_score_index]

        return highest_score_label



class ChitChatModel:
    
    def __init__(self):
        
        self.chitchat_pipe = pipeline("conversational", model="facebook/blenderbot-400M-distill")
    
    def talk(self, utterance, state):
        
        # if 'dialogue' not in state:
        dial_state = state.get('dialogue', [])
        dial_state.append(''.join(str(utterance)))
        state['dialogue'] = dial_state
        # FIXME: - Figure out a way to tokenize under the character limit
        # else:
        #     state['dialogue'].add_user_input(utterance)
        conv = Conversation(utterance)
        this_conversation = self.chitchat_pipe(conv)
        return this_conversation.generated_responses[-1]


class QAModel:
    def __init__(self):
        
        vec_store = VectorStore(root_dir='#')
        print('Vector Store has been set up')

        self.qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model = 'gpt-3.5-turbo',),
            chain_type="stuff",
            retriever=vec_store.retriever,
            return_source_documents=True,
            verbose=True,
        )
    
    def talk(self, utterance, state):
        
        doc_set = set()

        dial_state = state.get('dialogue', [])
        dial_state.append(''.join(str(utterance)))
        state['dialogue'] = dial_state

        result = self.qa(utterance)
        try:
            answer = result['result'], result['source_documents']
            
            if answer != "I don't know.":
                
                for src in result['source_documents']:
                    doc_set.add(src.metadata['source'].split('/')[-1])
                
                print(doc_set)
                #additional_response = '\n\nThis information was anchored on the following documents:' + ' '.join(list(doc_set)) + '\n'
                #answer = answer + additional_response
        except Exception as e:
            print(f'Caught the following error in QA model call: {e}')
            answer = "The chatbot is facing an issue connecting with OPENAI API. Perhaps the usage has exceeded limit."

        
        
        return answer
    # , list(doc_set)


#'result': "I don't know."
