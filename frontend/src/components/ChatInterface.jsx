import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Loader2 } from 'lucide-react';
import { chatWithAI, getChatHistory } from '../api';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const ChatInterface = ({ department, setDepartment, sessionId }) => {
    const [messages, setMessages] = useState([
        { role: 'ai', content: "Hello! I'm your AI Learning Roadmap Assistant. Choose your department and ask me anything!" }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const scrollRef = useRef(null);

    const departments = [
        "Cyber Security", "Computer Science", "Artificial Intelligence",
        "IoT", "Data Science", "Software Engineering"
    ];

    // Fetch history when sessionId changes
    useEffect(() => {
        const loadHistory = async () => {
            if (!sessionId) return;

            const history = await getChatHistory(sessionId);
            if (history && history.length > 0) {
                setMessages(history);
            } else {
                setMessages([{ role: 'ai', content: "Hello! I'm your AI Learning Roadmap Assistant. Choose your department and ask me anything!" }]);
            }
        };
        loadHistory();
    }, [sessionId]);

    // Scroll to bottom on messages update
    useEffect(() => {
        scrollRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMsg = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            const data = await chatWithAI(userMsg.content, department, sessionId);
            setMessages(prev => [...prev, { role: 'ai', content: data.response }]);
        } catch (err) {
            setMessages(prev => [...prev, { role: 'ai', content: "Sorry, I couldn't reach the server." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white">
            {/* Header / Department Selector */}
            <div className="p-4 border-b border-gray-100 flex justify-between items-center bg-white z-10">
                <div>
                    <h2 className="text-lg font-bold text-gray-800">AI Mentor Chat</h2>
                    <p className="text-sm text-gray-500">Constraint-based RAG Knowledge Base</p>
                </div>
                <select
                    value={department}
                    onChange={(e) => setDepartment(e.target.value)}
                    className="p-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
                >
                    {departments.map(dept => (
                        <option key={dept} value={dept}>{dept}</option>
                    ))}
                </select>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-gray-50/50">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`flex max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'} gap-3`}>
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-green-600 text-white'
                                }`}>
                                {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                            </div>
                            <div className={`p-4 rounded-2xl shadow-sm text-sm leading-relaxed ${msg.role === 'user'
                                ? 'bg-indigo-600 text-white rounded-tr-none'
                                : 'bg-white text-gray-800 border border-gray-100 rounded-tl-none prose prose-sm max-w-none'
                                }`}>
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                    {msg.content}
                                </ReactMarkdown>
                            </div>
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start gap-3">
                        <div className="w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center">
                            <Bot size={16} />
                        </div>
                        <div className="bg-white p-4 rounded-2xl rounded-tl-none border border-gray-100 shadow-sm flex items-center gap-2">
                            <Loader2 className="w-4 h-4 animate-spin text-indigo-600" />
                            <span className="text-sm text-gray-500">Generating response...</span>
                        </div>
                    </div>
                )}
                <div ref={scrollRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-white border-t border-gray-100">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Ask for a roadmap, resources, or advice..."
                        className="flex-1 p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
                    />
                    <button
                        onClick={handleSend}
                        disabled={loading}
                        className="p-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <Send size={20} />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ChatInterface;
