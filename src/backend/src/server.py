from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from conversation import Conversation
from conversation_state import ConversationState
import warnings
__import__('pysqlite3')
import sys
import threading
import json
from datetime import datetime
import time

warnings.filterwarnings("ignore")
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

app = Flask(__name__)
CORS(app)

convo = Conversation()
conversations = {}
interval = 300  
file_path = '/home/bhargavclick/cse535-p3/data/conversations.json'

def save_conversations_to_file(interval, file_path):
    # while True:
        # time.sleep(interval)  
    data_to_save = {
        'timestamp': datetime.now().isoformat(),
        'conversations': {conv_id: conv.serialize() for conv_id, conv in conversations.items()}
    }
    with open(file_path, 'w') as file:
        json.dump(data_to_save, file)
        file.write('\n')

def load_conversations_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                # Load the most recent state (last line in the file)
                data = json.loads(lines[-1])
                conversations_data = data['conversations']

                for conv_id, conv_data in conversations_data.items():
                    # print("Lets deserialize", conv_data)
                    conversations[conv_id] = ConversationState.from_serialized(conv_data)
                
    except FileNotFoundError:
        print(f"No existing file found at {file_path}. Starting with empty conversations.")
    except json.JSONDecodeError:
        print("Error decoding JSON from file. Ensure the file is correctly formatted.")


# thread = threading.Thread(target=save_conversations_to_file, args=(interval, file_path))
# thread.daemon = True
# thread.start()

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST":
        data = request.json
        user_input = data.get('input')
        conv_id = data.get('conv_id')

        if conv_id not in conversations:
            conversations[conv_id] = ConversationState()
        state = conversations[conv_id]

        start_time = datetime.now() 
        response = convo.talk(user_input, state)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        state.add_to_history(user_input, response, duration)

        save_conversations_to_file(interval, file_path)
        return jsonify({'response': response})

@app.route('/conversations', methods=['GET'])
@cross_origin()
def get_conversations():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    
    conv_id = request.args.get('conv_id')

    if conv_id:
        if conv_id in conversations:
            resp = {
                "conv_id": conv_id,
                "data": conversations[conv_id].serialize()
            }
            return jsonify({"response": resp})
        else:
            return jsonify({"error": "Conversation not found"}), 404
    else:
        resp = []
        for id, conv in conversations.items():
            resp.append({
                "conv_id": id,
                "data": conv.serialize()
            })
        return jsonify({"response": resp})

if __name__ == '__main__':
    load_conversations_from_file(file_path)
    app.run(host='0.0.0.0', port=5000, debug=True)
