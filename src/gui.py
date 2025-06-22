import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.simulation import StockSimulator

class TradingApp(tk.Tk):
    def __init__(self, symbols):
        super().__init__()
        self.title("Multi-Stock Trading Simulator")
        self.geometry("1400x900")
        # data & state
        self.stocks = { s: StockSimulator(s, start_price=50 + 100*np.random.rand()) for s in symbols }
        self.selected = symbols[0]
        self.cash = 10000.0
        self.portfolio = { s:0 for s in symbols }
        # fonts & styles
        self.font_label = ("Segoe UI", 14)
        self.btn_cfg = {"font":("Segoe UI",14,"bold"), "width":8}
        # layout frames
        frm_chart = ttk.Frame(self)
        frm_chart.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        frm_ctrl  = ttk.Frame(self)
        frm_ctrl.pack(fill=tk.X, padx=10, pady=5)
        frm_status= ttk.Frame(self)
        frm_status.pack(fill=tk.X, side=tk.BOTTOM)
        # matplotlib canvas
        plt.rcParams.update({'font.size':12})
        self.fig, self.ax = plt.subplots(figsize=(12,7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frm_chart)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # controls
        ttk.Label(frm_ctrl, text="Stock:", font=self.font_label).pack(side=tk.LEFT)
        self.sym_var = tk.StringVar(value=self.selected)
        ttk.Combobox(frm_ctrl,textvariable=self.sym_var, values=symbols,
                     state="readonly", width=10, font=self.font_label).pack(side=tk.LEFT, padx=5)
        tk.Button(frm_ctrl, text="Switch", bg="#3498db", fg="white",
                  command=self.on_switch, **self.btn_cfg).pack(side=tk.LEFT, padx=(5,20))
        ttk.Label(frm_ctrl, text="Price:", font=self.font_label).pack(side=tk.LEFT)
        self.price_var = tk.StringVar(value="0.00")
        ttk.Label(frm_ctrl, textvariable=self.price_var,
                  font=self.font_label, width=10).pack(side=tk.LEFT, padx=(5,20))
        ttk.Label(frm_ctrl, text="Qty:", font=self.font_label).pack(side=tk.LEFT)
        self.qty_var = tk.IntVar(value=0)
        tk.Entry(frm_ctrl, textvariable=self.qty_var, font=self.font_label,
                 width=6).pack(side=tk.LEFT, padx=(5,20))
        tk.Button(frm_ctrl, text="Buy", bg="#2ecc71", fg="white",
                  command=self.on_buy, **self.btn_cfg).pack(side=tk.LEFT)
        tk.Button(frm_ctrl, text="Sell/Short", bg="#e74c3c", fg="white",
                  command=self.on_sell, **self.btn_cfg).pack(side=tk.LEFT, padx=(10,20))
        tk.Button(frm_ctrl, text="Next Day ▶", bg="#f39c12", fg="white",
                  command=self.on_next, **self.btn_cfg).pack(side=tk.LEFT)
        tk.Button(frm_ctrl, text="Exit", bg="#95a5a6", fg="white",
                  command=self.exit_app, **self.btn_cfg).pack(side=tk.RIGHT)
        # status bar
        self.status_var = tk.StringVar()
        ttk.Label(frm_status, textvariable=self.status_var,
                  font=self.font_label, relief=tk.SUNKEN).pack(fill=tk.X)
        # initial draw
        self.redraw()

    def on_switch(self):
        self.selected = self.sym_var.get()
        self.redraw()

    def on_next(self):
        self.stocks[self.selected].advance()
        self.redraw()

    def on_buy(self):
        qty = self.qty_var.get()
        price = self.stocks[self.selected].price()
        cost = price * qty
        if qty<=0 or cost>self.cash:
            messagebox.showerror("Error","Invalid qty or insufficient cash.")
            return
        self.cash -= cost
        self.portfolio[self.selected] += qty
        self.redraw()

    def on_sell(self):
        qty = self.qty_var.get()
        price = self.stocks[self.selected].price()
        if qty<=0:
            messagebox.showerror("Error","Quantity must be positive.")
            return
        self.cash += price*qty
        self.portfolio[self.selected] -= qty
        self.redraw()

    def redraw(self):
        price = self.stocks[self.selected].price()
        self.price_var.set(f"{price:.2f}")
        total = self.cash + sum(self.portfolio[s]*self.stocks[s].price() for s in self.stocks)
        holdings = []
        for s, q in self.portfolio.items():
            if q!=0:
                holdings.append(f"{s}:{q:+}")
        self.status_var.set(f"Cash: {self.cash:.2f}   Portfolio: {', '.join(holdings) or 'None'}   Net Worth: {total:.2f}")
        df = self.stocks[self.selected].view()
        self.ax.clear()
        mc = mpf.make_marketcolors(up='green', down='red', edge='inherit')
        style = mpf.make_mpf_style(marketcolors=mc)
        mpf.plot(df, type='candle', ax=self.ax, style=style, show_nontrading=False)
        self.ax.set_title(f"{self.selected} — Day {self.stocks[self.selected].current_day+1}", fontsize=16)
        self.canvas.draw()

    def exit_app(self):
        self.quit()
        self.destroy()