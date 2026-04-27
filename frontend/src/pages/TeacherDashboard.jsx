import { useState } from 'react'
import { getAllTeachers, getFeedbackAnalysis } from '../api'

export default function TeacherDashboard() {
  const [teachers, setTeachers] = useState([])
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)

  const loadTeachers = async () => {
    const res = await getAllTeachers()
    setTeachers(res.data)
  }

  const analyze = async (id) => {
    setLoading(true)
    setAnalysis(null)
    try {
      const res = await getFeedbackAnalysis(id)
      setAnalysis(res.data)
    } catch(e) {
      alert('Error: ' + e.message)
    }
    setLoading(false)
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Teacher Dashboard</h2>
        <button onClick={loadTeachers} className="bg-blue-600 px-4 py-2 rounded-lg text-sm hover:bg-blue-700">
          Load Teachers
        </button>
      </div>

      {teachers.length > 0 && (
        <div className="grid grid-cols-3 gap-3">
          {teachers.map(t => (
            <button
              key={t.id}
              onClick={() => analyze(t.id)}
              className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-left hover:border-blue-500 transition"
            >
              <div className="font-medium">{t.name}</div>
              <div className="text-gray-400 text-sm">{t.subject}</div>
            </button>
          ))}
        </div>
      )}

      {loading && <div className="text-center text-blue-400 py-10">🤖 Analyzing feedback...</div>}

      {analysis && (
        <div className="space-y-4">
          {analysis.message ? (
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 text-gray-400">
              {analysis.message}
            </div>
          ) : (
            <>
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
                <div className="flex justify-between">
                  <h3 className="font-semibold">Feedback Analysis</h3>
                  <span className="text-yellow-400 font-bold">⭐ {analysis.avg_rating}/5</span>
                </div>
                <p className="text-gray-300 mt-3 text-sm">{analysis.analysis?.sentiment_summary}</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-900 border border-green-900 rounded-xl p-5">
                  <h4 className="text-green-400 font-medium mb-3">👍 Positives</h4>
                  <ul className="space-y-1">
                    {analysis.analysis?.key_positives?.map((p, i) => (
                      <li key={i} className="text-gray-300 text-sm">• {p}</li>
                    ))}
                  </ul>
                </div>
                <div className="bg-gray-900 border border-red-900 rounded-xl p-5">
                  <h4 className="text-red-400 font-medium mb-3">⚠ Concerns</h4>
                  <ul className="space-y-1">
                    {analysis.analysis?.key_concerns?.map((c, i) => (
                      <li key={i} className="text-gray-300 text-sm">• {c}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="bg-gray-900 border border-blue-900 rounded-xl p-5">
                <h4 className="text-blue-400 font-medium mb-3">💡 Suggestions</h4>
                <ul className="space-y-1">
                  {analysis.analysis?.actionable_suggestions?.map((s, i) => (
                    <li key={i} className="text-gray-300 text-sm">{i+1}. {s}</li>
                  ))}
                </ul>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  )
}