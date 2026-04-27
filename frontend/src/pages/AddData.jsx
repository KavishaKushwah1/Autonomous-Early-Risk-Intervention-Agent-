import { useState } from 'react'
import { createStudent, createTeacher, addAcademic, markAttendance, addActivity, submitFeedback } from '../api'

export default function AddData() {
  const [tab, setTab] = useState('student')
  const [msg, setMsg] = useState('')
  const [form, setForm] = useState({})

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))
  const success = (m) => { setMsg('✅ ' + m); setForm({}) }
  const fail = (e) => setMsg('❌ Error: ' + e.message)

  const tabs = ['student', 'teacher', 'academic', 'attendance', 'activity', 'feedback']

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h2 className="text-xl font-semibold">Add Data</h2>

      <div className="flex gap-2 flex-wrap">
        {tabs.map(t => (
          <button key={t} onClick={() => { setTab(t); setMsg(''); setForm({}) }}
            className={`px-3 py-1 rounded-lg text-sm capitalize ${tab === t ? 'bg-blue-600' : 'bg-gray-800 hover:bg-gray-700'}`}>
            {t}
          </button>
        ))}
      </div>

      {msg && <div className="bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-sm">{msg}</div>}

      {/* Student Form */}
      {tab === 'student' && (
        <Form title="Add Student" onSubmit={async () => {
          await createStudent(form).then(() => success('Student added!')).catch(fail)
        }}>
          <Input label="Name" onChange={v => set('name', v)} value={form.name} />
          <Input label="Roll Number" onChange={v => set('roll_number', v)} value={form.roll_number} />
          <Input label="Class Section (e.g. 10-A)" onChange={v => set('class_section', v)} value={form.class_section} />
          <Input label="Email" onChange={v => set('email', v)} value={form.email} />
          <Input label="Parent Email" onChange={v => set('parent_email', v)} value={form.parent_email} />
        </Form>
      )}

      {/* Teacher Form */}
      {tab === 'teacher' && (
        <Form title="Add Teacher" onSubmit={async () => {
          await createTeacher(form).then(() => success('Teacher added!')).catch(fail)
        }}>
          <Input label="Name" onChange={v => set('name', v)} value={form.name} />
          <Input label="Email" onChange={v => set('email', v)} value={form.email} />
          <Input label="Subject" onChange={v => set('subject', v)} value={form.subject} />
        </Form>
      )}

      {/* Academic Form */}
      {tab === 'academic' && (
        <Form title="Add Academic Record" onSubmit={async () => {
          await addAcademic({ ...form, score: +form.score, max_score: +(form.max_score || 100), submitted_on_time: form.submitted_on_time !== 'false' })
            .then(() => success('Record added!')).catch(fail)
        }}>
          <Input label="Student ID" onChange={v => set('student_id', v)} value={form.student_id} />
          <Input label="Subject" onChange={v => set('subject', v)} value={form.subject} />
          <Input label="Score" type="number" onChange={v => set('score', v)} value={form.score} />
          <Input label="Max Score" type="number" onChange={v => set('max_score', v)} value={form.max_score} />
          <Select label="Exam Type" options={['unit_test','midterm','final','assignment']} onChange={v => set('exam_type', v)} value={form.exam_type} />
          <Select label="Submitted On Time" options={['true','false']} onChange={v => set('submitted_on_time', v)} value={form.submitted_on_time} />
        </Form>
      )}

      {/* Attendance Form */}
      {tab === 'attendance' && (
        <Form title="Mark Attendance" onSubmit={async () => {
          await markAttendance({ ...form, lms_activity_duration: +(form.lms_activity_duration || 0) })
            .then(() => success('Attendance marked!')).catch(fail)
        }}>
          <Input label="Student ID" onChange={v => set('student_id', v)} value={form.student_id} />
          <Select label="Status" options={['present','absent','late']} onChange={v => set('status', v)} value={form.status} />
          <Input label="LMS Duration (minutes)" type="number" onChange={v => set('lms_activity_duration', v)} value={form.lms_activity_duration} />
        </Form>
      )}

      {/* Activity Form */}
      {tab === 'activity' && (
        <Form title="Add Activity" onSubmit={async () => {
          await addActivity(form).then(() => success('Activity added!')).catch(fail)
        }}>
          <Input label="Student ID" onChange={v => set('student_id', v)} value={form.student_id} />
          <Select label="Category" options={['sports','arts','competition','club']} onChange={v => set('category', v)} value={form.category} />
          <Input label="Activity Name" onChange={v => set('activity_name', v)} value={form.activity_name} />
          <Input label="Achievement (optional)" onChange={v => set('achievement', v)} value={form.achievement} />
        </Form>
      )}

      {/* Feedback Form */}
      {tab === 'feedback' && (
        <Form title="Submit Anonymous Feedback" onSubmit={async () => {
          await submitFeedback({ ...form, rating: +form.rating })
            .then(() => success('Feedback submitted!')).catch(fail)
        }}>
          <Input label="Teacher ID" onChange={v => set('teacher_id', v)} value={form.teacher_id} />
          <Input label="Feedback Text" onChange={v => set('feedback_text', v)} value={form.feedback_text} />
          <Select label="Rating (1-5)" options={['1','2','3','4','5']} onChange={v => set('rating', v)} value={form.rating} />
        </Form>
      )}
    </div>
  )
}

function Form({ title, children, onSubmit }) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-4">
      <h3 className="font-medium text-gray-200">{title}</h3>
      {children}
      <button onClick={onSubmit} className="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded-lg text-sm font-medium transition">
        Submit
      </button>
    </div>
  )
}

function Input({ label, onChange, value, type = 'text' }) {
  return (
    <div>
      <label className="text-gray-400 text-xs mb-1 block">{label}</label>
      <input
        type={type}
        value={value || ''}
        onChange={e => onChange(e.target.value)}
        className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
      />
    </div>
  )
}

function Select({ label, options, onChange, value }) {
  return (
    <div>
      <label className="text-gray-400 text-xs mb-1 block">{label}</label>
      <select
        value={value || ''}
        onChange={e => onChange(e.target.value)}
        className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
      >
        <option value="">Select...</option>
        {options.map(o => <option key={o} value={o}>{o}</option>)}
      </select>
    </div>
  )
}