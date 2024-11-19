import sys
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from sqlalchemy import func
from models import Connect, Recipes, Ingredients
from PySide6.QtWidgets import (
    QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QMainWindow, QApplication, QListWidget
)

class RecipeManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.session = Connect.create_session()
        self.setWindowTitle("Хранение рецептов")
        self.setWindowIcon(QIcon("F:/icon.png"))

        self.layout = QVBoxLayout()

        # Поля ввода
        self.recipe_name_input = QLineEdit(self)
        self.recipe_name_input.setPlaceholderText("Название рецепта")
        self.layout.addWidget(self.recipe_name_input)

        self.ingredient_id_input = QLineEdit(self)
        self.ingredient_id_input.setPlaceholderText("ID ингредиента")
        self.layout.addWidget(self.ingredient_id_input)

        self.instructions_input = QLineEdit(self)
        self.instructions_input.setPlaceholderText("Инструкция")
        self.layout.addWidget(self.instructions_input)

        # Кнопки
        self.add_button = QPushButton("Добавить рецепт", self)
        self.add_button.clicked.connect(self.add_recipe)
        self.layout.addWidget(self.add_button)

        self.update_button = QPushButton("Обновить рецепт", self)
        self.update_button.clicked.connect(self.update_recipe)
        self.layout.addWidget(self.update_button)

        self.search_button = QPushButton("Поиск ингредиента", self)
        self.search_button.clicked.connect(self.search_ingredient)
        self.layout.addWidget(self.search_button)

        # Список для отображения результатов поиска
        self.ingredient_list = QListWidget(self)
        self.layout.addWidget(self.ingredient_list)

        self.status_label = QLabel("", self)
        self.layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def add_recipe(self):
        nazvanie_recipes = self.recipe_name_input.text()
        nazvanie_ingred = self.ingredient_id_input.text()
        instrukciya = self.instructions_input.text()
        if nazvanie_recipes and nazvanie_ingred and instrukciya:
            self.session.add(Recipes(
                nazvanie_recipes=nazvanie_recipes,
                nazvanie_ingred=int(nazvanie_ingred),
                instrukciya=instrukciya
            ))
            self.session.commit()
            self.status_label.setText(f"Рецепт '{nazvanie_recipes}' успешно добавлен.")
        else:
            self.status_label.setText("Пожалуйста, заполните все поля.")

    def update_recipe(self):
        recipe_id = self.ingredient_id_input.text()
        nazvanie_recipes = self.recipe_name_input.text() or None
        instrukciya = self.instructions_input.text() or None
        if recipe_id:
            recipe = self.session.query(Recipes).filter(Recipes.recipes_id == int(recipe_id)).first()
            if recipe:
                if nazvanie_recipes is not None:
                    recipe.nazvanie_recipes = nazvanie_recipes
                if instrukciya is not None:
                    recipe.instrukciya = instrukciya
                
                self.session.commit()
                self.status_label.setText(f"Рецепт с ID {recipe_id} успешно обновлён.")
            else:
                self.status_label.setText(f"Рецепт с ID {recipe_id} не найден.")
        else:
            self.status_label.setText("Пожалуйста, введите ID рецепта.")

    def search_ingredient(self):
        ingredient_name = self.recipe_name_input.text()
        if ingredient_name:
            ingredients = self.session.query(Ingredients).filter(
                func.lower(Ingredients.names_ingredients).like(f"%{ingredient_name.lower()}%")
            ).all()
            self.ingredient_list.clear()
            if ingredients:
                for ingredient in ingredients:
                    self.ingredient_list.addItem(f"{ingredient.ingredients_id}: {ingredient.names_ingredients}")
            else:
                self.status_label.setText("Ингредиенты не найдены.")
        else:
            self.status_label.setText("Пожалуйста, введите название ингредиента для поиска.")

    def closeEvent(self, event):
        self.session.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecipeManager()
    window.show()
    sys.exit(app.exec())