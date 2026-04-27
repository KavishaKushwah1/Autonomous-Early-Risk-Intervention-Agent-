import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:8000/api' });

// Attach token to every request
API.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

export const getStudentRecommendations = (studentId) =>
    API.get(`/ai/student/${studentId}/recommendations`);

export const getParentReport = (studentId, month, year) =>
    API.get(`/ai/student/${studentId}/parent-report`, { params: { month, year } });

export const getTeacherFeedbackAnalysis = (teacherId) =>
    API.get(`/ai/teacher/${teacherId}/feedback-analysis`);

export const submitAnonymousFeedback = (teacherId, feedbackText, rating) =>
    API.post(`/ai/student/feedback`, null, {
        params: { teacher_id: teacherId, feedback_text: feedbackText, rating }
    });