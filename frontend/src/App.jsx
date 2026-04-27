import { useState } from 'react'
import StudentDashboard from './pages/StudentDashboard'
import TeacherDashboard from './pages/TeacherDashboard'
import AddData from './pages/AddData'

export default function App() {
  const [page, setPage] = useState('home')

  return (
    <div style={{ fontFamily: "'DM Sans', sans-serif" }} className="min-h-screen bg-[#0a0a0f] text-white">
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Syne:wght@600;700;800&display=swap" rel="stylesheet" />

      {/* Ambient background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] rounded-full opacity-20"
          style={{ background: 'radial-gradient(circle, #3b82f6 0%, transparent 70%)' }} />
        <div className="absolute bottom-[-20%] right-[-10%] w-[500px] h-[500px] rounded-full opacity-15"
          style={{ background: 'radial-gradient(circle, #8b5cf6 0%, transparent 70%)' }} />
        <div className="absolute top-[40%] left-[50%] w-[400px] h-[400px] rounded-full opacity-10"
          style={{ background: 'radial-gradient(circle, #06b6d4 0%, transparent 70%)' }} />
      </div>

      {/* Navbar */}
      <nav className="relative z-10 flex items-center gap-2 px-8 py-5 border-b border-white/5 backdrop-blur-sm bg-white/[0.02]">
        <div className="flex items-center gap-2 mr-8">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center text-sm">🎓</div>
          <span style={{ fontFamily: "'Syne', sans-serif" }} className="font-bold text-white tracking-tight">EduAgent</span>
        </div>
        {[
          { id: 'home', label: 'Home' },
          { id: 'student', label: 'Students' },
          { id: 'teacher', label: 'Teachers' },
          { id: 'add', label: 'Add Data' },
        ].map(item => (
          <button key={item.id} onClick={() => setPage(item.id)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
              page === item.id
                ? 'bg-white/10 text-white border border-white/20'
                : 'text-white/40 hover:text-white/70 hover:bg-white/5'
            }`}>
            {item.label}
          </button>
        ))}
      </nav>

      {/* Content */}
      <div className="relative z-10">
        {page === 'home' && <Home nav={setPage} />}
        {page === 'student' && <StudentDashboard />}
        {page === 'teacher' && <TeacherDashboard />}
        {page === 'add' && <AddData />}
      </div>
    </div>
  )
}

function Home({ nav }) {
  const stats = [
    { value: '10+', label: 'Data Points Tracked' },
    { value: 'AI', label: 'Gemini 2.5 Flash' },
    { value: '360°', label: 'Student View' },
  ]

  const cards = [
    {
      id: 'student', icon: '👨‍🎓', label: 'Student Dashboard',
      desc: 'AI-powered performance analysis, risk detection & recommendations',
      accent: 'from-blue-500/20 to-blue-600/5', border: 'hover:border-blue-500/40',
      tag: 'AI Insights'
    },
    {
      id: 'teacher', icon: '👨‍🏫', label: 'Teacher Dashboard',
      desc: 'Anonymous feedback analysis, mentoring records & sentiment tracking',
      accent: 'from-violet-500/20 to-violet-600/5', border: 'hover:border-violet-500/40',
      tag: 'Feedback AI'
    },
    {
      id: 'add', icon: '⚡', label: 'Data Entry',
      desc: 'Add students, academic records, attendance, activities & more',
      accent: 'from-cyan-500/20 to-cyan-600/5', border: 'hover:border-cyan-500/40',
      tag: 'Management'
    },
  ]

  return (
    <div className="max-w-5xl mx-auto px-8 pt-24 pb-16">
      {/* Hero */}
      <div className="text-center mb-20">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-medium mb-8">
          <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse"></span>
          Powered by Gemini 2.5 Flash
        </div>
        <h1 style={{ fontFamily: "'Syne', sans-serif" }}
          className="text-6xl font-extrabold tracking-tight mb-6 leading-tight">
          Autonomous Early
          <span className="block text-transparent bg-clip-text"
            style={{ backgroundImage: 'linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4)' }}>
            Risk Intervention
          </span>
        </h1>
        <p className="text-white/40 text-lg max-w-xl mx-auto leading-relaxed">
          AI-powered student intelligence platform that monitors, analyzes, and intervenes before students fall behind.
        </p>
      </div>

      {/* Stats */}
      <div className="flex justify-center gap-16 mb-20">
        {stats.map(s => (
          <div key={s.label} className="text-center">
            <div style={{ fontFamily: "'Syne', sans-serif" }}
              className="text-3xl font-bold text-white mb-1">{s.value}</div>
            <div className="text-white/30 text-xs uppercase tracking-widest">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Cards */}
      <div className="grid grid-cols-3 gap-5">
        {cards.map(card => (
          <button key={card.id} onClick={() => nav(card.id)}
            className={`group relative text-left p-6 rounded-2xl border border-white/8 bg-gradient-to-br ${card.accent} ${card.border} transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl`}>
            <div className="flex justify-between items-start mb-5">
              <span className="text-3xl">{card.icon}</span>
              <span className="text-xs text-white/30 border border-white/10 rounded-full px-2 py-0.5">{card.tag}</span>
            </div>
            <div style={{ fontFamily: "'Syne', sans-serif" }}
              className="font-bold text-white text-lg mb-2">{card.label}</div>
            <div className="text-white/40 text-sm leading-relaxed">{card.desc}</div>
            <div className="mt-5 flex items-center gap-1 text-white/30 text-xs group-hover:text-white/60 transition-colors">
              Open <span className="group-hover:translate-x-1 transition-transform inline-block">→</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}