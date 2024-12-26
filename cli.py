from classes import *

def main_menu():
    print("""
_____________________
Welcome to CLI-Study
_____________________
Type the number for the corresponding menu item to select it.

1. Create a new deck
2. Open an existing deck
3. Exit
------------------------
""")
    choice = input("Enter your choice: ").strip()
    return choice

def create_deck(dbmger):
    """
    Prompts the user to create a new deck by entering a name and description,
    then saves the deck using the provided database manager.

    Args:
        dbmger: The database manager instance used to save the new deck.

    Returns:
        None
    """
    print("\n--- Create a New Deck ---\n")
    name = input("Enter the name of the deck: ").strip()
    description = input("Enter a description for the deck: ").strip()
    new_deck = Deck(name=name, desc=description, cards=[])
    new_deck.save_deck(dbmger)
    print(f"\nDeck '{name}' created successfully!\n")

def open_deck(dbmger):
    """
    Opens an existing deck from the database and allows the user to manage it.

    This function retrieves the list of available decks from the database and
    prompts the user to select one. If no decks are found, it informs the user
    and returns to the main menu. Once a deck is selected, it loads the deck
    and calls the manage_deck function to allow further operations on the deck.

    Args:
        dbmger: An instance of the database manager that provides access to the
                database and its operations.

    Returns:
        None
    """
    print("\n--- Open an Existing Deck ---\n")
    dbmger.c.execute("SELECT name, description FROM Decks")
    decks = dbmger.c.fetchall()

    if not decks:
        print("No decks found. Please create one first.\n")
        return

    print("Available Decks:")
    for i, (name, description) in enumerate(decks, 1):
        print(f"{i}. {name} --> {description}")

    choice = input("\nEnter the number of the deck to open: ").strip()

    try:
        deck_index = int(choice) - 1
        deck_name = decks[deck_index][0]
    except (ValueError, IndexError):
        print("Invalid choice. Returning to the main menu.\n")
        return

    deck = Deck.load_deck(dbmger, deck_name)
    manage_deck(dbmger, deck)

def manage_deck(dbmger, deck):
    """
    Manages the specified deck by providing options to start a study session,
    add new cards, or return to the main menu.

    Parameters:
    dbmger (DatabaseManager): The database manager instance to handle database operations.
    deck (Deck): The deck object that is being managed.

    The function enters a loop where it displays a menu with the following options:
    1. Start a study session
    2. Add new cards
    3. Return to the main menu

    Based on the user's choice, it either starts a study session, adds new cards to the deck,
    or breaks the loop to return to the main menu. If an invalid choice is entered, it prompts
    the user to try again.
    """
    while True:
        print(f"\n--- Managing Deck: {deck.name} ---\n")
        print("1. Start a study session")
        print("2. Add new cards")
        print("3. Return to main menu\n")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            study_deck(deck)
        elif choice == "2":
            add_cards(dbmger, deck)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.\n")

def study_deck(deck):
    """
    Initiates a study session for the given deck of flashcards.

    Parameters:
    deck (Deck): The deck of flashcards to study. The deck should have a 'name' attribute and a list of 'cards'.
                 Each card should have 'front' and 'back' attributes.

    Returns:
    None

    The function prints the name of the deck and iterates through each card in the deck, displaying the front of the card
    and waiting for the user to press Enter before displaying the back of the card. If the deck is empty, it notifies the user
    to add some cards first.
    """
    print(f"\n--- Study Session: {deck.name} ---\n")
    if not deck.cards: # We check if the deck is empty or not
        print("No cards in this deck. Add some cards first!\n")
        return

    for card in deck.cards: # Iterate through each card in the deck
        print(f"Front: {card.front}")
        input("Press Enter to see the back...")
        print(f"Back: {card.back}\n")

    print("End of deck. Great job!\n")

def add_cards(dbmger, deck):
    """
    Adds new cards to the specified deck by prompting the user for input.

    Parameters:
    dbmger (DatabaseManager): The database manager instance to handle database operations.
    deck (Deck): The deck to which new cards will be added.

    The function will continuously prompt the user to enter the front and back of the card
    until the user types 'done' for the front of the card. Each new card is saved to the 
    database and appended to the deck's list of cards.

    Example:
        add_cards(dbmger, deck)
    """
    print(f"\n--- Add New Cards to Deck: {deck.name} ---\n")
    while True:
        front = input("Enter the front of the card (or type 'done' to finish): ").strip()
        if front.lower() == "done":
            break
        back = input("Enter the back of the card: ").strip()
        new_card = Card(deck=deck.name, front=front, back=back)
        new_card.save_card(dbmger, deck_id=deck.deck_id)
        deck.cards.append(new_card)
        print("Card added successfully!\n")

def main():
    dbmger = Database_Manager("cli_study")
    while True:
        choice = main_menu()
        if choice == "1":
            create_deck(dbmger)
        elif choice == "2":
            open_deck(dbmger)
        elif choice == "3":
            print("Exiting CLI-Study. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")
    dbmger.close()

if __name__ == "__main__":
    main()
