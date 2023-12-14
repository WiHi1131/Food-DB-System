import psycopg2
import os

from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, flash, jsonify
app = Flask(__name__)
app.secret_key = os.getenv('food_lookup_key')

@app.route('/')
def foodlookup():
    return render_template('foodlookup.html')

@app.route('/get_food_suggestions')
def get_food_suggestions():
    search_term = request.args.get('term', '')  # Get the search term from the query parameter
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    query = "SELECT name FROM Foods WHERE name ILIKE %s LIMIT 10"
    cur.execute(query, (f'%{search_term}%',))
    suggestions = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(suggestions)

@app.route('/get_food_info')
def get_food_info():
    food_name = request.args.get('name', '')
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    query = "SELECT * FROM Foods WHERE name = %s"
    cur.execute(query, (food_name,))
    food_info = cur.fetchone()
    cur.close()
    conn.close()
    if food_info:
        
        info_dict = {
            "name": food_info[1],
            "portion_size (grams)": food_info[2],
            "calories (kcals)": food_info[3],
            "total_fat (g)": food_info[4],
            "saturated_fat (g)": food_info[5],
            "trans_fat (g)": food_info[6],
            "cholesterol (mg)": food_info[7],
            "sodium (mg)": food_info[8],
            "total_carbohydrates (g)": food_info[9],
            "dietary_fiber (g)": food_info[10],
            "sugars (g)": food_info[11],
            "protein (g)": food_info[12],
            "vitamin_d (µg)": food_info[13],
            "calcium (mg)": food_info[14],
            "iron (mg)": food_info[15],
            "potassium (mg)": food_info[16]
        }
        return jsonify(info_dict)
    else:
        return jsonify({"error": "Food not found"}), 404

