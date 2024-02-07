import React, { useState, useEffect } from 'react';
import './App.css';
import { v4 as uuidv4 } from 'uuid';
import EmptyConversationComponent from './emptyConvo';
import Dashboard from './Dashboard';

function App() {
  const [allConv, setAllConv] = useState({});
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [input, setInput] = useState('');
  const [showDashboard, setShowDashboard] = useState(false);

  const fetchConversations = async () => {
    try {
      const response = await fetch('http://34.0.47.210:5000/conversations', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        mode: 'cors'
      });

      if (response.ok) {
        const data = await response.json();
        const newConv = data.response.map((conv) => {
          return {
            "conv_id": conv.conv_id,
            "responses": conv.data?.conversation_history
          }
        })
        setAllConv(data.response);
        setConversations(newConv);
      } else {
        console.error('Error fetching conversations:', response.statusText);
      }
    } catch (error) {
      console.error('Error conversations:', error);
    }
  };

  useEffect(() => {
    fetchConversations();
  }, []);

  const switchConversation = (index) => {
    setCurrentConversation(index);
    setInput("")
    setShowDashboard(false);
  };

  const startNewConversation = () => {
    const newConvId = uuidv4();
    const newConversation = {
      conv_id: newConvId,
      responses: [],
    };
    setConversations([...conversations, newConversation]);
    setCurrentConversation(newConvId);
  };

  const sendChat = async () => {
    const response = await fetch('http://34.0.47.210:5000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({ input, conv_id: conversations[currentConversation].conv_id }),
    });
    const data = await response.json();
    const newConv = conversations[currentConversation]
    const newResponses = [...newConv.responses, { query: input, response: data.response }]
    newConv.responses = newResponses
    const newConvArray = [...conversations]
    newConvArray[currentConversation] = newConv

    setInput('');
    setConversations(newConvArray)
  };

  return (
    <div className="App">
      {
        showDashboard ?
          <Dashboard
            onClose={() => setShowDashboard(false)}
            conversations={allConv}
            onReload={fetchConversations}
          />
          :
          currentConversation != null ?
            (
              <header className="App-header">
                <div className="chat-container">
                  {conversations && conversations[currentConversation]?.responses?.map((res, index) => (
                    <div key={index}>
                      <p className="user-message"><b>You:</b> {res.query}</p>
                      <p className="bot-message"><b>Bot:</b> {res.response}</p>
                    </div>
                  ))}
                </div>
                <input value={input} onChange={(e) => setInput(e.target.value)} />
                <button onClick={sendChat}>Send</button>
              </header>
            ) : (
              <EmptyConversationComponent />
            )
      }
      <div className="sidebar">
        {conversations && conversations?.map((conversation, index) => (
          <button
            key={index}
            onClick={() => switchConversation(index)}
            className={index === currentConversation ? "active-conversation" : ""}
          >
            Conversation {conversation.conv_id}
          </button>
        ))}
        <button onClick={startNewConversation}>Start New Conversation</button>
        <button onClick={() => setShowDashboard(!showDashboard)}>{showDashboard ? "Close Dashboard" : "Show Dashboard"}</button>
      </div>

    </div>
  );
}

export default App;
