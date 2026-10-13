import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "cardvault.db"


def get_connection():
    """Connect to the CardVault SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    """Create the tables required for CardVault."""
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PokemonTypes (
                type_id INTEGER PRIMARY KEY,
                type_name TEXT NOT NULL UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cards (
                card_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type_id INTEGER NOT NULL,
                rarity TEXT NOT NULL
                    CHECK (rarity IN (
                        'Common', 'Uncommon', 'Rare',
                        'Ultra Rare', 'Secret Rare'
                    )),
                hp INTEGER NOT NULL CHECK (hp > 0),
                market_value REAL NOT NULL
                    CHECK (market_value >= 0),
                is_holo INTEGER NOT NULL DEFAULT 0
                    CHECK (is_holo IN (0, 1)),
                generation INTEGER NOT NULL
                    CHECK (generation > 0),
                FOREIGN KEY (type_id)
                    REFERENCES PokemonTypes(type_id)
            )
        """)

        connection.commit()
        print("CardVault tables created successfully.")

    finally:
        connection.close()


def add_sample_data():
    """Insert starter types and cards if the tables are empty."""
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM PokemonTypes")
        type_count = cursor.fetchone()[0]

        if type_count == 0:
            types = [
                (1, "Grass"),
                (2, "Fire"),
                (3, "Water"),
                (4, "Lightning"),
                (5, "Psychic"),
                (6, "Fighting"),
                (7, "Darkness"),
                (8, "Metal"),
                (9, "Fairy"),
                (10, "Dragon")
            ]

            cursor.executemany("""
                INSERT INTO PokemonTypes (type_id, type_name)
                VALUES (?, ?)
            """, types)

        cursor.execute("SELECT COUNT(*) FROM Cards")
        card_count = cursor.fetchone()[0]

        if card_count == 0:
            cards = [
                ("Pikachu", 4, "Common", 60, 1.50, 0, 1),
                ("Charizard", 2, "Rare", 120, 25.00, 1, 1),
                ("Bulbasaur", 1, "Common", 60, 1.00, 0, 1),
                ("Squirtle", 3, "Common", 50, 1.25, 0, 1),
                ("Mewtwo", 5, "Ultra Rare", 130, 35.00, 1, 1),
                ("Machop", 6, "Common", 60, 0.75, 0, 1),
                ("Umbreon", 7, "Rare", 100, 18.00, 1, 2),
                ("Magnemite", 8, "Common", 40, 0.50, 0, 1),
                ("Dragonite", 10, "Rare", 150, 22.00, 1, 1),
                ("Jigglypuff", 9, "Common", 60, 0.80, 0, 1),
                ("Raichu", 4, "Uncommon", 90, 4.00, 0, 1),
                ("Arcanine", 2, "Rare", 100, 8.50, 1, 1),
                ("Ivysaur", 1, "Uncommon", 80, 2.50, 0, 1),
                ("Wartortle", 3, "Uncommon", 70, 2.25, 0, 1),
                ("Gengar", 5, "Rare", 100, 12.00, 1, 1),
                ("Lucario", 6, "Rare", 110, 9.00, 1, 4),
                ("Absol", 7, "Rare", 80, 7.00, 0, 3),
                ("Metagross", 8, "Rare", 130, 10.00, 1, 3),
                ("Clefairy", 9, "Common", 50, 0.90, 0, 1),
                ("Garchomp", 10, "Rare", 140, 14.00, 1, 4),
                ("Eevee", 1, "Common", 50, 2.00, 0, 1),
                ("Vulpix", 2, "Common", 50, 0.70, 0, 1),
                ("Psyduck", 3, "Common", 60, 0.60, 0, 1),
                ("Voltorb", 4, "Common", 40, 0.65, 0, 1),
                ("Abra", 5, "Common", 30, 0.80, 0, 1),
                ("Geodude", 6, "Common", 70, 0.55, 0, 1),
                ("Murkrow", 7, "Uncommon", 60, 1.75, 0, 2),
                ("Scizor", 8, "Rare", 100, 6.50, 1, 2),
                ("Togepi", 9, "Common", 30, 1.10, 0, 2),
                ("Dratini", 10, "Common", 40, 1.50, 0, 1)
            ]

            cursor.executemany("""
                INSERT INTO Cards (
                    name, type_id, rarity, hp,
                    market_value, is_holo, generation
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, cards)

        connection.commit()

        cursor.execute("SELECT COUNT(*) FROM Cards")
        print("Cards in database:", cursor.fetchone()[0])

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()
    add_sample_data()
