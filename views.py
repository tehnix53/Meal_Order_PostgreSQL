from flask import session, redirect, request, render_template

from app import app, db
from models import User, Order, Category, Meal
from forms import LoginForm, OrderForm
from Utility import day, month, shuffle, month_dict
from init_base import fill_category, fill_items

category = db.session.query(Category).all()
meals = db.session.query(Meal).all()

is_empty = db.session.query(Meal).all()

if len(is_empty) == 0:
    fill_category()
    fill_items()
    db.session.commit()
else:
    print('base_ok')


@app.route('/')
def index():
    # range of category numbers
    ids = db.session.query(Category).all()
    cat_range = [i.id for i in ids]
    # add three random id from each category:
    triple_meal = []
    for i in range(min(cat_range), max(cat_range) + 1):
        meal = db.session.query(Meal). \
            filter(Meal.category_id == i).all()
        for_shuffle = []
        for m in meal:
            for_shuffle += [m.id]
        key = shuffle(for_shuffle)
        random_meal = db.session.query(Meal). \
            filter(db.or_(Meal.id == key[0],
                          Meal.id == key[1],
                          Meal.id == key[2])).all()
        triple_meal += [random_meal]

    # variables to enable and disable some fields of page:
    mode = 'd-none'
    greeting = 'hidden'
    if session.get("user_id"):
        try:
            user_id = session.get('user_id')
            user = db.session.query(User).filter(User.id == user_id).first().mail
            if session.get('cart'):
                item_in_cart = session['cart']
                col_in_cart = []
                for i in item_in_cart:
                    col_in_cart += \
                        [db.session.query(Meal).
                             filter(Meal.title == i).first()]
            else:
                item_in_cart = []
                col_in_cart = []

            return render_template('main.html', category=category,
                                   triple_meal=triple_meal, mode_logon=mode,
                                   user=user, item_in_cart=item_in_cart,
                                   col_in_cart=col_in_cart)
        except AttributeError:
            return render_template('main.html', category=category,
                                   triple_meal=triple_meal, mode_logoff=mode,
                                   greeting=greeting, hidden_cart=greeting)

    return render_template('main.html', category=category,
                           triple_meal=triple_meal, mode_logoff=mode,
                           greeting=greeting, hidden_cart=greeting)


@app.route('/auth/', methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        if session.get('cart'):
            session.pop("cart")
        return redirect("/")
    form = LoginForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("auth.html", form=form,
                                   mode_logon='hidden',
                                   mode_logoff='hidden',
                                   hidden_cart='hidden')
        user = User.query.filter(User.mail == form.mail.data).first()
        if user and user.password_valid(form.password.data):
            session["user_id"] = user.id
            if session.get('cart'):
                session.pop("cart")
            return redirect("/")
        else:
            form.mail.errors.append("Не верное имя или пароль")
    mode = 'd-none'
    hidden_cart = 'hidden'
    return render_template("auth.html", form=form,
                           mode_logon=mode, mode_logoff=mode,
                           hidden_cart=hidden_cart)


@app.route('/logout/', methods=["POST", "GET"])
def logout():
    if session.get("user_id"):
        session.pop("user_id")
        return redirect("/auth/")
    else:
        return redirect('/')


@app.route('/addtocart/<item>/')
def add(item):
    if session.get("user_id"):
        cart = session.get("cart", [])
        cart.append(item)
        session['cart'] = cart
        return redirect('/cart')
    else:
        return redirect('/cart')


@app.route('/reset/<item>/')
def reset_cart(item):
    # удаляем корзину из сессии
    if session.get('cart'):
        cart = session.get('cart', [])
        cart.remove(item)
        session['cart'] = cart
    return redirect('/cart')


@app.route('/cart', methods=["GET", "POST"])
def cart():
    form = OrderForm()

    mode = 'd-none'
    cart_mode = 9
    form_visible = 'hidden'
    register_visible = 'hidden'
    drop_mode = 'hidden'
    if session.get("user_id"):
        id = session['user_id']
        cart_mode = 7
        if session.get('cart'):
            item_in_cart = session['cart']
            col_in_cart = []
            for i in item_in_cart:
                col_in_cart += \
                    [db.session.query(Meal).
                         filter(Meal.title == i).first()]

        else:
            item_in_cart = []
            col_in_cart = []

        return render_template('cart.html', id=id,
                               meals=meals,
                               col_in_cart=col_in_cart,
                               drop_mode=drop_mode,
                               item_in_cart=item_in_cart,
                               mode_logon=mode,
                               cart_mode=cart_mode,
                               register_visible=register_visible,
                               day=day, month=month,
                               month_dict=month_dict,
                               form=form
                               )

    return render_template('cart.html',
                           hide_header=form_visible,
                           day=day,
                           month=month,
                           month_dict=month_dict,
                           hidden_cart=register_visible,
                           mode_logoff=mode,
                           cart_mode=cart_mode,
                           form_visible=form_visible,
                           drop_mode='hidden',
                           unreg='hidden',
                           form=form)


@app.route('/ordered/', methods=["GET", "POST"])
def ordered():
    if request.method == "POST" and session.get('cart'):
        sum = request.form.get('sum')
        id = request.form.get('id')
        data = request.form.get('data')

        form = OrderForm()

        address = form.address.data
        phone = form.phone.data

        item_in_cart = session['cart']

        order = Order(data=data,
                      summa=sum,
                      phone=phone,
                      address=address)
        db.session.add(order)
        user = db.session.query(User).filter(User.id == id).first()
        order.user.append(user)
        for item in item_in_cart:
            meal = db.session.query(Meal).filter(Meal.title == item).first()
            order.meals.append(meal)
        db.session.commit()

        session.pop("cart")

        return render_template('ordered.html',
                               form=form,
                               item_in_cart=item_in_cart,
                               sum=sum,
                               address=address, phone=phone,
                               id=id, data=data,
                               hidden_cart='hidden',
                               mode_logon='d-none',
                               month_dict=month_dict,
                               day=day, month=month)
    else:
        return redirect('/')


@app.route('/register/', methods=["GET", "POST"])
def register():
    error_msg = ""  # Пока ошибок нет
    mode = 'd-none'
    if request.method == "POST":
        mail = request.form.get("mail")
        password = request.form.get("password")
        if not mail or not password:
            error_msg = "Не указано имя или пароль"
            return render_template("register.html",
                                   error_msg=error_msg, mode_logon='hidden',
                                   mode_logoff='hidden')

        user = User(mail=mail, password=password)
        db.session.add(user)
        db.session.commit()
        return render_template("register_success.html", mail=mail,
                               hidden_cart='hidden', mode_logon=mode,
                               mode_logoff=mode)

    return render_template("register.html", error_msg=error_msg,
                           hidden_cart='hidden', mode_logon=mode,
                           mode_logoff=mode)


@app.route('/account/')
def test():
    if session.get('user_id'):
        user_id = session.get('user_id')
        user = db.session.query(User).filter(User.id == user_id).first()
        all_orders = []
        for ord in user.order:
            all_orders += [ord]
        return render_template('account.html', hidden_cart='hidden',
                               mode_logon='d-none',
                               all_orders=all_orders)
    else:
        redirect('/')