@app.route('/add_food', methods=['GET', 'POST'])
def addfood():
    if request.method == 'POST':
        try:
            # Extract data from form
            food_name = request.form['foodName']
            print("Food Name:", food_name)
            portion_size = request.form['portion_size']
            calories = request.form['calories']
            total_fat = request.form['total_fat']
            saturated_fat = request.form['saturated_fat']
            trans_fat = request.form['trans_fat']
            cholesterol = request.form['cholesterol']
            sodium = request.form['sodium']
            total_carbohydrates = request.form['total_carbohydrates']
            dietary_fiber = request.form['dietary_fiber']
            sugars = request.form['sugars']
            protein = request.form['protein']
            vitamin_d = request.form['vitamin_d']
            calcium = request.form['calcium']
            iron = request.form['iron']
            potassium = request.form['potassium']

            # Validate data (server-side validation)
            if not food_name:
                raise ValueError("Must specify food name")
            if not food_name.replace(',', '').replace(' ', '').isalpha():
                raise ValueError("Invalid food name: Food name can only contain letters, spaces, and commas")
                
            # Convert empty strings to None and strings to appropriate types
            def convert_or_none(value):
                if value.strip() == '':
                    return None
                try:
                    float_value = float(value)
                    if float_value < 0:
                        return 'invalid'  # Reject negative numbers
                    return float_value
                except ValueError:
                    return 'invalid'

            # Validate other fields
            portion_size = convert_or_none(portion_size)
            if portion_size == 'invalid':
                raise ValueError("Portion size must be a positive real number or empty")
            calories = convert_or_none(calories)
            if calories == 'invalid':
                raise ValueError("Calories must be a positive real number or empty")    
            total_fat = convert_or_none(total_fat)
            if total_fat == 'invalid':
                raise ValueError("Total fat must be a positive real number or empty")    
            saturated_fat = convert_or_none(saturated_fat)
            if saturated_fat == 'invalid':
                raise ValueError("Saturated fat must be a positive real number or empty")
            trans_fat = convert_or_none(trans_fat)
            if trans_fat == 'invalid':
                raise ValueError("Trans fat must be a positive real number or empty")
            cholesterol = convert_or_none(cholesterol)
            if cholesterol == 'invalid':
                raise ValueError("Cholesterol must be a positive real number or empty")
            sodium = convert_or_none(sodium)
            if sodium == 'invalid':
                raise ValueError("Sodium must be a positive real number or empty")
            total_carbohydrates = convert_or_none(total_carbohydrates)
            if total_carbohydrates == 'invalid':
                raise ValueError("Total carbohydrates must be a positive real number or empty")
            dietary_fiber = convert_or_none(dietary_fiber)
            if dietary_fiber == 'invalid':
                raise ValueError("Dietary fiber must be a positive real number or empty")
            sugars = convert_or_none(sugars)
            if sugars == 'invalid':
                raise ValueError("Sugars must be a positive real number or empty")
            protein = convert_or_none(protein)
            if protein == 'invalid':
                raise ValueError("Protein must be a positive real number or empty")
            vitamin_d = convert_or_none(vitamin_d)
            if vitamin_d == 'invalid':
                raise ValueError("Vitamin_d must be a positive real number or empty")
            calcium = convert_or_none(calcium)
            if calcium == 'invalid':
                raise ValueError("Calcium must be a positive real number or empty")
            iron = convert_or_none(iron)
            if iron == 'invalid':
                raise ValueError("Iron must be a positive real number or empty")
            potassium = convert_or_none(potassium)
            if potassium == 'invalid':
                raise ValueError("Potassium must be a positive real number or empty")
            
            # Insert into database
            conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
            cur = conn.cursor()
            query = """
                INSERT INTO Foods (name, portion_size, calories, total_fat, saturated_fat, trans_fat, cholesterol, sodium, total_carbohydrates, dietary_fiber, sugars, protein, vitamin_d, calcium, iron, potassium) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (food_name, portion_size, calories, total_fat, saturated_fat, trans_fat, cholesterol, sodium, total_carbohydrates, dietary_fiber, sugars, protein, vitamin_d, calcium, iron, potassium))
            conn.commit()
            cur.close()
            conn.close()

            flash('Food item added successfully!')
            return redirect(url_for('addfood'))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('addfood'))

    return render_template('addfood.html')

@app.route('/db_test')
def testing():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    conn.close()
    return "Database Connection Successful!"

@app.route('/db_create')
def create():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    # Create Foods table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Foods (
        food_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        
        portion_size REAL,           -- Usually in grams (g)
        calories REAL,               -- Usually in kcal
        total_fat REAL,              -- Typically in grams (g)
        saturated_fat REAL,          -- Typically in grams (g)
        trans_fat REAL,              -- Typically in grams (g)
        cholesterol REAL,            -- Typically in milligrams (mg)
        sodium REAL,                 -- Typically in milligrams (mg)
        total_carbohydrates REAL,    -- Typically in grams (g)
        dietary_fiber REAL,          -- Typically in grams (g)
        sugars REAL,                 -- Typically in grams (g)
        protein REAL,                -- Typically in grams (g)
        vitamin_d REAL,              -- Usually in micrograms (µg) or IU
        calcium REAL,                -- Typically in milligrams (mg)
        iron REAL,                   -- Typically in milligrams (mg)
        potassium REAL               -- Typically in milligrams (mg)
        );
    ''')
    # Create Dishes table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Dishes (
        dish_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        description TEXT
        );
    ''')
    
    # Create foodsinDish table (junction table)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS foodsInDish (
        food_in_dish_id SERIAL PRIMARY KEY,
        dish_id INT,
        food_id INT,
        portion_multiplier REAL,  -- Multiplier for the portion size from Foods table
        FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id),
        FOREIGN KEY (food_id) REFERENCES Foods(food_id)
        );
    ''')
    
    # Create an Enum type for meal_type
    cur.execute('''
        DO $$ BEGIN
            CREATE TYPE meal_type AS ENUM ('breakfast', 'lunch', 'dinner', 'snack');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Meals (
        meal_id SERIAL PRIMARY KEY,
        meal_time TIMESTAMP NOT NULL,
        dish_id INT,                 -- Foreign key to reference the Dishes table
        type meal_type NOT NULL,       -- Enum type for meal type
        FOREIGN KEY (dish_id) REFERENCES Dishes(dish_id)
        );
    ''')
    
    # Create Users table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        user_id SERIAL PRIMARY KEY,
        username TEXT NOT NULL UNIQUE
        );
    ''')

    # Create Days table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Days (
        day_id SERIAL PRIMARY KEY,
        date DATE NOT NULL,
        user_id INT,
        meal_id INT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (meal_id) REFERENCES Meals(meal_id)
        );
    ''')
    
    conn.commit()
    conn.close()
    return "All Tables Successfully Created!"

@app.route('/db_insert')
def inserting():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    food_items = [('Avocado', 230, 384, 35, 4.9, None, None, 18, 20, 16, 0.7, 4.5, 0, 30, 1.4, 1166),
                  ('Onion, raw', 160, 64, 0.2, 0.1, None, None, 6.4, 15, 2.7, 6.8, 1.8, 0, 37, 0.3, 234),
                  ('Salami', 28, 119, 10, 3.7, None, 22, 529, 0.3, 0, 0.3, 6.1, None, 2.8, 0.4, 95), 
                  ('Spinach', 30, 23, 0.4, 0.1, 0, 0, 79, 3.6, 2.2, 0.4, 2.9, 0, 99, 2.7, 558),
                  ('Chicken Breast', 120, 165, 3.6, 1.0, 0, 85, 74, 0, 0, 0, 31, 0, 13, 1.2, 360),
                  ('Brown Rice', 195, 218, 1.6, 0.3, 0, 0, 10, 45, 3.5, 0.7, 5, 0, 19, 1.1, 84),
                  ('Eggs', 50, 78, 5.3, 1.6, 0.1, 186, 62, 0.6, 0, 0.6, 6.3, 1.2, 28, 0.9, 67),
                  ('Almonds', 30, 164, 14.2, 1.1, 0, 0, 0, 6.1, 3.5, 1.2, 6, 0, 76, 1.1, 206),
                  ('Tomato', 123, 22, 0.2, 0.0, 0, 0, 6, 4.8, 1.5, 3.2, 1.1, 0, 12, 0.3, 292),
                  ('Feta Cheese', 28, 75, 6, 4.2, 0, 25, 260, 1.2, 0, 1.2, 4, 0, 140, 0.2, 62),
                  ('Olive Oil', 15, 119, 13.5, 1.9, 0, 0, 0.3, 0, 0, 0, 0, 0, 0, 0.1, 0.1),
                  ('Quinoa', 185, 222, 3.6, 0.4, 0, 0, 13, 39, 5.2, 1.6, 8.1, 0, 31, 2.8, 318),
                  ('Banana', 118, 105, 0.4, 0.1, 0, 0, 1, 27, 3.1, 14.4, 1.3, 0, 6, 0.3, 422), 
                  ('Whole Milk', 240, 150, 8, 4.5, 0, 25, 105, 12, 0, 12, 8, 0.1, 280, 0.1, 320), 
                  ('Penne Pasta', 77, 280, 2, 0, 0, 0, 0, 55, 8, 1, 10, 0, 16, 1, 170)]
    cur.executemany('INSERT INTO Foods (name, portion_size, calories, total_fat, saturated_fat, trans_fat, cholesterol, sodium, total_carbohydrates, dietary_fiber, sugars, protein, vitamin_d, calcium, iron, potassium) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', food_items)
    # Inserting into Dishes table
    dishes = [
        ('Chicken Salad', 'Grilled chicken with spinach, tomatoes, and feta cheese'),
        ('Egg Fried Rice', 'Fried rice with eggs, onions, and olive oil'),
        ('Tomato Pasta', 'Pasta with fresh tomato sauce and olive oil'),
        ('Quinoa Salad', 'Quinoa with spinach, almonds, and avocado'),
        ('Banana Smoothie', 'Smoothie made with banana, spinach, and almond milk'),
        ('Chicken Quinoa Bowl', 'Bowl of quinoa with grilled chicken and vegetables')
    ]
    cur.executemany('INSERT INTO Dishes (name, description) VALUES (%s, %s)', dishes)
    
     # Inserting into foodsinDish table
    foods_in_dishes = [
        # For Chicken Salad (dish_id = 1): Chicken Breast, Spinach, Tomato, Feta Cheese
        (1, 5, 1.0),  # Chicken Breast
        (1, 4, 1.0),  # Spinach
        (1, 9, 0.5),  # Tomato
        (1, 10, 0.5), # Feta Cheese

        # For Egg Fried Rice (dish_id = 2): Eggs, Brown Rice, Onion
        (2, 7, 2.0),  # Eggs
        (2, 6, 1.0),  # Brown Rice
        (2, 2, 0.5),  # Onion
        (2, 11, 2), # Olive Oil

        # For Tomato Pasta (dish_id = 3): Tomato, Olive Oil
        (3, 9, 1.0),  # Tomato
        (3, 11, 0.3), # Olive Oil
        (3, 15, 1.5), # Penne Pasta

        # For Quinoa Salad (dish_id = 4): Quinoa, Spinach, Almonds, Avocado
        (4, 12, 1.0), # Quinoa
        (4, 4, 1.0),  # Spinach
        (4, 8, 0.5),  # Almonds
        (4, 1, 0.5),  # Avocado

        # For Banana Smoothie (dish_id = 5): Banana, Spinach, Almonds
        (5, 13, 1.0), # Banana
        (5, 4, 0.5),  # Spinach
        (5, 8, 0.3),  # Almonds
        (5, 14, 1), #Whole Milk

        # For Chicken Quinoa Bowl (dish_id = 6): Chicken Breast, Quinoa, Tomato
        (6, 5, 1.0),  # Chicken Breast
        (6, 12, 1.0), # Quinoa
        (6, 9, 0.5)   # Tomato
        # ... Add more as per your recipes
    ]
    cur.executemany('INSERT INTO foodsInDish (dish_id, food_id, portion_multiplier) VALUES (%s, %s, %s)', foods_in_dishes)
    
     # Inserting into Meals table
    meals = [
        ('2023-01-10 08:00:00', 1, 'breakfast'),
        ('2023-01-10 13:00:00', 2, 'lunch'),
        ('2023-01-10 18:00:00', 3, 'dinner'),
        ('2023-01-11 07:30:00', 4, 'breakfast'),
        ('2023-01-11 12:30:00', 5, 'lunch'),
        ('2023-01-11 19:00:00', 6, 'dinner')
    ]
    cur.executemany('INSERT INTO Meals (meal_time, dish_id, type) VALUES (%s, %s, %s)', meals)
     # Inserting into Users table
    users = [
        ('john_doe'),
        ('jane_smith'),
        ('alex_brown')
    ]
    cur.executemany('INSERT INTO Users (username) VALUES (%s)', users)
    
    # Inserting into Days table
    day_meals = [
        ('2023-01-10', 1, 1),
        ('2023-01-10', 1, 2),
        ('2023-01-10', 1, 3),
        ('2023-01-11', 2, 4),
        ('2023-01-11', 2, 5),
        ('2023-01-11', 2, 6)
    ]
    cur.executemany('INSERT INTO Days (date, user_id, meal_id) VALUES (%s, %s, %s)', day_meals)
    conn.commit()
    conn.close()
    return "All Tables Successfully Populated!"

@app.route('/db_select')
def selecting():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    
    # Function to format records into an HTML table
    def format_records_as_table(records, table_name):
        response_string = "<h2>{}</h2>".format(table_name)
        response_string += "<table border='1'>"
        for record in records:
            response_string += "<tr>"
            for info in record:
                response_string += "<td>{}</td>".format(info)
            response_string += "</tr>"
        response_string += "</table><br>"
        return response_string

    # Query and display data from Foods table
    cur.execute('SELECT * FROM Foods;')
    records = cur.fetchall()
    response_string = format_records_as_table(records, "Foods")

    # Query and display data from Dishes table
    cur.execute('SELECT * FROM Dishes;')
    records = cur.fetchall()
    response_string += format_records_as_table(records, "Dishes")

    # Query and display data from foodsInDish table
    cur.execute('SELECT * FROM foodsInDish;')
    records = cur.fetchall()
    response_string += format_records_as_table(records, "foodsinDish")

    # Query and display data from Meals table
    cur.execute('SELECT * FROM Meals;')
    records = cur.fetchall()
    response_string += format_records_as_table(records, "Meals")

    # Query and display data from Users table
    cur.execute('SELECT * FROM Users;')
    records = cur.fetchall()
    response_string += format_records_as_table(records, "Users")

    # Query and display data from Days table
    cur.execute('SELECT * FROM Days;')
    records = cur.fetchall()
    response_string += format_records_as_table(records, "Days")

    conn.close()
    return response_string

@app.route('/db_drop')
def dropping():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()

    # Drop tables in reverse order of creation due to foreign key constraints
    tables_to_drop = ['Days', 'Meals', 'foodsinDish', 'Dishes', 'Foods', 'Users']

    for table in tables_to_drop:
        cur.execute('DROP TABLE IF EXISTS {};'.format(table))

    # Drop the enum type meal_type as well
    cur.execute('DROP TYPE IF EXISTS meal_type;')

    conn.commit()
    conn.close()
    return "All Tables Successfully Dropped"