-- Dadd-E Supabase Database Schema
-- Run this in your Supabase SQL editor to create the required tables

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    connected_apps TEXT[] DEFAULT '{}',
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Sessions table
CREATE TABLE IF NOT EXISTS sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    context JSONB DEFAULT '{}',
    last_intent TEXT,
    conversation_history JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Devices table
CREATE TABLE IF NOT EXISTS devices (
    device_id TEXT PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    device_type TEXT DEFAULT 'omi_glasses',
    is_connected BOOLEAN DEFAULT FALSE,
    battery_level INTEGER,
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Action history table
CREATE TABLE IF NOT EXISTS action_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    session_id UUID REFERENCES sessions(session_id) ON DELETE SET NULL,
    action_type TEXT NOT NULL,
    intent TEXT,
    parameters JSONB DEFAULT '{}',
    result TEXT,
    success BOOLEAN DEFAULT TRUE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Vision logs table
CREATE TABLE IF NOT EXISTS vision_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    prompt TEXT NOT NULL,
    description TEXT,
    model TEXT,
    objects TEXT[] DEFAULT '{}',
    text_detected TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transcription logs table (optional, for analytics)
CREATE TABLE IF NOT EXISTS transcription_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    session_id UUID REFERENCES sessions(session_id) ON DELETE SET NULL,
    text TEXT NOT NULL,
    confidence REAL,
    language TEXT DEFAULT 'en',
    wake_word_detected BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_updated_at ON sessions(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_devices_user_id ON devices(user_id);
CREATE INDEX IF NOT EXISTS idx_action_history_user_id ON action_history(user_id);
CREATE INDEX IF NOT EXISTS idx_action_history_timestamp ON action_history(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_vision_logs_user_id ON vision_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_vision_logs_timestamp ON vision_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_transcription_logs_user_id ON transcription_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_transcription_logs_timestamp ON transcription_logs(timestamp DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE devices ENABLE ROW LEVEL SECURITY;
ALTER TABLE action_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE vision_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE transcription_logs ENABLE ROW LEVEL SECURITY;

-- RLS Policies (users can only access their own data)
CREATE POLICY "Users can view own data"
    ON users FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can update own data"
    ON users FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can view own sessions"
    ON sessions FOR SELECT
    USING (user_id IN (SELECT user_id FROM users WHERE auth.uid() = user_id));

CREATE POLICY "Users can insert own sessions"
    ON sessions FOR INSERT
    WITH CHECK (user_id IN (SELECT user_id FROM users WHERE auth.uid() = user_id));

CREATE POLICY "Users can update own sessions"
    ON sessions FOR UPDATE
    USING (user_id IN (SELECT user_id FROM users WHERE auth.uid() = user_id));

-- Add similar policies for other tables
CREATE POLICY "Users can view own devices"
    ON devices FOR SELECT
    USING (user_id IN (SELECT user_id FROM users WHERE auth.uid() = user_id));

CREATE POLICY "Users can view own action history"
    ON action_history FOR SELECT
    USING (user_id IN (SELECT user_id FROM users WHERE auth.uid() = user_id));

CREATE POLICY "Users can insert own action history"
    ON action_history FOR INSERT
    WITH CHECK (user_id IN (SELECT user_id FROM users WHERE auth.uid() = user_id));

CREATE POLICY "Users can view own vision logs"
    ON vision_logs FOR SELECT
    USING (user_id IN (SELECT user_id FROM users WHERE auth.uid() = user_id));

CREATE POLICY "Users can insert own vision logs"
    ON vision_logs FOR INSERT
    WITH CHECK (user_id IN (SELECT user_id FROM users WHERE auth.uid() = user_id));

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sessions_updated_at
    BEFORE UPDATE ON sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
