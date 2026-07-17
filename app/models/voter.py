import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Database

class Voter:
    def __init__(self):
        self.db = Database()
        self.db.connect()
    
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS voter (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            has_voted BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            deleted_at TIMESTAMP WITH TIME ZONE NULL
        )
        """
        return self.db.execute_query(query)
    
    def create(self, name, email):
        query = "INSERT INTO voter (name, email) VALUES (%s, %s) RETURNING id"
        if self.db.execute_query(query, (name, email)):
            result = self.db.fetch_one("SELECT lastval()")
            return result[0] if result else None
        return None
    
    def get_all(self):
        query = """
        SELECT id, name, email, has_voted, created_at 
        FROM voter 
        WHERE deleted_at IS NULL
        ORDER BY id
        """
        return self.db.fetch_all(query)
    
    def get_by_id(self, voter_id):
        query = """
        SELECT id, name, email, has_voted, created_at 
        FROM voter 
        WHERE id = %s AND deleted_at IS NULL
        """
        return self.db.fetch_one(query, (voter_id,))
    
    def get_by_email(self, email):
        query = """
        SELECT id, name, email, has_voted, created_at 
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
    
    def mark_as_voted(self, voter_id):
        query = "UPDATE voter SET has_voted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        return self.db.execute_query(query, (voter_id,))
    
    def update(self, voter_id, name, email):
        query = "UPDATE voter SET name = %s, email = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s AND deleted_at IS NULL"
        return self.db.execute_query(query, (name, email, voter_id))
    
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
    
    def close(self):
        self.db.disconnect()