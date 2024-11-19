from PySide6.QtWidgets import QApplication
from zachet import RecipeManager

if __name__ == "__main__":
    app = QApplication([])
    window = RecipeManager()
    window.show()
    app.exec()