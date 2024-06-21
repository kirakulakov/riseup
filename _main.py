import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token="7163464524:AAECjS-rvkkK-rib4rG2MRkK8VFdLTBmpTM")
dp = Dispatcher()

# Database setup
conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users
(id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, is_authenticated INTEGER DEFAULT 0)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products
(id INTEGER PRIMARY KEY, name TEXT, description TEXT, price REAL)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS cart
(user_id INTEGER, product_id INTEGER, quantity INTEGER,
FOREIGN KEY (user_id) REFERENCES users(id),
FOREIGN KEY (product_id) REFERENCES products(id))
''')

conn.commit()

# Add some sample products
sample_products = [
    ("Laptop", "High-performance laptop", 999.99),
    ("Smartphone", "Latest model smartphone", 699.99),
    ("Headphones", "Noise-cancelling headphones", 199.99),
    ("Smartwatch", "Fitness tracking smartwatch", 249.99),
]

cursor.executemany("INSERT OR IGNORE INTO products (name, description, price) VALUES (?, ?, ?)", sample_products)
conn.commit()


# States
class AuthStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()


class ShopStates(StatesGroup):
    browsing = State()
    cart = State()
    checkout = State()


# Helper functions
def get_user(username):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()


def authenticate_user(username, password):
    user = get_user(username)
    if user and user[2] == password:
        cursor.execute("UPDATE users SET is_authenticated = 1 WHERE username = ?", (username,))
        conn.commit()
        return True
    return False


def get_products():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()


def get_cart(user_id):
    cursor.execute('''
    SELECT products.name, cart.quantity, products.price
    FROM cart
    JOIN products ON cart.product_id = products.id
    WHERE cart.user_id = ?
    ''', (user_id,))
    return cursor.fetchall()


def add_to_cart(user_id, product_id, quantity):
    cursor.execute("INSERT OR REPLACE INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
                   (user_id, product_id, quantity))
    conn.commit()


def clear_cart(user_id):
    cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()


# Command handlers
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Welcome to the Online Shop Bot! Please log in or register.")
    await message.answer("Enter your username:")
    await state.set_state(AuthStates.waiting_for_username)


@dp.message(AuthStates.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text
    await state.update_data(username=username)
    await message.answer("Enter your password:")
    await state.set_state(AuthStates.waiting_for_password)


@dp.message(AuthStates.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    password = message.text
    user_data = await state.get_data()
    username = user_data['username']

    if authenticate_user(username, password):
        await message.answer(f"Welcome back, {username}! 🎉")
        await show_main_menu(message)
        await state.set_state(ShopStates.browsing)
    else:
        user = get_user(username)
        if user:
            await message.answer("Incorrect password. Please try again.")
            await state.set_state(AuthStates.waiting_for_password)
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            await message.answer(f"New account created for {username}. Welcome! 🎉")
            await show_main_menu(message)
            await state.set_state(ShopStates.browsing)


async def show_main_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Browse Products 🛍️", callback_data="browse")],
        [InlineKeyboardButton(text="View Cart 🛒", callback_data="cart")],
        [InlineKeyboardButton(text="Checkout 💳", callback_data="checkout")]
    ])
    await message.answer("What would you like to do?", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "browse")
async def process_browse(callback_query: types.CallbackQuery):
    products = get_products()
    builder = InlineKeyboardBuilder()
    for product in products:
        builder.button(text=f"{product[1]} - ${product[3]:.2f}", callback_data=f"product_{product[0]}")
    builder.adjust(2)
    await callback_query.message.answer("Here are our products:", reply_markup=builder.as_markup())
    await callback_query.answer()


@dp.callback_query(lambda c: c.data.startswith("product_"))
async def process_product(callback_query: types.CallbackQuery, state: FSMContext):
    product_id = int(callback_query.data.split("_")[1])
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Add to Cart", callback_data=f"add_{product_id}")],
        [InlineKeyboardButton(text="Back to Products", callback_data="browse")]
    ])

    await callback_query.message.answer(
        f"{product[1]}\n\n{product[2]}\n\nPrice: ${product[3]:.2f}",
        reply_markup=keyboard
    )
    await callback_query.answer()


@dp.callback_query(lambda c: c.data.startswith("add_"))
async def process_add_to_cart(callback_query: types.CallbackQuery, state: FSMContext):
    product_id = int(callback_query.data.split("_")[1])
    user_id = callback_query.from_user.id
    add_to_cart(user_id, product_id, 1)
    await callback_query.answer("Product added to cart!")
    await process_browse(callback_query)


@dp.callback_query(lambda c: c.data == "cart")
async def process_cart(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    cart_items = get_cart(user_id)

    if not cart_items:
        await callback_query.message.answer("Your cart is empty.")
    else:
        total = sum(item[1] * item[2] for item in cart_items)
        cart_text = "Your Cart:\n\n"
        for item in cart_items:
            cart_text += f"{item[0]} - Quantity: {item[1]} - ${item[2]:.2f}\n"
        cart_text += f"\nTotal: ${total:.2f}"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Checkout 💳", callback_data="checkout")],
            [InlineKeyboardButton(text="Clear Cart 🗑️", callback_data="clear_cart")],
            [InlineKeyboardButton(text="Back to Products 🛍️", callback_data="browse")]
        ])

        await callback_query.message.answer(cart_text, reply_markup=keyboard)

    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "clear_cart")
async def process_clear_cart(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    clear_cart(user_id)
    await callback_query.answer("Cart cleared!")
    await process_cart(callback_query)


@dp.callback_query(lambda c: c.data == "checkout")
async def process_checkout(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    cart_items = get_cart(user_id)

    if not cart_items:
        await callback_query.message.answer("Your cart is empty. Nothing to checkout.")
    else:
        total = sum(item[1] * item[2] for item in cart_items)
        await callback_query.message.answer(f"Total amount: ${total:.2f}\n\nThank you for your purchase! 🎉")
        clear_cart(user_id)

    await callback_query.answer()
    await show_main_menu(callback_query.message)


# Error handler
@dp.error()
async def error_handler(update: types.Update, exception: Exception):
    logging.exception(f"Exception occurred: {exception}")
    await update.message.answer("An error occurred. Please try again later.")


# Main function to start the bot
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())