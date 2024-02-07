import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import ResponseTimeLineChart from './ResponseTimeLineChart'
import TopicDistributionBarChart from './TopicDistributionBarChart';

function Dashboard({ conversations, onClose, onReload }) {
    const [selectedConversationId, setSelectedConversationId] = useState(null);

    const selectedConversation = conversations[selectedConversationId];

    const aggregateTopicDistribution = calculateAggregateTopicDistribution(conversations);

    return (
        <div style={styles.container}>
          <h2 style={styles.title}>Chatbot Analytics Dashboard</h2>
    
          <select style={styles.selector} onChange={(e) => setSelectedConversationId(e.target.value)}>
            {/* Options */}
            <option key={"selectConv"} value={null}>Select a Conversation</option>
            {Object.keys(conversations).map((id) => (
                    <option key={id} value={id}>Conversation {id}</option>
                ))
            }
          </select>
    
          {selectedConversation && (
            <div style={styles.individualChartContainer}>
              <h3 style={styles.title}>Metrics for Conversation {selectedConversationId}</h3>
              <ul style={styles.conversationList}>
                {
                    selectedConversation.data.conversation_history.map((entry, index) => (
                        <li>{`Q${index + 1}: ` + entry.query}</li>
                    ))
                }
              </ul>
              <ResponseTimeLineChart 
                conversationHistory={selectedConversation.data.conversation_history}
              />
              <TopicDistributionBarChart
                conversation={selectedConversation.data}
              />
            </div>
          )}
    
          <div style={styles.overallChartContainer}>
            <h3>Overall Metrics</h3>
                <BarChart width={600} height={300} data={aggregateTopicDistribution} style={styles.barChart}>
                    <XAxis dataKey="topic" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="count" fill="#8884d8" />
                </BarChart>
          </div>
    
          <button style={styles.closeButton} onClick={onReload}>Reload Data</button>
          <button style={styles.closeButton} onClick={onClose}>Close Dashboard</button>
        </div>
      );
}

export default Dashboard;

function calculateAggregateTopicDistribution(conversations) {
    const topicCounts = {};
    Object.values(conversations).forEach(convData => {
        const conversation = convData.data
        Object.entries(conversation.topic_distribution || {}).forEach(([topic, count]) => {
            if (!topicCounts[topic]) {
                topicCounts[topic] = 0;
            }
            topicCounts[topic] += count;
        });
    });

    const data = Object.entries(topicCounts).map(([topic, count]) => ({ topic, count }));
    return data
}

const styles = {
    container: {
        minHeight: "100vh",
        padding: "20px",
        backgroundColor: "#f4f4f4",
        marginLeft: '250px'
    },
    title: {
        textAlign: "center",
        color: "#333",
        marginBottom: "20px",
    },
    selector: {
        display: "block",
        margin: "0 auto 20px",
        padding: "10px",
        maxWidth: "300px",
        fontSize: "16px",
    },
    individualChartContainer: {
        display: "flex",
        flexDirection: 'column',
        justifyContent: "center",
        paddingBottom: "20px",
    },
    overallChartContainer: {
        display: "flex",
        flexDirection: 'column',
        justifyContent: "center",
        marginBottom: "20px",
    },
    conversationList: {
        listStyle: "none",
        padding: "5px",
        maxHeight: "300px",
        overflowY: "auto",
        border: "1px solid #ddd",
        borderRadius: "5px",
    },
    conversationItem: {
        padding: "10px",
        borderBottom: "1px solid #ddd",
    },
    closeButton: {
        display: "block",
        margin: "20px auto",
        padding: "10px 20px",
        backgroundColor: "#007bff",
        color: "white",
        border: "none",
        borderRadius: "5px",
        cursor: "pointer",
    },
    barChart: {
        justifyContent: "center",
    }
};  