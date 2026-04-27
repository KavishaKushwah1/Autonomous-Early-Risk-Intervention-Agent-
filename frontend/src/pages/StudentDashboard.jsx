import { useState, useEffect } from 'react';
import { getStudentRecommendations } from '../api/aiAgent';

export default function StudentDashboard({ studentId }) {
    const [insights, setInsights] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getStudentRecommendations(studentId)
            .then(res => setInsights(res.data.data))
            .finally(() => setLoading(false));
    }, [studentId]);

    if (loading) return <div className="p-8 text-center">AI is analyzing your profile...</div>;

    const riskColor = {
        low: 'bg-green-100 text-green-800',
        medium: 'bg-yellow-100 text-yellow-800',
        high: 'bg-red-100 text-red-800'
    };

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6">
            {/* Overall Assessment */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
                <div className="flex justify-between items-start">
                    <h2 className="text-xl font-medium text-gray-900">Your AI Assessment</h2>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${riskColor[insights.risk_level]}`}>
                        {insights.risk_level} risk
                    </span>
                </div>
                <p className="mt-3 text-gray-600">{insights.overall_assessment}</p>
                <p className="mt-2 text-sm text-blue-600">
                    Trajectory: <strong>{insights.predicted_trajectory}</strong>
                </p>
            </div>

            {/* Strengths */}
            <div className="bg-green-50 rounded-xl border border-green-200 p-6">
                <h3 className="font-medium text-green-900 mb-3">Your Strengths</h3>
                <ul className="space-y-2">
                    {insights.strengths.map((s, i) => (
                        <li key={i} className="flex items-start gap-2 text-green-800">
                            <span className="text-green-500 mt-0.5">✓</span> {s}
                        </li>
                    ))}
                </ul>
            </div>

            {/* Recommendations */}
            <div className="bg-blue-50 rounded-xl border border-blue-200 p-6">
                <h3 className="font-medium text-blue-900 mb-3">AI Recommendations</h3>
                <ul className="space-y-2">
                    {insights.academic_recommendations.map((r, i) => (
                        <li key={i} className="flex items-start gap-2 text-blue-800">
                            <span className="text-blue-400 font-bold">{i + 1}.</span> {r}
                        </li>
                    ))}
                </ul>
            </div>

            {/* Wellbeing */}
            <div className="bg-purple-50 rounded-xl border border-purple-200 p-6">
                <h3 className="font-medium text-purple-900 mb-2">Wellbeing Observation</h3>
                <p className="text-purple-800">{insights.wellbeing_observations}</p>
            </div>
        </div>
    );
}