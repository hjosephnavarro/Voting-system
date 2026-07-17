from app.database import Database

class VoterRepository:
    def __init__(self):
        self.db = Database()
        self.db.connect()
    
    def create(self, name, email):
        query = "INSERT INTO voter (name, email) VALUES (%s, %s) RETURNING id"
        if self.db.execute_query(query, (name, email)):
            result = self.db.fetch_one("SELECT lastval()")
            return result[0] if result else None
        return None
    
    def get_all(self):
        query = """
        SELECT id, name, email, has_voted, created_at, updated_at
        FROM voter 
        WHERE deleted_at IS NULL
        ORDER BY id
        """
        return self.db.fetch_all(query)
    
    def get_by_id(self, voter_id):
        query = """
        SELECT id, name, email, has_voted, created_at, updated_at
        FROM voter 
        WHERE id = %s AND deleted_at IS NULL
        """
        return self.db.fetch_one(query, (voter_id,))
    
    def get_by_email(self, email):
        query = """
        SELECT id, name, email, has_voted, created_at, updated_at
        FROM voter 
        WHERE email = %s AND deleted_at IS NULL
        """
        return self.db.fetch_one(query, (email,))
    
    def get_available_voters(self):
        query = """
        SELECT id, name, email
        FROM voter 
        WHERE has_voted = FALSE AND deleted_at IS NULL
        ORDER BY id
        """
        return self.db.fetch_all(query)
    
    def update(self, voter_id, name, email):
        query = """
        UPDATE voter 
        SET name = %s, email = %s, updated_at = CURRENT_TIMESTAMP 
        WHERE id = %s AND deleted_at IS NULL
        """
        return self.db.execute_query(query, (name, email, voter_id))
    
    def mark_as_voted(self, voter_id):
        query = "UPDATE voter SET has_voted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        return self.db.execute_query(query, (voter_id,))
    
    def delete(self, voter_id):
        query = "UPDATE voter SET deleted_at = CURRENT_TIMESTAMP WHERE id = %s"
        return self.db.execute_query(query, (voter_id,))
    
    def count(self):
        query = "SELECT COUNT(*) FROM voter WHERE deleted_at IS NULL"
        result = self.db.fetch_one(query)
        return result[0] if result else 0
    
    def count_voted(self):
        query = "SELECT COUNT(*) FROM voter WHERE has_voted = TRUE AND deleted_at IS NULL"
        result = self.db.fetch_one(query)
        return result[0] if result else 0
    
    def exists_by_email(self, email):
        query = "SELECT COUNT(*) FROM voter WHERE email = %s AND deleted_at IS NULL"
        result = self.db.fetch_one(query, (email,))
        return result[0] > 0 if result else False
    
    def close(self):
        self.db.disconnect()