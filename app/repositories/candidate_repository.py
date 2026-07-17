from app.database import Database

class CandidateRepository:
    def __init__(self):
        self.db = Database()
        self.db.connect()
    
    def create(self, name, email, party=None):
        query = "INSERT INTO candidate (name, email, party) VALUES (%s, %s, %s) RETURNING id"
        if self.db.execute_query(query, (name, email, party)):
            result = self.db.fetch_one("SELECT lastval()")
            return result[0] if result else None
        return None
    
    def get_all(self):
        query = """
        SELECT id, name, email, party, votes, created_at, updated_at
        FROM candidate 
        WHERE deleted_at IS NULL
        ORDER BY votes DESC, id
        """
        return self.db.fetch_all(query)
    
    def get_by_id(self, candidate_id):
        query = """
        SELECT id, name, email, party, votes, created_at, updated_at
        FROM candidate 
        WHERE id = %s AND deleted_at IS NULL
        """
        return self.db.fetch_one(query, (candidate_id,))
    
    def get_by_email(self, email):
        query = """
        SELECT id, name, email, party, votes, created_at, updated_at
        FROM candidate 
        WHERE email = %s AND deleted_at IS NULL
        """
        return self.db.fetch_one(query, (email,))
    
    def update(self, candidate_id, name=None, email=None, party=None):
        updates = []
        params = []
        if name is not None:
            updates.append("name = %s")
            params.append(name)
        if email is not None:
            updates.append("email = %s")
            params.append(email)
        if party is not None:
            updates.append("party = %s")
            params.append(party)
        
        if not updates:
            return False
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(candidate_id)
        
        query = f"UPDATE candidate SET {', '.join(updates)} WHERE id = %s AND deleted_at IS NULL"
        return self.db.execute_query(query, tuple(params))
    
    def increment_votes(self, candidate_id):
        query = "UPDATE candidate SET votes = votes + 1, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        return self.db.execute_query(query, (candidate_id,))
    
    def delete(self, candidate_id):
        query = "UPDATE candidate SET deleted_at = CURRENT_TIMESTAMP WHERE id = %s"
        return self.db.execute_query(query, (candidate_id,))
    
    def count(self):
        query = "SELECT COUNT(*) FROM candidate WHERE deleted_at IS NULL"
        result = self.db.fetch_one(query)
        return result[0] if result else 0
    
    def exists_by_email(self, email):
        query = "SELECT COUNT(*) FROM candidate WHERE email = %s AND deleted_at IS NULL"
        result = self.db.fetch_one(query, (email,))
        return result[0] > 0 if result else False
    
    def close(self):
        self.db.disconnect()