# Initializing classes to store decks, cards, 
# and the front and back of each card
import sqlite3 as sql

# Database Manager class to handle database operations
class Database_Manager:
    def __init__(self, db_name: str):
        self.conn = sql.connect(db_name + '.db')
        self.c = self.conn.cursor()
        self.init_tables()
    # Initialize tables if they do not exist
    def init_tables(self):
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS Decks (
            deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
        """)
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS Flashcards (
            card_id INTEGER PRIMARY KEY AUTOINCREMENT,
            deck_id INTEGER NOT NULL,
            front TEXT NOT NULL,
            back TEXT NOT NULL,
            FOREIGN KEY (deck_id) REFERENCES Decks(deck_id) ON DELETE CASCADE
        )
        """)
        self.conn.commit()
    # Command to close the connection
    def close(self):
        self.conn.close()

# Deck class to store the name of the deck and the cards it contains
class Deck:
    def __init__(self, name: str, desc: str, cards: list, deck_id: int = None):
        self.name = name
        self.cards = cards
        self.desc = desc
        self.deck_id = deck_id
    
    def save_deck(self, dbmger: Database_Manager):
        dbmger.c.execute("INSERT INTO Decks (name, description) VALUES (?, ?)", (self.name, self.desc))
        dbmger.conn.commit()
        deck_id = dbmger.c.lastrowid
        self.deck_id = deck_id
        for card in self.cards:
            dbmger.c.execute("INSERT INTO Flashcards (deck_id, front, back) VALUES (?, ?, ?)", (deck_id, card.front, card.back))
        dbmger.conn.commit()
        
    @classmethod
    def load_deck(cls, dbmger: Database_Manager, deck_name: str):
        # Retrieve the deck from the database
        dbmger.c.execute("SELECT * FROM Decks WHERE name = ?", (deck_name,))
        deck_data = dbmger.c.fetchone()

        if deck_data is None:
            raise ValueError(f"No deck found with name: {deck_name}")
        
        deck_id, name, desc = deck_data
        # Retrieve associated cards
        dbmger.c.execute("SELECT front, back FROM Flashcards WHERE deck_id = ?", (deck_id,))
        cards_data = dbmger.c.fetchall()

        cards = [Card(deck=name, front=front, back=back) for front, back in cards_data]
        return cls(name=name, desc=desc, cards=cards, deck_id=deck_id)
    
    def __repr__(self):
        return f"Deck('{self.name}', {self.cards})"
    
    def __str__(self):
        return f"""
        Deck Name: {self.name}
        # Cards: {len(self.cards)}
        Description: {self.desc}
        """

# Card class to store the front and back of each card, and reference the deck it belongs to
class Card:
    def __init__(self, deck: str, front: str, back: str):
        self.front = front # Question
        self.back = back # Answer 
        self.deck = deck # Deck name
    
    @classmethod
    def str_to_card(cls, card_str: str):
        front, back = card_str.split(' _@flip_ ')
        return cls(deck=None, front=front, back=back)

    def save_card(self, dbmger: Database_Manager, deck_id: int):
        dbmger.c.execute("INSERT INTO Flashcards (deck_id, front, back) VALUES (?, ?, ?)", (deck_id, self.front, self.back))
        dbmger.conn.commit()
    
    def __repr__(self):
        return f"Card(front='{self.front}', back='{self.back}', deck='{self.deck}')"
    
    def __str__(self):
        return f"Card belongs to {self.deck}"
    
