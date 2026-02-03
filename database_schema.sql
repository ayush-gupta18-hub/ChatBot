-- Database Schema Reference
-- This file documents the current database structure for the Controlled Anonymity ChatBot.
-- It works with SQLite (via SQLAlchemy).

-- --------------------------------------------------------------------------------
-- Table: users
-- Purpose: Stores anonymous user identities and reputation data.
-- --------------------------------------------------------------------------------
CREATE TABLE users (
    -- Primary Key: Device Fingerprint (UUIDv4)
    device_id VARCHAR(64) NOT NULL PRIMARY KEY,
    
    -- Verification Data
    gender_result VARCHAR(10),       -- "Man" or "Woman", stored after one-time verification
    last_verified_at DATETIME,       -- Timestamp of last verification attempt
    
    -- Profile Data (Optional)
    nickname VARCHAR(50),            -- Public nickname
    bio VARCHAR(200),                -- Public bio
    
    -- Reputation System (Karma)
    karma_score INTEGER DEFAULT 100 NOT NULL,
    daily_matches_count INTEGER DEFAULT 0,
    daily_specific_filter_count INTEGER DEFAULT 0,
    
    -- Activity Tracking
    last_active_date DATETIME,       -- Used for daily login streaks
    last_queue_time DATETIME,        -- Used for queue cooldowns
    created_at DATETIME              -- Account creation time
);

-- Indexes for 'users'
CREATE INDEX ix_users_device_id ON users (device_id);


-- --------------------------------------------------------------------------------
-- Table: reports
-- Purpose: Tracks reports filed by users against others for abuse prevention.
-- --------------------------------------------------------------------------------
CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Foreign Keys (logical, not physically enforced in simple SQLite mode by default)
    reporter_device_id VARCHAR(64) NOT NULL,
    reported_device_id VARCHAR(64) NOT NULL,
    
    -- Report Details
    reason VARCHAR(500) NOT NULL,
    status VARCHAR(10) DEFAULT 'pending', -- Enum: pending, verified, rejected
    
    -- Timestamps
    created_at DATETIME,
    resolved_at DATETIME
);

-- Indexes for 'reports'
CREATE INDEX ix_reports_reporter_device_id ON reports (reporter_device_id);
CREATE INDEX ix_reports_reported_device_id ON reports (reported_device_id);
CREATE INDEX ix_reports_id ON reports (id);
