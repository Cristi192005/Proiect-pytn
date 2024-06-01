class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def to_dict(self):
        return {'name': self.name, 'ingredients': self.ingredients, 'instructions': self.instructions}

class RecipeBook:
    def __init__(self):
        self.recipes = []

    def load_recipes(self):
        with open('recipes.json', 'r') as f:
            recipes_data = json.load(f)
        for recipe_data in recipes_data:
            recipe = Recipe(recipe_data['name'], recipe_data['ingredients'], recipe_data['instructions'])
            self.recipes.append(recipe)

    def get_recipe(self, name):
        for recipe in self.recipes:
            if recipe.name == name:
                return recipe
        return None

class NutritionData:
    def __init__(self):
        self.macronutrients = {'calories': 0, 'protein': 0, 'fat': 0, 'carbohydrates': 0}

    def load_nutrition_data(self):
        with open('nutrition_data.json', 'r') as f:
            nutrition_data = json.load(f)
        for nutrient in nutrition_data:
            self.macronutrients[nutrient] = nutrition_data[nutrient]

    def calculate_nutrition(self, recipe):
        calories = 0
        protein = 0
        fat = 0
        carbohydrates = 0
        for ingredient in recipe.ingredients:
            ingredient_nutrition = nutrition_data.get(ingredient)
            if ingredient_nutrition:
                calories += ingredient_nutrition['calories']
                protein += ingredient_nutrition['protein']
                fat += ingredient_nutrition['fat']
                carbohydrates += ingredient_nutrition['carbohydrates']
        self.macronutrients['calories'] += calories
        self.macronutrients['protein'] += protein
        self.macronutrients['fat'] += fat
        self.macronutrients['carbohydrates'] += carbohydrates

class Planificator:
    def __init__(self, config):
        self.config = config
        self.recipe_book = RecipeBook()
        self.nutrition_data = NutritionData()

    def plan_recipe(self, recipe_name, servings):
        recipe = self.recipe_book.get_recipe(recipe_name)
        if recipe:
            self.nutrition_data.calculate_nutrition(recipe)
            print(f"Recipe planned: {recipe_name} x {servings}")
            print(f"Nutrition: {self.nutrition_data.macronutrients}")
        else:
            print(f"Recipe not found: {recipe_name}")

app = Flask(__name__)

@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes_list = [recipe.to_dict() for recipe in recipe_book.recipes]
    return jsonify(recipes_list)

@app.route('/recipes/<name>', methods=['GET'])
def get_recipe(name):
    recipe = recipe_book.get_recipe(name)
    if recipe:
        return jsonify(recipe.to_dict())
    return jsonify({'error': 'Recipe not found'}), 404

@app.route('/plan', methods=['POST'])
def plan_recipe():
    data = request.get_json()
    recipe_name = data['recipe_name']
    servings = data['servings']
    planner = Planificator(config)
    planner.plan_recipe(recipe_name, servings)
    return jsonify({'message': 'Recipe planned successfully'})

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    with open('recipes.json', 'r') as f:
        recipes_data = json.load(f)

    for recipe_data in recipes_data:
        recipe_book.recipes.append(Recipe(recipe_data['name'], recipe_data['ingredients'], recipe_data['instructions']))

    nutrition_data.load_nutrition_data()

    app.run(debug=True)

nutrition_data.load_nutrition_data()