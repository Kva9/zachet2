from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ingredients(Base):
    __tablename__ = "ingredients"
    ingredients_id = Column(Integer, primary_key=True)
    names_ingredients = Column(String(50))

class Recipes(Base):
    __tablename__ = "recipes"
    recipes_id = Column(Integer, primary_key=True)
    nazvanie_recipes = Column(String(100))
    instrukciya = Column(String(100))
    nazvanie_ingred = Column(Integer, ForeignKey("ingredients.ingredients_id"))
    ingredients = relationship("Ingredients")

class Connect:
    @staticmethod
    def create_session():
        engine = create_engine("postgresql://postgres:1@localhost:5433/postgres")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session