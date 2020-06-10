import pandas as pd

from models import db, Category, Meal


def fill_category():
    csv_category = 'delivery_categories.csv'

    frame = pd.read_csv(csv_category, index_col=0)

    for c in range(frame.shape[0]):
        series = frame.iloc[c]
        category = Category(title=series['title'])
        db.session.add(category)


def fill_items():
    csv_items = 'delivery_items.csv'

    meals = pd.read_csv(csv_items, index_col=0)

    for i in range(meals.shape[0]):
        series = meals.iloc[i]
        meal = Meal(title=series['title'],
                    price=int(series['price']),
                    picture=series['picture'],
                    description=series['description'],
                    category_id=int(series['category_id']))
        db.session.add(meal)
