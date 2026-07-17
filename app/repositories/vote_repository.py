from app.database import Database

class VoteRepository:
    def __init__(self):
        self.db = Database()
        self.db.connect()
    
    def create(self, voter_id, candidate_id):
        query = "INSERT INTO vote (voter_id, candidate_id) VALUES (%s, %s) RETURNING id"
        if self.db.execute_query(query, (voter_id, candidate_id)):
            result = self.db.fetch_one("SELECT lastval()")
            return result[0] if result else None
        return None
    
    def get_all(self):
        query = """
        SELECT 
            v.id,
            voter.name as voter_name,
            voter.email as voter_email,
            candidate.name as candidate_name,
            candidate.party,
            v.created_at
        FROM vote v
        JOIN voter ON v.voter_id = voter.id
        JOIN candidate ON v.candidate_id = candidate.id
        WHERE voter.deleted_at IS NULL AND candidate.deleted_at IS NULL
        ORDER BY v.created_at DESC
        """
        return self.db.fetch_all(query)
    
    def get_by_id(self, vote_id):
        query = """
        SELECT 
            v.id,
            voter.name as voter_name,
            voter.email as voter_email,
            candidate.name as candidate_name,
            candidate.party,
            v.created_at
        FROM vote v
        JOIN voter ON v.voter_id = voter.id
        JOIN candidate ON v.candidate_id = candidate.id
        WHERE v.id = %s AND voter.deleted_at IS NULL AND candidate.deleted_at IS NULL
        """
        return self.db.fetch_one(query, (vote_id,))
    
    def get_by_voter(self, voter_id):
        query = """
        SELECT 
            v.id,
            candidate.name as candidate_name,
            candidate.party,
            v.created_at
        FROM vote v
        JOIN candidate ON v.candidate_id = candidate.id
        WHERE v.voter_id = %s AND candidate.deleted_at IS NULL
        """
        return self.db.fetch_all(query, (voter_id,))
    
    def get_by_candidate(self, candidate_id):
        query = """
        SELECT 
            v.id,
            voter.name as voter_name,
            voter.email as voter_email,
            v.created_at
        FROM vote v
        JOIN voter ON v.voter_id = voter.id
        WHERE v.candidate_id = %s AND voter.deleted_at IS NULL
        """
        return self.db.fetch_all(query, (candidate_id,))
    
    def delete(self, vote_id):
        query = "DELETE FROM vote WHERE id = %s"
        return self.db.execute_query(query, (vote_id,))
    
    def count(self):
        query = "SELECT COUNT(*) FROM vote"
        result = self.db.fetch_one(query)
        return result[0] if result else 0
    
    def get_statistics(self):
        query = """
        WITH total_votes AS (
            SELECT COUNT(*) as total FROM vote
        ),
        candidate_votes AS (
            SELECT 
                c.id,
                c.name,
                c.party,
                COUNT(v.id) as votes_count
            FROM candidate c
            LEFT JOIN vote v ON v.candidate_id = c.id
            WHERE c.deleted_at IS NULL
            GROUP BY c.id, c.name, c.party
        )
        SELECT 
            cv.id as candidate_id,
            cv.name as candidate_name,
            cv.party,
            cv.votes_count,
            ROUND(CASE 
                WHEN tv.total = 0 THEN 0 
                ELSE (cv.votes_count::NUMERIC / tv.total::NUMERIC) * 100 
            END, 2) as percentage
        FROM candidate_votes cv
        CROSS JOIN total_votes tv
        ORDER BY cv.votes_count DESC
        """
        return self.db.fetch_all(query)
    
    def close(self):
        self.db.disconnect()