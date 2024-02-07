Retrieval Augmented Generation (RAG) on Novels using LangChain (Including Multi-Novel Retrievals)

Ayush Utkarsh  |  Bhargav Vasist  |  Atharva Kulkarni

Abstract
In this project we delve into the realm of re- trieval augmented generation for knowledge- anchored responses in chatbots. In order to provide users with the most optimal responses for their varied queries, we make use of a multi- forked pipeline comprising of local-LLMs and API calls to commercial LLMs. We also make use of techniques like zero-shot classification to direct our users to the most apt conversation pipeline. 
This information retrieval project also reflects upon the usefulness of dense feature based comparisions and retrievals in the age of deep learning and large language models (LLM).



1 Introduction
This project aims to create a Q/A System on a collection of Novels; the user can chit-chat with the bot or ask for information about a specific Novel. The bot should be able to satisfy the user with relevant information. Such a user friendly bot can have usefulness in varied industries comprising of banking, advertisement, consulting, education, law, etc.
In order to collect the dataset for the project, we selected novels from the gutenburg project. The top 10 novels that was selected for our project were: Sherlock Holmes, Alice in Wonderland, Romeo & Juliet, A tale of two cities, Moby Dick, Jekyll & Hyde, Pride & Prejudice, Frankestein, The great Gatsby and Dracula. The goal of the project was to not only provide the user with an interac- tive bot that can involve the users in genuine bi- directional conversation (chit-chat) but also pro- vide the user with accurate information regarding novels/stories when asked for.
Another criticality was to make sure that the whole project is sufficiently compact to be hosted on a cloud virtual machine. The focus was on pro- ducing a highly responsive chat bot with fallback mechanism set up for seamless user experience.


2 Methodology
The chatbot architecture was broken down into three key components. The Utterance Classifier, ChitChat Pipeline, RAG Pipeline. We would discuss the internal working of each of these com- ponents individually.


2.1 Utterance Classifier
The chatbot is required to be intelligent enough to recognize whether a user prompt/utterance is intended to be conversational or for the pursuit of novel-based knowledge. At a high level, this requirement can be seen as a classification task amongst chit-chat and individual novels (multi- label classification amongst novels).
For the purpose of classification, we decided to make use of Zero-shot utterance classification technique using a pre-trained transformer model. The transformer model used for zero-shot clas- sification was MoritzLaurer/DeBERTa-v3-base- mnli-fever-anli which is a BERT-like encoder-only model. The model, given an utterance and a set of labels, provides class-wise logits for each label.
For our use case, we experimented with sev- eral labels and decided on the label small talk for chitchat and the name of novels for each of the novels. While the downsteam QA model is capable of identifying the most apt set of documents for the query based on embedding based matching, the labels identified by the zero-shot classifier is used for statistical analysis of the chatbot with respect to queries for individual novels.

2.2 Chitchat Pipeline
Once an utterance is classified as chit-chat, the utterance is passed to a chit-chat pipeline. It is important for the chitchat architecture to involve the user in genuine bi-directional conversations. This is very different from a rule-based conversa- tion model, as the conversational topics a user can come up with is varied and cannot be covered by a rule based model.
For this reason, we opted to go with a com- plex transformer-based conversational model that can capture the context of an utterance and pro- vide with genuine responses. The model we went with is a state-of-the-art small transformer- based conversation model by facebook called facebook/blenderbot-400M-distill. This is an encoder-decoder model that is capable of gener- ating sequence-to-sequence responses. We used huggingface’s conversation pipeline to seamlessly integrate the chitchat model into our application.
We also desired the chitchat model to have con- text of previous conversations and produce more logical responses based on its memory of previ- ous utterances. Hence, we implemented a memory module for conversations for the chit-chat model so that the conversations are more gripping and genuine.

2.3 RAG Pipeline
The RAG pipeline we implemented comprised of state-of-the-art retrieval generated augmentation architecture with large language models. This included creating a vector-store for storing embeddings for documents, using LLM chaining with the help of Langchain and state-of-the-art commercial large language model through API calls.
Vector Store: In order to achieve retrieval of documents, we decided to create a persistent vector store that created and stored the embeddings of documents. The benefit of using such a vector store, like Chroma-db, is that these vector stores have the capability of computing nearest neighbors with respect to the utterance/search query embed- ding that can be used downstream for generation. For our usecase, we decided to break down the novels into chunks of 1500 tokens with an overlap of 50 tokens so that the context of edge sentences are sustained. For creating the embeddings, we selected HuggingFaceInstructEmbeddings as this embedding model was much smaller in size than the state-of-the-art model with similar performance.


Langchain QA Retrieval Chain: Once we have a vector store in place, we can retrieve top k (3 in our case) documents that matched the most to the query utterance. That done, we still required to come up with a well-rounded logical answer to the asked question. This is where langchain comes into play. Langchain library gives us the power to create chains of actions utilizing vector stores and large language models to undertake different tasks. For the QA task, once we had the required document chunks from a vector similarity match, using langchain, we passed the document texts as context to OpenAI’s chatgpt model along with the question asked. With langchain, we could also update the prompt passed to chatgpt model to con- tain a preamble asking the model to respond to the question with an answer if its present in the pro- vided context, else response with ’I don’t know’. This is a really powerful feature as it helps curb hallucinations and make sure that the QA model only provides with an answer if the information is present in the documents for sure.
As we made use of a embedding similarity match and LLM for finding answer from context doc- uments, our application is capable of answering questions from multiple novels.

2.4 User Interface
For our user interface, we designed a UI which is similar to chatgpt visually so that users can feel more comfortable with using a new application. We also added a visualization tab to present the performance of the model on each novel, the hit and miss rates as well as performance metrics.

2.5 Error Handling
We implemented extensive error handling in our application so that the user do not face an appli- cation failure or random error logs on the screen. This includes taking care of situations where the chatgpt api might be down or issues with the api key.


3 Conclusion
The application created is an intelligent chatbot comprising of state of the art large language mod- els. The application can identify, on the fly, the con- text of a user’s prompt and indulge them into either chit-chat or provide them with anchored answers to their questions along with the reference documents. Utilising Langchain and OpenAi model provides the application with new-world deep-learning wits and logic to provide accurate and coherent answers. Langchain also helped further strengthen knowl- edge anchoring by providing the model with the command to accept it does not know the answer to a given question instead of producing un-anchored hallucinated responses.
6 References
1. https://www.youtube.com/watch?v=Cim1lNXvCzY
2. https://www.langchain.com/
3. https://huggingface.co/docs/transformers/v4.15.0/examples


