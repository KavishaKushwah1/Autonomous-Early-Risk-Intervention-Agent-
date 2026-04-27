import axios from 'axios'

const API = axios.create({ baseURL: 'http://localhost:8000/api' })

export const createStudent = (data) => API.post('/students/', data)
export const getAllStudents = () => API.get('/students/')
export const getStudent = (id) => API.get(`/students/${id}`)
export const addAcademic = (data) => API.post('/students/academic', data)
export const markAttendance = (data) => API.post('/students/attendance', data)
export const addActivity = (data) => API.post('/students/activity', data)
export const addLibraryVisit = (data) => API.post('/students/library', data)
export const updateStreak = (data) => API.post('/students/streak', data)

export const createTeacher = (data) => API.post('/teachers/', data)
export const getAllTeachers = () => API.get('/teachers/')
export const submitFeedback = (data) => API.post('/teachers/feedback', data)
export const sendMessage = (data) => API.post('/teachers/message', data)

export const getRecommendations = (id) => API.get(`/ai/student/${id}/recommendations`)
export const getParentReport = (id, month, year) => API.get(`/ai/student/${id}/parent-report`, { params: { month, year } })
export const getFeedbackAnalysis = (id) => API.get(`/ai/teacher/${id}/feedback-analysis`)