from flask import Flask  
from flask import render_template, abort
import json
import os

app = Flask(__name__)

RECIPES = {
    "chocolate-chip-cookies": {
        "title": "Brown Butter Chocolate Chip Cookies",
        "category": "Cookies",
        "description": "Crispy edges, chewy centers, nutty brown butter.",
        "tags": ["cookies", "chocolate"],
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
        "tags": ["cookies", "cinnamon"],
        "ingredients": ["Flour", "Sugar", "Butter", "Eggs", "Cream of tartar", "Cinnamon"],
        "steps": ["Make dough", "Roll in cinnamon sugar", "Bake 180°C 9–11 min"]
    },
    
    "oatmeal-raisin": {
        "title": "Oatmeal Raisin Cookies",
        "category": "Cookies",
        "description": "Soft and cinnamon‑kissed with plump raisins.",
        "tags": ["cookies", "oatmeal"],
        "ingredients": ["Oats", "Flour", "Butter", "Sugar", "Eggs", "Raisins", "Cinnamon"],
        "steps": ["Cream butter and sugar", "Add eggs", "Fold in dry + oats + raisins", "Bake 175°C 10–12 min"]
    },
    "peanut-butter-cookies": {
        "title": "Peanut Butter Cookies",
        "category": "Cookies",
        "description": "Classic cross‑hatch, melt‑in‑mouth PB cookies.",
        "tags": ["cookies", "peanut"],
        "ingredients": ["Peanut butter", "Flour", "Sugar", "Egg", "Baking soda"],
        "steps": ["Mix", "Scoop and criss‑cross", "Bake 180°C 10–11 min"]
    }
}

RECIPES_PATH = os.path.join(os.path.dirname(__file__), 'recipes.json')

def load_recipes():
    global RECIPES
    try:
        if os.path.exists(RECIPES_PATH):
            with open(RECIPES_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    RECIPES = data
    except Exception:
        # If loading fails, keep in-memory defaults
        pass

def save_recipes():
    try:
        with open(RECIPES_PATH, 'w', encoding='utf-8') as f:
            json.dump(RECIPES, f, ensure_ascii=False, indent=2)
    except Exception:
        # Ignore persistence errors in dev mode
        pass

# Load from disk if available
load_recipes()

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/recipes')
def recipes():
    # Pass recipes to the template for dynamic rendering
    return render_template('recipes.html', recipes=RECIPES)

@app.route('/my-recipes')
def my_recipes():
    my_recs = {slug: r for slug, r in RECIPES.items() if isinstance(r, dict) and r.get('favorite')}
    return render_template('my_recipes.html', recipes=my_recs)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recipes/<slug>')
def recipe_detail(slug: str):
    recipe = RECIPES.get(slug)
    if not recipe:
        abort(404)
    return render_template('recipe_detail.html', recipe=recipe, slug=slug)

# --- Toggle favorite ---
@app.route('/recipes/<slug>/favorite', methods=['POST'])
def toggle_favorite(slug: str):
    from flask import redirect, url_for, request
    recipe = RECIPES.get(slug)
    if not recipe:
        abort(404)
    # Toggle favorite flag
    recipe['favorite'] = not bool(recipe.get('favorite'))
    RECIPES[slug] = recipe
    save_recipes()
    # Redirect back to recipe detail or referer
    dest = request.headers.get('Referer')
    return redirect(dest or url_for('recipe_detail', slug=slug))

# --- Add new recipe ---
def slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    return text

@app.route('/recipes/new', methods=['GET', 'POST'])
def new_recipe():
    from flask import request, redirect, url_for
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        tags_raw = request.form.get('tags', '').strip()
        ingredients_raw = request.form.get('ingredients', '').strip()
        steps_raw = request.form.get('steps', '').strip()
        if not title:
            return render_template('new_recipe.html', error='Title is required')
        slug = slugify(title)
        if slug in RECIPES:
            return render_template('new_recipe.html', error='A recipe with that title already exists')
        recipe = {
            'title': title,
            'category': 'Cookies',
            'description': description or 'A cozy cookie recipe.',
            'tags': ['cookies'] + [t.strip().lower() for t in tags_raw.split(',') if t.strip()],
            'ingredients': [i.strip() for i in ingredients_raw.splitlines() if i.strip()],
            'steps': [s.strip() for s in steps_raw.splitlines() if s.strip()],
            'user_created': True,
            'favorite': False,
        }
        RECIPES[slug] = recipe
        save_recipes()
        return redirect(url_for('recipe_detail', slug=slug))
    return render_template('new_recipe.html')

# --- Delete recipe ---
@app.route('/recipes/<slug>/delete', methods=['POST'])
def delete_recipe(slug: str):
    from flask import redirect, url_for
    if slug in RECIPES:
        RECIPES.pop(slug)
        save_recipes()
    return redirect(url_for('recipes'))

# --- Edit recipe ---
@app.route('/recipes/<slug>/edit', methods=['GET', 'POST'])
def edit_recipe(slug: str):
    from flask import request, redirect, url_for
    recipe = RECIPES.get(slug)
    if not recipe:
        abort(404)
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        tags_raw = request.form.get('tags', '').strip()
        ingredients_raw = request.form.get('ingredients', '').strip()
        steps_raw = request.form.get('steps', '').strip()
        if not title:
            return render_template('edit_recipe.html', recipe=recipe, slug=slug, error='Title is required')
        new_slug = slugify(title)
        # If slug changes and collides
        if new_slug != slug and new_slug in RECIPES:
            return render_template('edit_recipe.html', recipe=recipe, slug=slug, error='A recipe with that title already exists')
        updated = {
            'title': title,
            'category': recipe.get('category') or 'Cookies',
            'description': description or 'A cozy cookie recipe.',
            'tags': ['cookies'] + [t.strip().lower() for t in tags_raw.split(',') if t.strip()],
            'ingredients': [i.strip() for i in ingredients_raw.splitlines() if i.strip()],
            'steps': [s.strip() for s in steps_raw.splitlines() if s.strip()],
            'user_created': bool(recipe.get('user_created')),
            'favorite': bool(recipe.get('favorite')),
        }
        # Move key if slug changed
        if new_slug != slug:
            RECIPES.pop(slug, None)
            RECIPES[new_slug] = updated
            save_recipes()
            return redirect(url_for('recipe_detail', slug=new_slug))
        else:
            RECIPES[slug] = updated
            save_recipes()
            return redirect(url_for('recipe_detail', slug=slug))
    # GET
    return render_template('edit_recipe.html', recipe=recipe, slug=slug)

@app.route('/health')
def health():
    return {'status': 'ok'}, 200

@app.errorhandler(403)
def handle_403(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def handle_404(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(405)
def handle_405(e):
    return render_template('errors/405.html'), 405


if __name__ == '__main__':
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', '5000'))
    app.run(host=host, port=port, debug=True)
