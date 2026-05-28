''''by michelle 11DTP'''
#SQLite自带了大小写转换，十分之方便
#return意为直接结束函数，避免连接失败后代码持续报错


# Import required modules
#import可以引用python自带功能库
import sqlite3
import os
import random

# Database file path
DB_PATH = "game.db"


# Menu option constants
#用于main
OP_VIEW_ALL = "1"
OP_FILTER_GENRE = "2"
OP_SORT_YEAR = "3"
OP_SORT_RATING = "4"
OP_FILTER_PLATFORM = "5"
OP_QUIZ_RECOMMEND = "6"
OP_EXIT = "0"

# Game genre corresponding letter selection
#用于Game Database System问题2
TYPE_DICT = {
    "A": "Action", 
    "B": "RPG",      
    "C": "FPS", 
    "D": "Simulation", 
    "E": "Adventure", 
    "F": "Strategy", 
    "G": "Racing", 
    "H": "Horror", 
    "I": "Party", 
    "J": "Sandbox", 
    "K": "UGC Platform" 
}

# Establish connection with SQLite database
#跟着ai新学的用来保证安全打开db的代码+连接数据库
def connect_db():
    # Check if database file exists
    #os是python的模块，检查DB_PATH路径下的文件是否存在，path为os的子模块，处理路径相关的操作
    #exists是os.path里的一个函数，如果这个路径在就true，不在就false
    if not os.path.exists(DB_PATH):
        print("❌ data not found!")
        return None
    # Create database connection
    conn = sqlite3.connect(DB_PATH)
    # Return data in dictionary form for easy field access
    conn.row_factory = sqlite3.Row
    return conn


# Format single game information output with aligned layout
#ljust用来打空格，为了对准每一列
def print_game_info(game):
    game_name = game["name"].ljust(35)[:35]
    game_platform = game["platform"].ljust(18)[:18]
    game_genre = game["genre"].ljust(15)[:15]
    #str转化字符为数字
    release_year = str(game["release_year"]).ljust(6)
    game_rating = f"{game['rating']}".ljust(5)
    print(f"| {game_name} | {game_platform} | {game_genre} | {release_year} | Score:{game_rating} |")


# Print formatted table header
#表头
def print_table_head():
    print("-" * 110)
    print(f"| Game Name".ljust(37) + "| Platform".ljust(20) + "| Genre".ljust(17) + "| Release Year | Rating |")
    print("-" * 110)


# Function 1: Query and display all games in database
def show_all_games():
    conn = connect_db()
    if not conn:
        return
    #cursor游标，执行sql指令用
    cursor = conn.cursor()
    # Query all data sorted by id
    cursor.execute("SELECT * FROM game ORDER BY id")
    #fetchall把所有查询结果一次性输出
    all_games_data = cursor.fetchall()
    print("\n📋 Full Game List")
    print_table_head()
    # Loop to print all game info
    for game_item in all_games_data:
        print_game_info(game_item)
    print("-" * 110)
    # Count total game quantity
    print(f"✅ Total: {len(all_games_data)} games")
    conn.close()


# Function 2: Filter games by selected genre via letters
def choose_type_filter():
    print("\n🎮 Select Game Genre")
    # Print all selectable genres and corresponding letters
    #键genre_key, 值genre_value，代表一个键A 一个值RPG，etc.
    for genre_key, genre_value in TYPE_DICT.items():
        print(f"【{genre_key}】{genre_value}")
    # Get user input letter
    selected_genre_letter = input("Enter letter: ").strip().upper()
    # Verify valid input
    if selected_genre_letter not in TYPE_DICT:
        print("⚠️ Invalid category!")
        return
    target_genre = TYPE_DICT[selected_genre_letter]
    conn = connect_db()
    cursor = conn.cursor()
    # Fuzzy match games of target genre
    #在sql里，LIKE？%{target}%用来模糊搜索，通配符
    cursor.execute("SELECT * FROM game WHERE genre LIKE ?", (f"%{target_genre}%",))
    filtered_genre_games = cursor.fetchall()
    print(f"\n📂 Genre: {target_genre}")
    print_table_head()
    # Check empty query result
    if not filtered_genre_games:
        print("| No games in this category".ljust(108) + "|")
    else:
        for game in filtered_genre_games:
            print_game_info(game)
    print("-" * 110)
    print(f"✅ Total: {len(filtered_genre_games)} games")
    conn.close()


# Function 3: Sort games by release year from oldest to newest
def sort_by_year_asc():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM game ORDER BY release_year ASC")
    sorted_year_games = cursor.fetchall()
    print("\n📅 Sort by Release Year (Oldest to Newest)")
    print_table_head()
    for game in sorted_year_games:
        print_game_info(game)
    print("-" * 110)
    conn.close()


# Function 4: Sort games by rating from highest to lowest
def sort_by_rating_desc():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM game ORDER BY rating DESC")
    sorted_rating_games = cursor.fetchall()
    print("\n⭐ Sort by Rating (Highest to Lowest)")
    print_table_head()
    for game in sorted_rating_games:
        print_game_info(game)
    print("-" * 110)
    conn.close()


