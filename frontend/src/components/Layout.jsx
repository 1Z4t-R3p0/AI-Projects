import React from 'react';
import { BookOpen, MessageSquare, Map, CheckSquare, Plus, Trash2, History } from 'lucide-react';

const Layout = ({ children, activeTab, onTabChange, sessions = [], currentSessionId, onNewChat, onSwitchSession, onDeleteSession }) => {
    return (
        <div className="flex h-screen bg-gray-50">
            {/* Sidebar */}
            <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
                <div className="p-6 border-b border-gray-100">
                    <h1 className="text-2xl font-bold text-indigo-600 flex items-center gap-2">
                        <BookOpen className="w-8 h-8" />
                        EduPath AI
                    </h1>
                    <p className="text-xs text-gray-500 mt-1">Final Year Project</p>
                </div>

                <div className="p-4 pb-2">
                    <button
                        onClick={onNewChat}
                        className="w-full flex items-center justify-center gap-2 bg-indigo-600 text-white p-3 rounded-xl hover:bg-indigo-700 transition-colors shadow-sm font-medium"
                    >
                        <Plus size={18} />
                        New Chat
                    </button>
                </div>

                <nav className="p-4 space-y-2">
                    <NavButton
                        icon={<MessageSquare />}
                        label="AI Mentor"
                        active={activeTab === 'chat'}
                        onClick={() => onTabChange('chat')}
                    />
                    <NavButton
                        icon={<Map />}
                        label="Roadmap"
                        active={activeTab === 'roadmap'}
                        onClick={() => onTabChange('roadmap')}
                    />
                    <NavButton
                        icon={<CheckSquare />}
                        label="Productivity"
                        active={activeTab === 'productivity'}
                        onClick={() => onTabChange('productivity')}
                    />
                </nav>

                {/* History Section */}
                <div className="flex-1 overflow-y-auto border-t border-gray-100 p-4">
                    <h3 className="text-xs font-semibold text-gray-400 uppercase mb-3 flex items-center gap-1">
                        <History size={12} />
                        Recent History
                    </h3>
                    <div className="space-y-1">
                        {sessions.map(session => (
                            <div
                                key={session.id}
                                className={`group flex items-center justify-between p-2 rounded-lg text-sm cursor-pointer transition-colors ${session.id === currentSessionId
                                        ? 'bg-gray-100 text-gray-900 border border-gray-200'
                                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                                    }`}
                                onClick={() => onSwitchSession(session.id)}
                            >
                                <span className="truncate flex-1 pr-2">{session.title || 'New Chat'}</span>
                                <button
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        onDeleteSession(session.id);
                                    }}
                                    className="text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity p-1"
                                >
                                    <Trash2 size={14} />
                                </button>
                            </div>
                        ))}
                        {sessions.length === 0 && (
                            <p className="text-xs text-gray-400 italic text-center py-4">No history yet.</p>
                        )}
                    </div>
                </div>

                <div className="p-4 border-t border-gray-200 text-center text-xs text-gray-400">
                    v1.1.0 Session Enabled
                </div>
            </div>

            {/* Main Content */}
            <main className="flex-1 overflow-hidden relative">
                {children}
            </main>
        </div>
    );
};

const NavButton = ({ icon, label, active, onClick }) => (
    <button
        onClick={onClick}
        className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${active
            ? 'bg-indigo-50 text-indigo-600 font-semibold shadow-smring-1 ring-indigo-200'
            : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
            }`}
    >
        {React.cloneElement(icon, { size: 20 })}
        {label}
    </button>
);

export default Layout;
