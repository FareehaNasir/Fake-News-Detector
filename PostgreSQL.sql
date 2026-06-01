-- Location: Supabase Database Migration Terminal SQL Console
CREATE TABLE verimedia_forensic_repository (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    content_payload_snippet TEXT NOT NULL,
    selected_bias_domain VARCHAR(80) NOT NULL,
    calculated_fraud_score INT4 NOT NULL,
    system_verdict_badge VARCHAR(30) DEFAULT 'SUSPICIOUS'
);