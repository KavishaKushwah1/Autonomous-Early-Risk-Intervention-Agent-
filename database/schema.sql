-- 1. Core Student Profile (Includes interest-based goals)
CREATE TABLE Students (
    student_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    grade_level INT NOT NULL,
    interest_goals TEXT,             -- For the interest-based learning module
    learning_streak_days INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. The "Observe" Layer: Academic Data
CREATE TABLE Academic_Records (
    record_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES Students(student_id),
    subject VARCHAR(50) NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    assessment_type VARCHAR(50),     -- e.g., 'Quiz', 'Final', 'Homework'
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. The "Observe" Layer: Non-Academic & Behavioral Data
CREATE TABLE Behavioral_Engagement (
    engagement_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES Students(student_id),
    activity_type VARCHAR(50),       -- e.g., 'Forum Post', 'Extracurricular'
    engagement_score INT,            -- 1-10 scale
    self_reflection_notes TEXT,      -- For reflection-based validation
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. The "Reason & Decide" Layer: Risk Signals
CREATE TABLE Risk_Signals (
    signal_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES Students(student_id),
    signal_type VARCHAR(50),         -- e.g., 'Engagement Drop', 'Score Drop'
    severity_level VARCHAR(20),      -- 'Low', 'Medium', 'High'
    agent_reasoning TEXT,            -- Why the AI flagged this
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. The "Act & Learn" Layer: Human-in-the-Loop Interventions
CREATE TABLE Interventions (
    intervention_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES Students(student_id),
    risk_signal_id INT REFERENCES Risk_Signals(signal_id),
    ai_recommended_action TEXT,      -- The supportive intervention
    teacher_feedback TEXT,           -- Teacher's edits/approval
    status VARCHAR(20) DEFAULT 'Pending Review', -- 'Pending Review', 'Approved', 'Rejected'
    actioned_at TIMESTAMP
);