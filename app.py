from flask import Flask  
from flask import render_template, abort

app = Flask(__name__)

RECIPES = {
    "chocolate-chip-cookies": {
        "title": "Brown Butter Chocolate Chip Cookies",
        "category": "Cookies",
        "description": "Crispy edges, chewy centers, nutty brown butter.",
        "ingredients": [
            "200g unsalted butter (browned)",
            "220g brown sugar",
            "100g white sugar",
            "2 eggs",
            "300g plain flour",
            "1 tsp baking soda",
            "1/2 tsp salt",
            "200g dark choc chips"
        ],
        "steps": [
            "Brown the butter and cool.",
            "Cream sugars with butter, beat in eggs.",
            "Fold in dry ingredients and chips.",
            "Chill 30–60 min, scoop, bake 180°C ~10–12 min."
        ]
    },
    "snickerdoodles": {
        "title": "Snickerdoodles",
        "category": "Cookies",
        "description": "Tender cinnamon-sugar coated classics.",
        "ingredients": ["Flour", "Sugar", "Butter", "Eggs", "Cream of tartar", "Cinnamon"],
        "steps": ["Make dough", "Roll in cinnamon sugar", "Bake 180°C 9–11 min"]
    },
    
    "oatmeal-raisin": {
        "title": "Oatmeal Raisin Cookies",
        "category": "Cookies",
        "description": "Soft and cinnamon‑kissed with plump raisins.",
        "ingredients": ["Oats", "Flour", "Butter", "Sugar", "Eggs", "Raisins", "Cinnamon"],
        "steps": ["Cream butter and sugar", "Add eggs", "Fold in dry + oats + raisins", "Bake 175°C 10–12 min"]
    },
    "peanut-butter-cookies": {
        "title": "Peanut Butter Cookies",
        "category": "Cookies",
        "description": "Classic cross‑hatch, melt‑in‑mouth PB cookies.",
        "ingredients": ["Peanut butter", "Flour", "Sugar", "Egg", "Baking soda"],
        "steps": ["Mix", "Scoop and criss‑cross", "Bake 180°C 10–11 min"]
    }
}

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

@app.route('/my-recipes')
def my_recipes():
    return render_template('my_recipes.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recipes/<slug>')
def recipe_detail(slug: str):
    recipe = RECIPES.get(slug)
    if not recipe:
        abort(404)
    return render_template('recipe_detail.html', recipe=recipe)


if __name__ == '__main__':
    app.run(debug=True)
