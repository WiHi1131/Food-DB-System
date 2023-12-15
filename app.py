import psycopg2
import os
import json

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
    #Create index on name of Foods table
    cur.execute('''
        CREATE INDEX idx_foods_name ON Foods (name);
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
    
    # Create FoodUpdatesLog
    cur.execute('''
        CREATE TABLE IF NOT EXISTS FoodUpdatesLog (
        log_id SERIAL PRIMARY KEY,
        food_id INT,
        old_values JSONB,
        new_values JSONB,
        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (food_id) REFERENCES Foods(food_id)
    );
    ''')
    
    def create_triggers(cur):
        # Trigger function to prevent updates to the name in Foods
        cur.execute('''
            CREATE OR REPLACE FUNCTION prevent_name_update_foods()
            RETURNS TRIGGER AS $$
            BEGIN
                IF OLD.name IS DISTINCT FROM NEW.name THEN
                    RAISE EXCEPTION 'Updates to food name are not allowed.';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        ''')
        
        cur.execute('''
            CREATE TRIGGER prevent_name_update_foods_trigger
            BEFORE UPDATE OF name ON Foods
            FOR EACH ROW
            EXECUTE FUNCTION prevent_name_update_foods();
        ''')
        
        # Trigger function to prevent updates to the name in Dishes
        cur.execute('''
            CREATE OR REPLACE FUNCTION prevent_name_update_dishes()
            RETURNS TRIGGER AS $$
            BEGIN
                IF OLD.name IS DISTINCT FROM NEW.name THEN
                    RAISE EXCEPTION 'Updates to dish name are not allowed.';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        ''')
        
        cur.execute('''
            CREATE TRIGGER prevent_name_update_dishes_trigger
            BEFORE UPDATE OF name ON Dishes
            FOR EACH ROW
            EXECUTE FUNCTION prevent_name_update_dishes();
        ''')
        #Trigger function to log updates in Foods
        cur.execute('''
            CREATE OR REPLACE FUNCTION log_food_updates()
            RETURNS TRIGGER AS $$
            BEGIN
                INSERT INTO FoodUpdatesLog (food_id, old_values, new_values)
                VALUES (
                    OLD.food_id,
                    jsonb_build_object(
                        'portion_size', OLD.portion_size,
                        'calories', OLD.calories,
                        'total_fat', OLD.total_fat,
                        'saturated_fat', OLD.saturated_fat,
                        'trans_fat', OLD.trans_fat, 
                        'cholesterol', OLD.cholesterol,
                        'sodium', OLD.sodium, 
                        'total_carbohydrates', OLD.total_carbohydrates,
                        'dietary_fiber', OLD.dietary_fiber, 
                        'sugars', OLD.sugars,
                        'protein', OLD.protein, 
                        'vitamin_d', OLD.vitamin_d, 
                        'calcium', OLD.calcium,
                        'iron', OLD.iron,
                        'potassium', OLD.potassium
                    ),
                    jsonb_build_object(
                        'portion_size', NEW.portion_size,
                        'calories', NEW.calories,
                        'total_fat', NEW.total_fat,
                        'saturated_fat', NEW.saturated_fat,
                        'trans_fat', NEW.trans_fat, 
                        'cholesterol', NEW.cholesterol,
                        'sodium', NEW.sodium, 
                        'total_carbohydrates', NEW.total_carbohydrates,
                        'dietary_fiber', NEW.dietary_fiber, 
                        'sugars', NEW.sugars,
                        'protein', NEW.protein, 
                        'vitamin_d', NEW.vitamin_d, 
                        'calcium', NEW.calcium,
                        'iron', NEW.iron,
                        'potassium', NEW.potassium
                    )
                );
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        ''')
        #Trigger for logging updates
        cur.execute('''
            CREATE TRIGGER foods_update_log_trigger
            AFTER UPDATE OF calories, total_fat, sodium -- Add other fields as needed
            ON Foods
            FOR EACH ROW
            WHEN (OLD.* IS DISTINCT FROM NEW.*)
            EXECUTE FUNCTION log_food_updates();
        ''')
        # Trigger function for deleting dish in foodsInDish
        cur.execute('''
            CREATE OR REPLACE FUNCTION delete_dish()
            RETURNS TRIGGER AS $$
            BEGIN
                DELETE FROM foodsInDish WHERE dish_id = OLD.dish_id;
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;
        ''')

        # Trigger for deleting dish
        cur.execute('''
            CREATE TRIGGER delete_dish_trigger
            AFTER DELETE ON Dishes
            FOR EACH ROW
            EXECUTE FUNCTION delete_dish();
        ''')

        # Trigger function for deleting food in foodsInDish
        cur.execute('''
            CREATE OR REPLACE FUNCTION delete_food()
            RETURNS TRIGGER AS $$
            BEGIN
                DELETE FROM foodsInDish WHERE food_id = OLD.food_id;
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;
        ''')

        # Trigger for deleting food
        cur.execute('''
            CREATE TRIGGER delete_food_trigger
            AFTER DELETE ON Foods
            FOR EACH ROW
            EXECUTE FUNCTION delete_food();
        ''')
        
        # Delete meal when Dish is deleted
        cur.execute('''
            CREATE OR REPLACE FUNCTION delete_meal()
            RETURNS TRIGGER AS $$
            BEGIN
                DELETE FROM Meals WHERE dish_id = OLD.dish_id;
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;
        ''')
        cur.execute('''
            CREATE TRIGGER delete_meal_trigger
            AFTER DELETE ON Dishes
            FOR EACH ROW
            EXECUTE FUNCTION delete_meal();
        ''')

        # Triggers for Days table

        # Delete day when User is deleted
        cur.execute('''
            CREATE OR REPLACE FUNCTION delete_day_user()
            RETURNS TRIGGER AS $$
            BEGIN
                DELETE FROM Days WHERE user_id = OLD.user_id;
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;
        ''')
        cur.execute('''
            CREATE TRIGGER delete_day_user_trigger
            AFTER DELETE ON Users
            FOR EACH ROW
            EXECUTE FUNCTION delete_day_user();
        ''')

        # Delete day when Meal is deleted
        cur.execute('''
            CREATE OR REPLACE FUNCTION delete_day_meal()
            RETURNS TRIGGER AS $$
            BEGIN
                DELETE FROM Days WHERE meal_id = OLD.meal_id;
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;
        ''')
        cur.execute('''
            CREATE TRIGGER delete_day_meal_trigger
            AFTER DELETE ON Meals
            FOR EACH ROW
            EXECUTE FUNCTION delete_day_meal();
        ''')
    
    # Create triggers
    create_triggers(cur)
    
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
        ('Banana Smoothie', 'Smoothie made with banana, spinach, almonds, and whole milk'),
        ('Chicken Quinoa Bowl', 'Bowl of quinoa with grilled chicken and vegetables')
    ]
    cur.executemany('INSERT INTO Dishes (name, description) VALUES (%s, %s)', dishes)
    
    # Retrieve dish_ids by matching dish names
    cur.execute('SELECT dish_id, name FROM Dishes;')
    dish_ids = {name: dish_id for dish_id, name in cur.fetchall()}

    # Retrieve food_ids by matching food names
    cur.execute('SELECT food_id, name FROM Foods;')
    food_ids = {name: food_id for food_id, name in cur.fetchall()}

    # Define the composition of each dish
    dishes_composition = {
        'Chicken Salad': [('Chicken Breast', 1.0), ('Spinach', 1.0), ('Tomato', 0.5), ('Feta Cheese', 0.5)],
        'Egg Fried Rice': [('Eggs', 2.0), ('Brown Rice', 1.0), ('Onion, raw', 0.5), ('Olive Oil', 2)],
        'Tomato Pasta': [('Tomato', 1.0), ('Olive Oil', 0.3), ('Penne Pasta', 1.5)],
        'Quinoa Salad': [('Quinoa', 1.0), ('Spinach', 1.0), ('Almonds', 0.5), ('Avocado', 0.5)], 
        'Banana Smoothie': [('Banana', 1.0), ('Spinach', 0.5), ('Almonds', 0.3), ('Whole Milk', 1.0)], 
        'Chicken Quinoa Bowl': [('Chicken Breast', 1.0), ('Quinoa', 1.0), ('Tomato', 0.5)]
        
    }
    
    # Insert into foodsInDish
    for dish_name, ingredients in dishes_composition.items():
        for ingredient_name, portion_multiplier in ingredients:
            cur.execute(
                'INSERT INTO foodsInDish (dish_id, food_id, portion_multiplier) VALUES (%s, %s, %s)',
                (dish_ids[dish_name], food_ids[ingredient_name], portion_multiplier)
            )
            
    # Inserting into Users table
    users = [('john_doe'), ('jane_smith'), ('alex_brown')]
    cur.executemany('INSERT INTO Users (username) VALUES (%s)', [(user,) for user in users])

    # Retrieve user_ids by matching usernames
    cur.execute('SELECT user_id, username FROM Users;')
    user_ids = {username: user_id for user_id, username in cur.fetchall()}

    # Define meals with reference to dish names
    meal_data = [
        ('2023-01-10 08:00:00', 'Chicken Salad', 'breakfast'),
        ('2023-01-10 13:00:00', 'Egg Fried Rice', 'lunch'),
        ('2023-01-10 18:00:00', 'Tomato Pasta', 'dinner'),
        ('2023-01-11 07:30:00', 'Banana Smoothie', 'breakfast'),
        ('2023-01-11 12:30:00', 'Quinoa Salad', 'lunch'),
        ('2023-01-11 19:00:00', 'Chicken Quinoa Bowl', 'dinner')
    ]

    # Insert into Meals table with dynamic dish_id reference
    for meal_time, dish_name, meal_type in meal_data:
        cur.execute(
            'INSERT INTO Meals (meal_time, dish_id, type) VALUES (%s, %s, %s)',
            (meal_time, dish_ids[dish_name], meal_type)
        )

    # Retrieve meal_ids for the Days table
    cur.execute('SELECT meal_id, meal_time FROM Meals;')
    meal_ids = {str(meal_time): meal_id for meal_id, meal_time in cur.fetchall()}


    # Define day meals with reference to usernames and meal times
    day_meal_data = [
        ('2023-01-10', 'john_doe', '2023-01-10 08:00:00'),
        ('2023-01-10', 'john_doe', '2023-01-10 13:00:00'),
        ('2023-01-10', 'john_doe', '2023-01-10 18:00:00'), 
        ('2023-01-11', 'jane_smith', '2023-01-11 07:30:00'), 
        ('2023-01-11', 'jane_smith', '2023-01-11 12:30:00'), 
        ('2023-01-11', 'jane_smith', '2023-01-11 19:00:00')
    ]

    # Insert into Days table with dynamic user_id and meal_id references
    for date, username, meal_time in day_meal_data:
        if meal_time in meal_ids:
            meal_id = meal_ids[meal_time]
            cur.execute(
                'INSERT INTO Days (date, user_id, meal_id) VALUES (%s, %s, %s)',
                (date, user_ids[username], meal_id)
            )
        else:
            print(f"Meal time {meal_time} not found in meal_ids")

    conn.commit()
    conn.close()
    return "All Tables Successfully Populated!"

@app.route('/db_select')
def selecting():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    
    # Function to format records into an HTML table
    def format_records_as_table(records, table_name, column_names):
        response_string = "<h2>{}</h2>".format(table_name)
        response_string += "<table border='1'>"
        
        # Add column headers
        response_string += "<tr>"
        for col_name in column_names:
            response_string += "<th>{}</th>".format(col_name)
        response_string += "</tr>"
        
        # Add table data
        for record in records:
            response_string += "<tr>"
            for info in record:
                response_string += "<td>{}</td>".format(info)
            response_string += "</tr>"
        response_string += "</table><br>"
        return response_string

    def query_and_format_table(cur, table_name):
        cur.execute(f'SELECT * FROM {table_name};')
        records = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        return format_records_as_table(records, table_name, column_names)

    # Query and display data from each table
    response_string = ""
    for table in ["Foods", "Dishes", "foodsinDish", "Meals", "Users", "Days"]:
        response_string += query_and_format_table(cur, table)

    conn.close()
    return response_string

@app.route('/db_queries')
def db_queries():
    # Database connection
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()

    # Function to format records into an HTML table
    def format_records_as_table(records, table_name, column_names):
        response_string = f"<h2>{table_name}</h2>"
        response_string += "<table border='1'>"
        
        # Add column headers
        response_string += "<tr>"
        for col_name in column_names:
            response_string += f"<th>{col_name}</th>"
        response_string += "</tr>"
        
        # Add table data
        for record in records:
            response_string += "<tr>"
            for info in record:
                response_string += f"<td>{info}</td>"
            response_string += "</tr>"
        response_string += "</table><br>"
        return response_string

    # Query for foods with nonzero cholesterol
    cur.execute("SELECT * FROM Foods WHERE cholesterol > 0;")
    foods_records = cur.fetchall()
    foods_columns = [desc[0] for desc in cur.description]
    response_string = format_records_as_table(foods_records, "Foods with Nonzero Cholesterol", foods_columns)

    # Query for meals eaten before 13:00
    cur.execute("SELECT * FROM Meals WHERE EXTRACT(HOUR FROM meal_time) < 13;")
    meals_records = cur.fetchall()
    meals_columns = [desc[0] for desc in cur.description]
    response_string += format_records_as_table(meals_records, "Meals Eaten Before 13:00", meals_columns)

    # Query for days logged by user_id 1
    cur.execute("SELECT * FROM Days WHERE user_id = 1;")
    days_records = cur.fetchall()
    days_columns = [desc[0] for desc in cur.description]
    response_string += format_records_as_table(days_records, "Days Logged by User ID 1", days_columns)
    
    # Query: Count dishes for each type of meal
    cur.execute('''
        SELECT type, COUNT(*) AS total_dishes
        FROM Meals
        GROUP BY type;
    ''')
    meal_type_count = cur.fetchall()
    meal_type_count_columns = [desc[0] for desc in cur.description]
    response_string += format_records_as_table(meal_type_count, "Total Dishes for Each Meal Type (GROUP BY EXAMPLE)", meal_type_count_columns)

    # Close the database connection
    cur.close()
    conn.close()

    return response_string

@app.route('/db_joins')
def db_joins():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()

    # Function to format records into an HTML table
    def format_records_as_table(records, table_name, column_names):
        response_string = f"<h2>{table_name}</h2>"
        response_string += "<table border='1'>"
        
        # Add column headers
        response_string += "<tr>"
        for col_name in column_names:
            response_string += f"<th>{col_name}</th>"
        response_string += "</tr>"
        
        # Add table data
        for record in records:
            response_string += "<tr>"
            for info in record:
                response_string += f"<td>{info}</td>"
            response_string += "</tr>"
        response_string += "</table><br>"
        return response_string

    # Query 1: Dishes containing spinach
    cur.execute('''
        SELECT DISTINCT Dishes.name, Dishes.description
        FROM Dishes
        JOIN foodsInDish ON Dishes.dish_id = foodsInDish.dish_id
        JOIN Foods ON foodsInDish.food_id = Foods.food_id
        WHERE Foods.name = 'Spinach';
    ''')
    dishes_spinach = cur.fetchall()
    dishes_spinach_columns = [desc[0] for desc in cur.description]
    response_string = format_records_as_table(dishes_spinach, "Dishes Containing Spinach", dishes_spinach_columns)

    # Query 2: Calories in each dish
    cur.execute('''
        SELECT Dishes.name, SUM(Foods.calories * foodsInDish.portion_multiplier) AS total_calories
        FROM Dishes
        JOIN foodsInDish ON Dishes.dish_id = foodsInDish.dish_id
        JOIN Foods ON foodsInDish.food_id = Foods.food_id
        GROUP BY Dishes.name;
    ''')
    dish_calories = cur.fetchall()
    dish_calories_columns = [desc[0] for desc in cur.description]
    response_string += format_records_as_table(dish_calories, "Calories in Each Dish (GROUP BY EXAMPLE)", dish_calories_columns)

    # Query 3: Foods in lunch dishes
    cur.execute('''
        SELECT Foods.name
        FROM Meals
        JOIN Dishes ON Meals.dish_id = Dishes.dish_id
        JOIN foodsInDish ON Dishes.dish_id = foodsInDish.dish_id
        JOIN Foods ON foodsInDish.food_id = Foods.food_id
        WHERE Meals.type = 'lunch';
    ''')
    lunch_foods = cur.fetchall()
    lunch_foods_columns = [desc[0] for desc in cur.description]
    response_string += format_records_as_table(lunch_foods, "Foods in Lunch Dishes", lunch_foods_columns)
    
    # New Query: Display dishes by single ingredients
    cur.execute('''
        SELECT Foods.name AS Ingredient, Dishes.name AS Dish
        FROM Foods
        JOIN foodsInDish ON Foods.food_id = foodsInDish.food_id
        JOIN Dishes ON foodsInDish.dish_id = Dishes.dish_id
        ORDER BY Foods.name, Dishes.name;
    ''')
    dishes_by_ingredients = cur.fetchall()
    dishes_by_ingredients_columns = [desc[0] for desc in cur.description]
    response_string += format_records_as_table(dishes_by_ingredients, "Dishes Ordered By Ingredients", dishes_by_ingredients_columns)

    cur.close()
    conn.close()
    return response_string

@app.route('/db_updates')
def db_updates():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()

    def format_records_as_table(records, table_name, column_names):
        response_string = f"<h2>{table_name}</h2>"
        response_string += "<table border='1'>"
        for col_name in column_names:
            response_string += f"<th>{col_name}</th>"
        response_string += "</tr>"
        for record in records:
            response_string += "<tr>"
            for info in record:
                response_string += f"<td>{info}</td>"
            response_string += "</tr>"
        response_string += "</table><br>"
        return response_string

    response_string = ""

    # Attempt to update name in Foods table (should fail)
    try:
        cur.execute("UPDATE Foods SET name = 'Updated Name' WHERE food_id = 1;")
        conn.commit()
        response_string += "<p>Update to Foods name successful (unexpected).</p>"
    except psycopg2.Error as e:
        response_string += f"<p>Error updating Foods name: {e}</p>"
        conn.rollback()

    # Attempt to update name in Dishes table (should fail)
    try:
        cur.execute("UPDATE Dishes SET name = 'Updated Name' WHERE dish_id = 1;")
        conn.commit()
        response_string += "<p>Update to Dishes name successful (unexpected).</p>"
    except psycopg2.Error as e:
        response_string += f"<p>Error updating Dishes name: {e}</p>"
        conn.rollback()

    # Update nutritional values in Foods table and check log
    try:
        cur.execute("UPDATE Foods SET calories = 500 WHERE food_id = 1;")
        conn.commit()
        response_string += "<p>Nutritional values in Foods updated successfully.</p>"

        # Display FoodUpdatesLog
        cur.execute("SELECT * FROM FoodUpdatesLog;")
        log_records = cur.fetchall()
        log_columns = [desc[0] for desc in cur.description]
        response_string += format_records_as_table(log_records, "FoodUpdatesLog", log_columns)
    except psycopg2.Error as e:
        response_string += f"<p>Error updating Foods nutritional values: {e}</p>"
        conn.rollback()

    cur.close()
    conn.close()
    return response_string

@app.route('/db_deletes')
def db_deletes():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()

    # Function to format records into an HTML table
    def format_records_as_table(records, table_name, column_names):
        response_string = f"<h2>{table_name}</h2>"
        response_string += "<table border='1'>"
        
        # Add column headers
        response_string += "<tr>"
        for col_name in column_names:
            response_string += f"<th>{col_name}</th>"
        response_string += "</tr>"
        
        # Add table data
        for record in records:
            response_string += "<tr>"
            for info in record:
                response_string += f"<td>{info}</td>"
            response_string += "</tr>"
        response_string += "</table><br>"
        return response_string

    def query_and_format_table(cur, table_name):
        cur.execute(f'SELECT * FROM {table_name};')
        records = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        return format_records_as_table(records, table_name, column_names)

    response_string = ""

    # Delete the first item from each table and show which items were deleted
    tables_to_delete_from = ['Foods', 'Dishes', 'foodsinDish', 'Meals', 'Users', 'Days']
    for table in tables_to_delete_from:
        try:
            cur.execute(f'DELETE FROM {table} WHERE ctid IN (SELECT ctid FROM {table} LIMIT 1) RETURNING *;')
            deleted_records = cur.fetchall()
            if deleted_records:
                response_string += f"<p>Deleted from {table}: {deleted_records}</p>"
            else:
                response_string += f"<p>No record deleted from {table} (not found or already deleted).</p>"
        except psycopg2.Error as e:
            response_string += f"<p>Error deleting from {table}: {e}</p>"
            conn.rollback()

    # Query and display data from each table after deletion
    for table in ["Foods", "Dishes", "foodsinDish", "Meals", "Users", "Days"]:
        response_string += query_and_format_table(cur, table)

    conn.commit()
    cur.close()
    conn.close()
    return response_string

@app.route('/db_drop')
def dropping():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    
    # List of triggers to drop
    triggers_to_drop = [
        'prevent_name_update_foods_trigger', 'prevent_name_update_dishes_trigger', 
        'foods_update_log_trigger', 'delete_dish_trigger', 'delete_food_trigger', 
        'delete_meal_trigger', 'delete_day_user_trigger', 'delete_day_meal_trigger'
    ]

    # Drop triggers
    for trigger in triggers_to_drop:
        cur.execute(f'DROP TRIGGER IF EXISTS {trigger} ON public.Foods;')

    # Drop tables in reverse order of creation due to foreign key constraints
    tables_to_drop = ['FoodUpdatesLog', 'Days', 'Users', 'Meals', 'foodsinDish', 'Dishes', 'Foods']

    for table in tables_to_drop:
        cur.execute('DROP TABLE IF EXISTS {};'.format(table))

    # Drop the enum type meal_type as well
    cur.execute('DROP TYPE IF EXISTS meal_type;')

    conn.commit()
    conn.close()
    return "All Tables and Triggers Successfully Dropped"