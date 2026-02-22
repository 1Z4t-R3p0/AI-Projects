import axios from 'axios';

const API_BASE_URL = "/api";

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

export const chatWithAI = async (message, department, session_id) => {
    try {
        const response = await api.post("/chat/query", { message, department, session_id });
        return response.data;
    } catch (error) {
        console.error("Chat Error:", error);
        return { response: "Error: Unable to connect to AI backend." };
    }
};

export const getChatHistory = async (session_id) => {
    try {
        const response = await api.get(`/chat/history/${session_id}`);
        return response.data.history;
    } catch (error) {
        console.error("History Error:", error);
        return [];
    }
};

export const deleteSession = async (session_id) => {
    try {
        await api.delete(`/chat/session/${session_id}`);
    } catch (error) {
        console.error("Delete Session Error:", error);
    }
};

export const generateRoadmap = async (department, level) => {
    try {
        const response = await api.post("/roadmap/generate", { department, level });
        return response.data;
    } catch (error) {
        console.error("Roadmap Error:", error);
        return null;
    }
};

// --- Productivity API ---

export const getTasks = async (session_id) => {
    try {
        const response = await api.get(`/productivity/tasks/${session_id}`);
        return response.data;
    } catch (error) { return []; }
};

export const addTask = async (task) => {
    try {
        const response = await api.post("/productivity/tasks", task);
        return response.data;
    } catch (error) { return null; }
};

export const updateTask = async (session_id, task_id, update) => {
    try {
        await api.put(`/productivity/tasks/${session_id}/${task_id}`, update);
    } catch (error) { console.error(error); }
};

export const deleteTask = async (session_id, task_id) => {
    try {
        await api.delete(`/productivity/tasks/${session_id}/${task_id}`);
    } catch (error) { console.error(error); }
};

export const logStudySession = async (session_id, minutes) => {
    try {
        await api.post("/productivity/timer/log", { session_id, minutes });
    } catch (error) { console.error(error); }
};

export const getAnalytics = async (session_id) => {
    try {
        const response = await api.get(`/productivity/analytics/${session_id}`);
        return response.data;
    } catch (error) { return null; }
};
