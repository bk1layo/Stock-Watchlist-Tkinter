import tkinter as tk
from tkinter import messagebox as tkMB
import sqlite3
import yfinance as yf
import datetime

window = tk.Tk()
window.title('Watchlist')
window.geometry('200x175')

currentTD = datetime.datetime.now()
currentDate = datetime.date.today()

entry = tk.Entry(window)
entry.pack()

conn = sqlite3.connect("watchlist.db")
cursor = conn.cursor()

def realtimeClock():
    rawTD = datetime.datetime.now()
    nowTime = rawTD.strftime('%H:%M:%S %p')
    time.config(text = nowTime)
    window.after(1000, realtimeClock)

def get_input():
    tick = entry.get()
    print(tick)
    
    try:
        ticker = yf.Ticker(tick)
        info = ticker.history(period='1d')
        price = info['Close'][0]
        priceRound = round(price, 2)

    except Exception as e:
        tkMB.showerror("Error", f"Error fetching data: {e}")
        return
    
    cursor.execute("CREATE TABLE IF NOT EXISTS tickers(tick TEXT, price REAL)")
    cursor.execute("INSERT INTO tickers(tick, price) VALUES(?,?)", (tick, priceRound))
    
    conn.commit()

    tkMB.showinfo("Ticker Added", tick.upper() + " has been added to the watchlist.")

def updatePrice():
    price = cursor.execute("SELECT price FROM tickers")
    stock_price = cursor.fetchall()
    empt_ticks = " "    

    for i in stock_price:
        cursor.execute("SELECT price FROM tickers")
        price_catch = cursor.fetchall()
        empt_ticks += str(i)
        print(empt_ticks)

        """for j in i:
            updatedPrice = cursor.execute("")
            cursor.execute("UPDATE tickers SET price = %s WHERE price = %s", (updatedPrice ,price))"""
def see_list():
    cursor.execute("SELECT * FROM tickers")
    all_stocks = cursor.fetchall()
    empt_str = " "
    timeDate = "As of " 

    for i in all_stocks:
        empt_str += str(i[0]) + " " + str(i[1]) + "\n"
    tkMB.showinfo('Stock', timeDate + currentDate.strftime("%A, %b %d, %Y")+" "+time.cget("text") + "\n" + "\n" + empt_str.upper())

def clear_list():
    cursor.execute("DELETE FROM tickers")
    tkMB.showwarning("List Cleared", "The watchlist has been cleared.")
    conn.commit()

inputBut = tk.Button(window, text=('Enter Ticker'),command=(get_input))
seeListBut = tk.Button(window, text=('See Watchlist'), command=(see_list))
clearListBut = tk.Button(window, text="Clear Watchlist", command=clear_list)
time = tk.Label(window, text= currentTD.strftime('%H:%M:%S %p'))
date = tk.Label(window, text= currentDate.strftime("%A, %b %d, %Y"))

date.pack()
time.pack()
inputBut.pack()
seeListBut.pack()
clearListBut.pack()

updatePrice()
realtimeClock()
window.mainloop()