# Import required modules
import sqlite3
import os
import random

# Database file path
DB_PATH = "game.db"

# Game genre corresponding letter selection dictionary
TYPE_DICT = {
    "A": "Action",        # Action games
    "B": "RPG",           # Role-playing games
    "C": "FPS",           # First-person shooter games
    "D": "Simulation",    # Simulation games
    "E": "Adventure",     # Adventure games
    "F": "Strategy",      # Strategy games
    "G": "Racing",        # Racing games
    "H": "Horror",        # Horror games
    "I": "Party",         # Casual party games
    "J": "Sandbox",       # Sandbox games
    "K": "UGC Platform"   # UGC creation platform games (for Roblox)
}

# Establish connection with SQLite database
def connect_db():
    # Check if database file exists
    if not os.path.exists(DB_PATH):
        print("❌ data not found!")
        return None
    # Create database connection
    conn = sqlite3.connect(DB_PATH)
    # Return data in dictionary form for easy field access
    conn.row_factory = sqlite3.Row
    return conn

# Format single game information output with aligned layout
def print_game_info(game):
    name = game["name"].ljust(35)[:35]
    plat = game["platform"].ljust(18)[:18]
    genre = game["genre"].ljust(15)[:15]
    year = str(game["release_year"]).ljust(6)
    score = f"{game['rating']}".ljust(5)
    print(f"| {name} | {plat} | {genre} | {year} | Score:{score} |")

# Print formatted table header
def print_table_head():
    print("-" * 110)
    print(f"| Game Name".ljust(37) + "| Platform".ljust(20) + "| Genre".ljust(17) + "| Release Year | Rating |")
    print("-" * 110)

# Function 1: Query and display all games in database
def show_all_games():
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    # Query all data sorted by id
    cur.execute("SELECT * FROM game ORDER BY id")
    data = cur.fetchall()
    print("\n📋 Full Game List")
    print_table_head()
    # Loop to print all game info
    for item in data:
        print_game_info(item)
    print("-" * 110)
    # Count total game quantity
    print(f"✅ Total: {len(data)} games")
    conn.close()

# Function 2: Filter games by selected genre via letters
def choose_type_filter():
    print("\n🎮 Select Game Genre")
    # Print all selectable genres and corresponding letters
    for k, v in TYPE_DICT.items():
        print(f"【{k}】{v}")
    # Get user input letter
    sel = input("Enter letter: ").strip().upper()
    # Verify valid input
    if sel not in TYPE_DICT:
        print("⚠️ Invalid category!")
        return
    target = TYPE_DICT[sel]
    conn = connect_db()
    cur = conn.cursor()
    # Fuzzy match games of target genre
    cur.execute("SELECT * FROM game WHERE genre LIKE ?", (f"%{target}%",))
    res = cur.fetchall()
    print(f"\n📂 Genre: {target}")
    print_table_head()
    # Check empty query result
    if not res:
        print("| No games in this category".ljust(108) + "|")
    else:
        for g in res:
            print_game_info(g)
    print("-" * 110)
    print(f"✅ Total: {len(res)} games")
    conn.close()

# Function 3: Sort games by release year from oldest to newest
def sort_by_year_asc():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM game ORDER BY release_year ASC")
    data = cur.fetchall()
    print("\n📅 Sort by Release Year (Oldest to Newest)")
    print_table_head()
    for g in data:
        print_game_info(g)
    print("-" * 110)
    conn.close()

# Function 4: Sort games by rating from highest to lowest
def sort_by_rating_desc():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM game ORDER BY rating DESC")
    data = cur.fetchall()
    print("\n⭐ Sort by Rating (Highest to Lowest)")
    print_table_head()
    for g in data:
        print_game_info(g)
    print("-" * 110)
    conn.close()

