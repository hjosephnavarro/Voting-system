CREATE TABLE IF NOT EXISTS voter (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    has_voted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE NULL
);

CREATE INDEX IF NOT EXISTS idx_voter_email ON voter(email);
CREATE INDEX IF NOT EXISTS idx_voter_name ON voter(name);
CREATE INDEX IF NOT EXISTS idx_voter_deleted_at ON voter(deleted_at) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_voter_has_voted ON voter(has_voted) WHERE has_voted = FALSE;

CREATE TABLE IF NOT EXISTS candidate (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    party VARCHAR(255) NULL,
    votes INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE NULL
);

CREATE INDEX IF NOT EXISTS idx_candidate_email ON candidate(email);
CREATE INDEX IF NOT EXISTS idx_candidate_name ON candidate(name);
CREATE INDEX IF NOT EXISTS idx_candidate_party ON candidate(party);
CREATE INDEX IF NOT EXISTS idx_candidate_deleted_at ON candidate(deleted_at) WHERE deleted_at IS NULL;

CREATE TABLE IF NOT EXISTS vote (
    id SERIAL PRIMARY KEY,
    voter_id INTEGER NOT NULL,
    candidate_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_voter_vote UNIQUE (voter_id),
    CONSTRAINT fk_vote_voter 
        FOREIGN KEY (voter_id) 
        REFERENCES voter(id) 
        ON DELETE RESTRICT,
    CONSTRAINT fk_vote_candidate 
        FOREIGN KEY (candidate_id) 
        REFERENCES candidate(id) 
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_vote_voter_id ON vote(voter_id);
CREATE INDEX IF NOT EXISTS idx_vote_candidate_id ON vote(candidate_id);
CREATE INDEX IF NOT EXISTS idx_vote_created_at ON vote(created_at);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_voter_updated_at ON voter;
CREATE TRIGGER update_voter_updated_at 
    BEFORE UPDATE ON voter 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_candidate_updated_at ON candidate;
CREATE TRIGGER update_candidate_updated_at 
    BEFORE UPDATE ON candidate 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE FUNCTION update_vote_counters()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE candidate 
    SET votes = votes + 1 
    WHERE id = NEW.candidate_id;
    
    UPDATE voter 
    SET has_voted = TRUE 
    WHERE id = NEW.voter_id;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_vote_counters_trigger ON vote;
CREATE TRIGGER update_vote_counters_trigger
    AFTER INSERT ON vote
    FOR EACH ROW
    EXECUTE FUNCTION update_vote_counters();

CREATE OR REPLACE FUNCTION check_not_both_voter_and_candidate()
RETURNS TRIGGER AS $$
DECLARE
    v_count INTEGER;
    c_count INTEGER;
BEGIN
    IF TG_TABLE_NAME = 'voter' THEN
        SELECT COUNT(*) INTO c_count FROM candidate WHERE email = NEW.email;
        IF c_count > 0 THEN
            RAISE EXCEPTION 'Esta persona ya está registrada como candidato';
        END IF;
    ELSIF TG_TABLE_NAME = 'candidate' THEN
        SELECT COUNT(*) INTO v_count FROM voter WHERE email = NEW.email;
        IF v_count > 0 THEN
            RAISE EXCEPTION 'Esta persona ya está registrada como votante';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS prevent_voter_candidate_duplicate_voter ON voter;
CREATE TRIGGER prevent_voter_candidate_duplicate_voter
    BEFORE INSERT OR UPDATE ON voter
    FOR EACH ROW
    EXECUTE FUNCTION check_not_both_voter_and_candidate();

DROP TRIGGER IF EXISTS prevent_voter_candidate_duplicate_candidate ON candidate;
CREATE TRIGGER prevent_voter_candidate_duplicate_candidate
    BEFORE INSERT OR UPDATE ON candidate
    FOR EACH ROW
    EXECUTE FUNCTION check_not_both_voter_and_candidate();

CREATE OR REPLACE VIEW active_voters AS
SELECT 
    id,
    name,
    email,
    has_voted,
    created_at,
    updated_at
FROM voter
WHERE deleted_at IS NULL;

CREATE OR REPLACE VIEW active_candidates AS
SELECT 
    id,
    name,
    email,
    party,
    votes,
    created_at,
    updated_at
FROM candidate
WHERE deleted_at IS NULL;

CREATE OR REPLACE VIEW vote_statistics AS
WITH total_votes AS (
    SELECT COUNT(*)::INTEGER AS total 
    FROM vote
),
total_voters AS (
    SELECT COUNT(*)::INTEGER AS total 
    FROM voter v
    WHERE v.has_voted = TRUE 
      AND v.deleted_at IS NULL
),
candidate_votes AS (
    SELECT 
        c.id AS candidate_id,
        c.name AS candidate_name,
        c.party,
        COUNT(v.id)::INTEGER AS vote_count
    FROM candidate c
    LEFT JOIN vote v ON v.candidate_id = c.id
    WHERE c.deleted_at IS NULL
    GROUP BY c.id, c.name, c.party
)
SELECT 
    cv.candidate_id,
    cv.candidate_name,
    cv.party,
    cv.vote_count,
    ROUND(
        CASE 
            WHEN tv.total = 0 THEN 0 
            ELSE (cv.vote_count::NUMERIC / tv.total::NUMERIC) * 100 
        END, 
        2
    ) AS percentage,
    tv.total AS total_votes,
    tvv.total AS total_voters_voted
FROM candidate_votes cv
CROSS JOIN total_votes tv
CROSS JOIN total_voters tvv
ORDER BY cv.vote_count DESC;

CREATE OR REPLACE VIEW all_votes_with_details AS
SELECT 
    v.id AS vote_id,
    v.created_at AS voted_at,
    voter.name AS voter_name,
    voter.email AS voter_email,
    candidate.name AS candidate_name,
    candidate.email AS candidate_email,
    candidate.party AS candidate_party
FROM vote v
JOIN voter ON v.voter_id = voter.id
JOIN candidate ON v.candidate_id = candidate.id
WHERE voter.deleted_at IS NULL 
  AND candidate.deleted_at IS NULL;

INSERT INTO voter (name, email) VALUES 
    ('Juan Perez', 'juan.perez@email.com'),
    ('Maria Garcia', 'maria.garcia@email.com')
ON CONFLICT (email) DO NOTHING;

INSERT INTO candidate (name, email, party) VALUES 
    ('Carlos Lopez', 'carlos.lopez@email.com', 'Partido Azul'),
    ('Ana Martinez', 'ana.martinez@email.com', 'Partido Rojo')
ON CONFLICT (email) DO NOTHING;

INSERT INTO vote (voter_id, candidate_id) 
SELECT 
    (SELECT id FROM voter WHERE email = 'juan.perez@email.com'),
    (SELECT id FROM candidate WHERE email = 'carlos.lopez@email.com');

INSERT INTO vote (voter_id, candidate_id) 
SELECT 
    (SELECT id FROM voter WHERE email = 'maria.garcia@email.com'),
    (SELECT id FROM candidate WHERE email = 'ana.martinez@email.com');

SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY table_name;

SELECT table_name 
FROM information_schema.views 
WHERE table_schema = 'public'
ORDER BY table_name;

SELECT 'Votantes' as tipo, id::text, name, email, has_voted::text as detalle FROM active_voters
UNION ALL
SELECT 'Candidatos' as tipo, id::text, name, email, party as detalle FROM active_candidates;

SELECT * FROM vote_statistics;

SELECT * FROM voter;

SELECT * FROM candidate;

SELECT * FROM vote;

SELECT 'Votantes' as tipo, id::text, name, email, has_voted::text as detalle 
FROM active_voters;

SELECT 'Candidatos' as tipo, id::text, name, email, party as detalle 
FROM active_candidates;

SELECT * FROM vote_statistics;

SELECT * FROM voter;

SELECT * FROM candidate;

SELECT * FROM vote;