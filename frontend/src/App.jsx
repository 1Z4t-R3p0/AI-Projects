import React, { useState, useEffect } from 'react';
import Layout from './components/Layout';
import ChatInterface from './components/ChatInterface';
import RoadmapView from './components/RoadmapView';
import ProductivityView from './components/ProductivityView';
import { deleteSession as deleteSessionApi } from './api';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [department, setDepartment] = useState('Cyber Security');
  const [sessions, setSessions] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState('');

  // Load sessions from localStorage on mount
  useEffect(() => {
    const storedSessions = JSON.parse(localStorage.getItem('chat_sessions') || '[]');
    const storedCurrentId = localStorage.getItem('current_session_id');

    if (storedSessions.length > 0) {
      setSessions(storedSessions);
      setCurrentSessionId(storedCurrentId || storedSessions[0].id);
    } else {
      createNewSession();
    }
  }, []);

  // Save sessions to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('chat_sessions', JSON.stringify(sessions));
  }, [sessions]);

  // Save current session ID
  useEffect(() => {
    if (currentSessionId) {
      localStorage.setItem('current_session_id', currentSessionId);
    }
  }, [currentSessionId]);

  const createNewSession = () => {
    const newSession = {
      id: crypto.randomUUID(),
      title: `Chat ${new Date().toLocaleTimeString()}`, // Temporary title
      date: new Date().toISOString()
    };
    setSessions(prev => [newSession, ...prev]);
    setCurrentSessionId(newSession.id);
    setActiveTab('chat');
  };

  const switchSession = (id) => {
    setCurrentSessionId(id);
    setActiveTab('chat');
  };

  const deleteSession = async (id) => {
    // Call backend API to delete session data
    await deleteSessionApi(id);

    const updatedSessions = sessions.filter(s => s.id !== id);
    setSessions(updatedSessions);

    if (id === currentSessionId) {
      if (updatedSessions.length > 0) {
        setCurrentSessionId(updatedSessions[0].id);
      } else {
        createNewSession();
      }
    }
  };

  return (
    <Layout
      activeTab={activeTab}
      onTabChange={setActiveTab}
      sessions={sessions}
      currentSessionId={currentSessionId}
      onNewChat={createNewSession}
      onSwitchSession={switchSession}
      onDeleteSession={deleteSession}
    >
      {activeTab === 'chat' && (
        <ChatInterface
          department={department}
          setDepartment={setDepartment}
          sessionId={currentSessionId}
        />
      )}
      {activeTab === 'roadmap' && (
        <RoadmapView department={department} />
      )}
      {activeTab === 'productivity' && (
        <ProductivityView sessionId={currentSessionId} />
      )}
    </Layout>
  );
}

export default App;