# Function 5: Filter games by operating platform
def filter_platform():
    print("\n💻 Available: PC / Switch / PS5 / Xbox / Mobile")
    p = input("Enter platform name: ").strip()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM game WHERE platform LIKE ?", (f"%{p}%",))
    res = cur.fetchall()
    print(f"\n🔎 Platform: {p}")
    print_table_head()
    if not res:
        print("| No games found".ljust(108) + "|")
    else:
        for g in res:
            print_game_info(g)
    print("-" * 110)
    print(f"✅ Total: {len(res)} games")
    conn.close()

# New Added Function 6: Preference Quiz Game & Smart Game Recommendation
def game_preference_quiz():
    print("\n=====================================")
    print("🎮 Game Hobby Test & Recommendation")
    print("Answer simple questions, I will match suitable games for you!")
    print("=====================================")

    # Record user favorite genre tags
    user_like = []

    # Question 1: Favorite game style
    print("\nQ1. Which game style do you prefer most?")
    print("1. Exciting combat & action")
    print("2. Relaxing casual & creation")
    print("3. Brainy strategy & puzzle")
    print("4. Immersive story & adventure")
    ans1 = input("Enter your choice number: ")
    if ans1 == "1":
        user_like.extend(["Action","FPS","Horror"])
    elif ans1 == "2":
        user_like.extend(["Simulation","Sandbox","UGC Platform"])
    elif ans1 == "3":
        user_like.extend(["Strategy","Racing"])
    elif ans1 == "4":
        user_like.extend(["RPG","Adventure"])

    # Question 2: Preferred game atmosphere
    print("\nQ2. What game atmosphere do you like?")
    print("1. Intense and thrilling")
    print("2. Peaceful and comfortable")
    print("3. Mysterious and fantasy")
    ans2 = input("Enter your choice number: ")
    if ans2 == "1":
        user_like.append("FPS")
    elif ans2 == "2":
        user_like.append("Simulation")
    elif ans2 == "3":
        user_like.append("RPG")

    # Question 3: Preferred play time
    print("\nQ3. How long do you usually play games each time?")
    print("1. Short casual game within 1 hour")
    print("2. Long immersive game over 3 hours")
    ans3 = input("Enter your choice number: ")
    if ans3 == "1":
        user_like.append("Party")
    elif ans3 == "2":
        user_like.append("Adventure")

    # Remove duplicate preference tags
    user_like = list(set(user_like))
    print(f"\n✅ Your favorite game types: {', '.join(user_like)}")
    print("🔍 Now matching suitable games for you...\n")

    # Connect database to query matching games
    conn = connect_db()
    cur = conn.cursor()
    recommend_games = []
    # Match all user preferred genres
    for tag in user_like:
        cur.execute("SELECT * FROM game WHERE genre LIKE ?",(f"%{tag}%",))
        recommend_games.extend(cur.fetchall())
    
    # Randomly pick up to 8 recommended games
    if recommend_games:
        random.shuffle(recommend_games)
        final_rec = recommend_games[:8]
        print_table_head()
        for game in final_rec:
            print_game_info(game)
        print("-" * 110)
        print("🎊 These games are highly suitable for you!")
    else:
        print("😥 No matching games found, try other preferences next time!")
    conn.close()

# Main menu core logic
def main():
    while True:
        print("\n========== Game Database System ==========")
        print("1. View all games")                # Check all games
        print("2. Filter by game genre")           # Filter by game type
        print("3. Sort by release year (ascending)")# Sort by release year
        print("4. Sort by rating (descending)")     # Sort by score
        print("5. Filter by platform")             # Filter by device platform
        print("6. Hobby Quiz & Game Recommend")    # New: Preference quiz + smart recommendation
        print("0. Exit program")                   # Exit program
        op = input("Enter option number: ").strip()
        if op == "1":
            show_all_games()
        elif op == "2":
            choose_type_filter()
        elif op == "3":
            sort_by_year_asc()
        elif op == "4":
            sort_by_rating_desc()
        elif op == "5":
            filter_platform()
        elif op == "6":
            game_preference_quiz()
        elif op == "0":
            print("👋 Program exited.")
            break
        else:
            print("⚠️ Wrong input, please try again!")

# Program entry execution
if __name__ == "__main__":
    main()