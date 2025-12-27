-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User Memory Table
CREATE TABLE IF NOT EXISTS user_memory (
    user_id UUID PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    consent_given BOOLEAN NOT NULL DEFAULT FALSE,
    consent_date TIMESTAMP WITH TIME ZONE,
    
    -- Summary fields (NO raw text)
    -- Stores general relationship context (married, dating, long-distance, etc.)
    relationship_context JSONB DEFAULT '{}'::jsonb,
    
    -- Stores recurring themes identified over time (e.g., trust issues, financial stress)
    recurring_themes JSONB DEFAULT '{}'::jsonb,
    
    -- Stores patterns in emotional responses (e.g., anxious attachment signs)
    emotional_patterns JSONB DEFAULT '{}'::jsonb,
    
    -- Sliding window of recent progress notes (<200 chars each)
    progress_notes TEXT[] DEFAULT '{}',
    
    -- Metadata
    total_sessions INTEGER DEFAULT 0,
    last_session_date TIMESTAMP WITH TIME ZONE,
    highest_risk_level VARCHAR(20) DEFAULT 'LOW_RISK',
    
    CONSTRAINT check_progress_notes CHECK (
        array_length(progress_notes, 1) <= 10
    )
);

-- Audit Log Table for Safety & Privacy Compliance
CREATE TABLE IF NOT EXISTS memory_audit_log (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL, -- e.g., 'READ', 'UPDATE', 'DELETE', 'CONSENT_UPDATE'
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    details JSONB DEFAULT '{}'::jsonb,
    
    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
        REFERENCES user_memory(user_id)
        ON DELETE CASCADE
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_memory_audit_user_id ON memory_audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_user_memory_updated_at ON user_memory(updated_at);
