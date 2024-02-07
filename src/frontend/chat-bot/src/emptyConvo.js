import React from 'react';

const EmptyConversationComponent = ({ onStartNewConversation }) => {
  return (
    <div style={styles.container}>
      <h2 style={styles.header}>No Conversation Selected</h2>
      <p style={styles.text}>Please select a conversation from the list, or start a new one.</p>
    </div>
  );
};

// Styling for the component
const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100%', // Adjust as needed
    textAlign: 'center',
    color: '#FFFFFF',
    backgroundColor: '#282c34',
    minHeight: '100vh'
  },
  header: {
    marginBottom: '20px',
  },
  text: {
    marginBottom: '20px',
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    cursor: 'pointer',
  },
};

export default EmptyConversationComponent;
