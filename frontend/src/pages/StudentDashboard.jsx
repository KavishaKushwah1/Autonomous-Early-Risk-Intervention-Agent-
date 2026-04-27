import { useState } from 'react'
import { getAllStudents, getRecommendations, getParentReport } from '../api'

export default function StudentDashboard() {
  const [students, setStudents] = useState([])
  const [selected, setSelected] = useState(null)
  const [insights, setInsights] = useState(null)
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(false)

  const loadStudents = async () => {
    const res = await getAllStudents()
    setStudents(res.data)
  }

  const analyze = async (id) => {
    setLoading(true)
    setInsights(null)
    setReport(null)
    try {
      const res = await getRecommendations(id)
      setInsights(res.data.data)
      setSelected(id)
    } catch(e) {
      alert('AI error: ' + e.message)
    }
    setLoading(false)
  }

  const fetchReport = async () => {
    setLoading(true)
    const now = new Date()
    const res = await getParentReport(selected, now.getMonth() + 1, now.getFullYear())
    setReport(res.data.report)
    setLoading(false)
  }

  const riskColor = { low: 'text-green-400', medium: 'text-yellow-400', high: 'text-red-400' }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Student Dashboard</h2>
        <button onClick={loadStudents} className="bg-blue-600 px-4 py-2 rounded-lg text-sm hover:bg-blue-700">
          Load Students
        </button>
      </div>

      {/* Student List */}
      {students.length > 0 && (
        <div className="grid grid-cols-3 gap-3">
          {students.map(s => (
            <button
              key={s.id}
              onClick={() => analyze(s.id)}
              className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-left hover:border-blue-500 transition"
            >
              <div className="font-medium">{s.name}</div>
              <div className="text-gray-400 text-sm">{s.class_section} · {s.roll_number}</div>
            </button>
          ))}
        </div>
      )}

      {loading && <div className="text-center text-blue-400 py-10">🤖 AI is analyzing...</div>}

      {/* AI Insights */}
      {insights && (
        <div className="space-y-4">
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <div className="flex justify-between items-start">
              <h3 className="font-semibold text-lg">AI Assessment</h3>
              <span className={`font-bold ${riskColor[insights.risk_level]}`}>
                {insights.risk_level?.toUpperCase()} RISK
              </span>
            </div>
            <p className="text-gray-300 mt-3">{insights.overall_assessment}</p>
            <p className="text-blue-400 text-sm mt-2">Trajectory: {insights.predicted_trajectory}</p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-900 border border-green-900 rounded-xl p-5">
              <h4 className="text-green-400 font-medium mb-3">✓ Strengths</h4>
              <ul className="space-y-1">
                {insights.strengths?.map((s, i) => (
                  <li key={i} className="text-gray-300 text-sm">• {s}</li>
                ))}
              </ul>
            </div>
            <div className="bg-gray-900 border border-red-900 rounded-xl p-5">
              <h4 className="text-red-400 font-medium mb-3">⚠ Concerns</h4>
              <ul className="space-y-1">
                {insights.areas_of_concern?.map((c, i) => (
                  <li key={i} className="text-gray-300 text-sm">• {c}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="bg-gray-900 border border-blue-900 rounded-xl p-5">
            <h4 className="text-blue-400 font-medium mb-3">📚 Recommendations</h4>
            <ul className="space-y-2">
              {insights.academic_recommendations?.map((r, i) => (
                <li key={i} className="text-gray-300 text-sm">{i+1}. {r}</li>
              ))}
            </ul>
          </div>

          <div className="bg-gray-900 border border-purple-900 rounded-xl p-5">
            <h4 className="text-purple-400 font-medium mb-2">💌 Parent Message</h4>
            <p className="text-gray-300 text-sm">{insights.parent_message}</p>
          </div>

          <button
            onClick={fetchReport}
            className="w-full bg-purple-700 hover:bg-purple-800 py-3 rounded-xl font-medium transition"
          >
            Generate Full Monthly Parent Report
          </button>

          {report && (
            <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
              <h4 className="font-medium mb-3 text-purple-400">📄 Monthly Parent Report</h4>
              <p className="text-gray-300 text-sm whitespace-pre-line">{report}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}