# Function 5: Filter games by operating platform
def filter_platform():
    print("\n💻 Available: PC / Switch / PS5 / Xbox / Mobile")
    target_platform = input("Enter platform name: ").strip()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM game WHERE platform LIKE ?", (f"%{target_platform}%",))
    filtered_platform_games = cursor.fetchall()
    print(f"\n🔎 Platform: {target_platform}")
    print_table_head()
    if not filtered_platform_games:
        print("| No games found".ljust(108) + "|")
    else:
        for game in filtered_platform_games:
            print_game_info(game)
    print("-" * 110)
    print(f"✅ Total: {len(filtered_platform_games)} games")
    conn.close()


# New Added Function 6: Preference Quiz Game & Smart Game Recommendation
def game_preference_quiz():
    print("\n=====================================")
    print("🎮 Game Hobby Test & Recommendation")
    print("Answer simple questions, I will match suitable games for you!")
    print("=====================================")


    # Record user favorite genre tags
    user_favorite_genres = []
    # Question 1 constants
    Q1_COMBAT = "1"
    Q1_CASUAL = "2"
    Q1_STRATEGY = "3"
    Q1_STORY = "4"

    # Question 2 constants
    Q2_INTENSE = "1"
    Q2_PEACEFUL = "2"
    Q2_MYSTERIOUS = "3"

    # Question 3 constants
    Q3_SHORT = "1"
    Q3_LONG = "2"

    # Question 1: Favorite game style
    print("\nQ1. Which game style do you prefer most?")
    print("1. Exciting combat & action")
    print("2. Relaxing casual & creation")
    print("3. Brainy strategy & puzzle")
    print("4. Immersive story & adventure")
    question1_answer = input("Enter your choice number: ")
    if question1_answer == Q1_COMBAT:
        user_favorite_genres.extend(["Action","FPS","Horror"])
    elif question1_answer == Q1_CASUAL:
        user_favorite_genres.extend(["Simulation","Sandbox","UGC Platform"])
    elif question1_answer == Q1_STRATEGY:
        user_favorite_genres.extend(["Strategy","Racing"])
    elif question1_answer == Q1_STORY:
        user_favorite_genres.extend(["RPG","Adventure"])

    # Question 2: Preferred game atmosphere
    print("\nQ2. What game atmosphere do you like?")
    print("1. Intense and thrilling")
    print("2. Peaceful and comfortable")
    print("3. Mysterious and fantasy")
    question2_answer = input("Enter your choice number: ")
    if question2_answer == Q2_INTENSE:
        user_favorite_genres.append("FPS")
    elif question2_answer == Q2_PEACEFUL:
        user_favorite_genres.append("Simulation")
    elif question2_answer == Q2_MYSTERIOUS:
        user_favorite_genres.append("RPG")

    # Question 3: Preferred play time
    print("\nQ3. How long do you usually play games each time?")
    print("1. Short casual game within 1 hour")
    print("2. Long immersive game over 3 hours")
    question3_answer = input("Enter your choice number: ")
    if question3_answer == Q3_SHORT:
        user_favorite_genres.append("Party")
    elif question3_answer == Q3_LONG:
        user_favorite_genres.append("Adventure")
    

    # Remove duplicate preference tags
    user_favorite_genres = list(set(user_favorite_genres))
    print(f"\n✅ Your favorite game types: {', '.join(user_favorite_genres)}")
    print("🔍 Now matching suitable games for you...\n")

    # Connect database to query matching games
    conn = connect_db()
    cursor = conn.cursor()
    recommended_games_list = []
    # Match all user preferred genres
    for genre_tag in user_favorite_genres:
        #extend将多个元素加入一个列表
        cursor.execute("SELECT * FROM game WHERE genre LIKE ?",(f"%{genre_tag}%",))
        recommended_games_list.extend(cursor.fetchall())
    
    # Randomly pick up to 8 recommended games
    if recommended_games_list:
        #游戏随机排列random.shuffle
        random.shuffle(recommended_games_list)
        #[:8]类似于只提取前八
        final_recommended_games = recommended_games_list[:8]
        print_table_head()
        for game in final_recommended_games:
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
        print("1. View all games")                  # Check all games
        print("2. Filter by game genre")            # Filter by game type
        print("3. Sort by release year (ascending)")# Sort by release year
        print("4. Sort by rating (descending)")     # Sort by score
        print("5. Filter by platform")              # Filter by device platform
        print("6. Hobby Quiz & Game Recommend")     # New: Preference quiz + smart recommendation
        print("0. Exit program")                    # Exit program
        selected_option = input("Enter option number: ").strip()
        if selected_option == OP_VIEW_ALL:
            show_all_games()
        elif selected_option == OP_FILTER_GENRE:
            choose_type_filter()
        elif selected_option == OP_SORT_YEAR:
            sort_by_year_asc()
        elif selected_option == OP_SORT_RATING:
            sort_by_rating_desc()
        elif selected_option == OP_FILTER_PLATFORM:
            filter_platform()
        elif selected_option == OP_QUIZ_RECOMMEND:
            game_preference_quiz()
        elif selected_option == OP_EXIT:
            print("👋 Program exited, thanks for using.")
            break
        else:
            print("⚠️ Please enter a valid option!")

# Program entry execution
#用来启动整个程序
if __name__ == "__main__":
    main()