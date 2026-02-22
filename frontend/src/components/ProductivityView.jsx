import React, { useState, useEffect } from 'react';
import { getTasks, addTask, updateTask, deleteTask, logStudySession, getAnalytics } from '../api';
import { Plus, Trash2, CheckSquare, Clock, BarChart2, Play, Pause, RotateCcw } from 'lucide-react';

const ProductivityView = ({ sessionId }) => {
    const [tasks, setTasks] = useState([]);
    const [newTask, setNewTask] = useState("");
    const [analytics, setAnalytics] = useState(null);

    // Timer State
    const [timeLeft, setTimeLeft] = useState(25 * 60); // 25 minutes
    const [isActive, setIsActive] = useState(false);
    const [timerMode, setTimerMode] = useState("focus"); // focus | break

    useEffect(() => {
        if (sessionId) loadData();
    }, [sessionId]);

    useEffect(() => {
        let interval = null;
        if (isActive && timeLeft > 0) {
            interval = setInterval(() => {
                setTimeLeft(timeLeft - 1);
            }, 1000);
        } else if (timeLeft === 0) {
            setIsActive(false);
            if (timerMode === "focus") {
                logStudySession(sessionId, 25); // Log 25 mins
                alert("Focus session complete! Take a break.");
                loadData(); // Refresh analytics
            }
        }
        return () => clearInterval(interval);
    }, [isActive, timeLeft, timerMode]);

    const loadData = async () => {
        const t = await getTasks(sessionId);
        const a = await getAnalytics(sessionId);
        setTasks(t || []);
        setAnalytics(a);
    };

    const handleAddTask = async (e) => {
        e.preventDefault();
        if (!newTask.trim()) return;
        const task = { title: newTask, session_id: sessionId, completed: false };
        const created = await addTask(task);
        if (created) setTasks([...tasks, created]);
        setNewTask("");
        loadData(); // Refresh stats
    };

    const toggleTask = async (task) => {
        const updated = { ...task, completed: !task.completed };
        // Optimistic update
        setTasks(tasks.map(t => t.id === task.id ? updated : t));
        await updateTask(sessionId, task.id, { completed: updated.completed });
        loadData();
    };

    const handleDelete = async (id) => {
        setTasks(tasks.filter(t => t.id !== id));
        await deleteTask(sessionId, id);
        loadData();
    };

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    };

    const resetTimer = () => {
        setIsActive(false);
        setTimeLeft(25 * 60);
        setTimerMode("focus");
    };

    return (
        <div className="h-full overflow-y-auto bg-gray-50 p-6">
            <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">

                {/* 1. Task Manager */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 md:col-span-1">
                    <div className="flex items-center gap-2 mb-6 text-indigo-600">
                        <CheckSquare className="w-5 h-5" />
                        <h2 className="text-xl font-bold">Tasks</h2>
                    </div>

                    <form onSubmit={handleAddTask} className="flex gap-2 mb-4">
                        <input
                            type="text"
                            value={newTask}
                            onChange={(e) => setNewTask(e.target.value)}
                            placeholder="Add a new task..."
                            disabled={!sessionId}
                            title={!sessionId ? "Please select or create a chat session first" : ""}
                            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                        />
                        <button
                            type="submit"
                            disabled={!sessionId}
                            className="p-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-indigo-300 disabled:cursor-not-allowed"
                        >
                            <Plus className="w-5 h-5" />
                        </button>
                    </form>

                    <ul className="space-y-3 max-h-[500px] overflow-y-auto">
                        {tasks.map(task => (
                            <li key={task.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg group">
                                <div className="flex items-center gap-3">
                                    <input
                                        type="checkbox"
                                        checked={task.completed}
                                        onChange={() => toggleTask(task)}
                                        className="w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500"
                                    />
                                    <span className={`text-sm ${task.completed ? 'line-through text-gray-400' : 'text-gray-700'}`}>
                                        {task.title}
                                    </span>
                                </div>
                                <button onClick={() => handleDelete(task.id)} className="text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <Trash2 className="w-4 h-4" />
                                </button>
                            </li>
                        ))}
                        {tasks.length === 0 && <p className="text-gray-400 text-center text-sm py-4">No tasks yet. Add one!</p>}
                    </ul>
                </div>

                {/* 2. Focus Timer */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 md:col-span-1 flex flex-col items-center justify-center">
                    <div className="flex items-center gap-2 mb-6 text-indigo-600">
                        <Clock className="w-5 h-5" />
                        <h2 className="text-xl font-bold">Focus Timer</h2>
                    </div>

                    <div className="relative w-48 h-48 flex items-center justify-center border-4 border-indigo-100 rounded-full mb-8">
                        <span className="text-5xl font-mono text-gray-800 font-bold">{formatTime(timeLeft)}</span>
                    </div>

                    <div className="flex gap-4">
                        <button onClick={() => setIsActive(!isActive)} className="px-6 py-2 bg-indigo-600 text-white rounded-full font-semibold hover:bg-indigo-700 flex items-center gap-2">
                            {isActive ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                            {isActive ? "Pause" : "Start"}
                        </button>
                        <button onClick={resetTimer} className="p-2 text-gray-500 hover:bg-gray-100 rounded-full">
                            <RotateCcw className="w-5 h-5" />
                        </button>
                    </div>
                    <p className="mt-4 text-sm text-gray-400">25m Focus • 5m Break</p>
                </div>

                {/* 3. Analytics */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 md:col-span-1">
                    <div className="flex items-center gap-2 mb-6 text-indigo-600">
                        <BarChart2 className="w-5 h-5" />
                        <h2 className="text-xl font-bold">Analytics</h2>
                    </div>

                    {analytics ? (
                        <div className="space-y-6">
                            <div className="bg-indigo-50 p-4 rounded-xl">
                                <p className="text-sm text-gray-500 mb-1">Total Study Time</p>
                                <p className="text-3xl font-bold text-indigo-700">{analytics.study_stats.total_minutes} <span className="text-sm font-normal">mins</span></p>
                                <p className="text-xs text-indigo-400 mt-1">{analytics.study_stats.total_sessions} sessions completed</p>
                            </div>

                            <div className="bg-green-50 p-4 rounded-xl">
                                <p className="text-sm text-gray-500 mb-1">Tasks Completed</p>
                                <p className="text-3xl font-bold text-green-700">{analytics.task_stats.completed} <span className="text-sm font-normal">/ {analytics.task_stats.total}</span></p>
                                <div className="w-full bg-green-200 h-2 rounded-full mt-2">
                                    <div
                                        className="bg-green-600 h-2 rounded-full transition-all duration-500"
                                        style={{ width: `${analytics.task_stats.total ? (analytics.task_stats.completed / analytics.task_stats.total) * 100 : 0}%` }}
                                    ></div>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <p className="text-center text-gray-400">Loading stats...</p>
                    )}
                </div>

            </div>
        </div>
    );
};

export default ProductivityView;
