-- MindPath Career Mentor — PostgreSQL Schema
-- Run: psql -U postgres -d mindpath_db -f schema.sql

-- Create database (run as superuser)
-- CREATE DATABASE mindpath_db;

-- Leads table
CREATE TABLE IF NOT EXISTS leads (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    phone       VARCHAR(20) NOT NULL,
    email       VARCHAR(255),
    city        VARCHAR(100),
    source      VARCHAR(50) DEFAULT 'direct',
    status      VARCHAR(50) DEFAULT 'new',
    notes       TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Assessments table
CREATE TABLE IF NOT EXISTS assessments (
    id              SERIAL PRIMARY KEY,
    student_name    VARCHAR(200) NOT NULL,
    age             INTEGER,
    class_year      VARCHAR(50),
    school          VARCHAR(300),
    city            VARCHAR(100),
    phone           VARCHAR(20) NOT NULL,
    email           VARCHAR(255),
    main_confusion  VARCHAR(200),
    goal            VARCHAR(200),
    status          VARCHAR(50) DEFAULT 'started',
    answers         JSONB,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Assessment Results table
CREATE TABLE IF NOT EXISTS assessment_results (
    id                      SERIAL PRIMARY KEY,
    assessment_id           INTEGER REFERENCES assessments(id) ON DELETE CASCADE,
    overall_score           FLOAT,
    aptitude_score          FLOAT,
    personality_score       FLOAT,
    eq_score                FLOAT,
    learning_style          VARCHAR(100),
    interest_score          FLOAT,
    career_fit_score        FLOAT,
    top_careers             JSONB,
    stream_recommendation   JSONB,
    strengths               JSONB,
    skill_gaps              JSONB,
    action_plan             JSONB,
    mentor_notes            TEXT,
    created_at              TIMESTAMPTZ DEFAULT NOW()
);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    phone           VARCHAR(20) NOT NULL,
    email           VARCHAR(255),
    concern         VARCHAR(300),
    session_type    VARCHAR(50) DEFAULT 'student',
    preferred_time  VARCHAR(100),
    notes           TEXT,
    status          VARCHAR(50) DEFAULT 'pending',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Testimonials table
CREATE TABLE IF NOT EXISTS testimonials (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    role        VARCHAR(200),
    text        TEXT NOT NULL,
    stars       INTEGER DEFAULT 5,
    emoji       VARCHAR(10),
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- FAQs table
CREATE TABLE IF NOT EXISTS faqs (
    id          SERIAL PRIMARY KEY,
    category    VARCHAR(100) NOT NULL,
    question    TEXT NOT NULL,
    answer      TEXT NOT NULL,
    order_index INTEGER DEFAULT 0,
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Career Options table
CREATE TABLE IF NOT EXISTS career_options (
    id                  SERIAL PRIMARY KEY,
    title               VARCHAR(200) NOT NULL,
    emoji               VARCHAR(10),
    description         TEXT,
    suitable_streams    JSONB,
    required_strengths  JSONB,
    aptitude_range      JSONB,
    personality_types   JSONB,
    interest_areas      JSONB,
    is_active           BOOLEAN DEFAULT TRUE
);

-- Pricing Plans table
CREATE TABLE IF NOT EXISTS pricing_plans (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    emoji           VARCHAR(10),
    price           VARCHAR(50) NOT NULL,
    original_price  VARCHAR(50),
    tagline         VARCHAR(300),
    description     TEXT,
    includes        JSONB,
    suitable_for    VARCHAR(300),
    is_highlighted  BOOLEAN DEFAULT FALSE,
    badge           VARCHAR(100),
    is_active       BOOLEAN DEFAULT TRUE,
    order_index     INTEGER DEFAULT 0
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_leads_phone ON leads(phone);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_assessments_phone ON assessments(phone);
CREATE INDEX IF NOT EXISTS idx_assessments_status ON assessments(status);
CREATE INDEX IF NOT EXISTS idx_bookings_phone ON bookings(phone);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON bookings(status);
