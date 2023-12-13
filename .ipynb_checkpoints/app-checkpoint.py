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
    conn.commit()
    conn.close()
    return "Foods Table Successfully Created!"

@app.route('/db_insert')
def inserting():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    food_items = [('Avocado', 230, 384, 35, 4.9, None, None, 18, 20, 16, 0.7, 4.5, 0, 30, 1.4, 1166),
                  ('Onion, raw', 160, 64, 0.2, 0.1, None, None, 6.4, 15, 2.7, 6.8, 1.8, 0, 37, 0.3, 234),
                  ('Salami', 28, 119, 10, 3.7, None, 22, 529, 0.3, 0, 0.3, 6.1, None, 2.8, 0.4, 95)]
    cur.executemany('INSERT INTO Foods (name, portion_size, calories, total_fat, saturated_fat, trans_fat, cholesterol, sodium, total_carbohydrates, dietary_fiber, sugars, protein, vitamin_d, calcium, iron, potassium) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', food_items)
    conn.commit()
    conn.close()
    return "Foods Table Successfully Populated!"

@app.route('/db_select')
def selecting():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    cur.execute('''
        SELECT * FROM Foods;
        ''')
    records = cur.fetchall()
    conn.close()
    response_string=""
    response_string+="<table>"
    for food in records:
        response_string+="<tr>"
        for info in food: 
            response_string+="<td>{}</td>".format(info)
        response_string+="</tr>"
    response_string+="</table>"
    return response_string
    
@app.route('/db_drop')
def dropping():
    conn = psycopg2.connect("postgres://food_db_msqq_user:96WkFN4LYyA6g0p8n9ykbw7GT0KQudsM@dpg-clok7g1oh6hc73bia110-a/food_db_msqq")
    cur = conn.cursor()
    cur.execute('''
        DROP TABLE Foods;
    ''')
    conn.commit()
    conn.close()
    return "Foods Table Successfully Dropped"