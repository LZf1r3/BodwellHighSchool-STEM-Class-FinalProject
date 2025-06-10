import random
import tkinter as tk
from tkinter import messagebox

class Stock:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def update_price(self, emotion):
        if emotion == "pânico":
            change = random.uniform(-0.2, -0.05)
        elif emotion == "ganância":
            change = random.uniform(0.05, 0.2)
        elif emotion == "estabilidade":
            change = random.uniform(-0.03, 0.03)
        else:
            change = random.uniform(-0.05, 0.05)
        self.price *= (1 + change)
        if self.price < 1:
            self.price = 1

    def __str__(self):
        return f"{self.name}: ${self.price:.2f}"

class Investor:
    def __init__(self, cash):
        self.cash = cash
        self.portfolio = {}

    def buy(self, stock, amount):
        cost = stock.price * amount
        if cost > self.cash:
            return False, "Dinheiro insuficiente."
        self.cash -= cost
        self.portfolio[stock.name] = self.portfolio.get(stock.name, 0) + amount
        return True, f"Comprou {amount} ações de {stock.name} por ${cost:.2f}."

    def sell(self, stock, amount):
        if self.portfolio.get(stock.name, 0) < amount:
            return False, "Você não tem ações suficientes."
        self.portfolio[stock.name] -= amount
        revenue = stock.price * amount
        self.cash += revenue
        return True, f"Vendeu {amount} ações de {stock.name} por ${revenue:.2f}."

    def net_worth(self, stocks):
        total = self.cash
        for stock in stocks:
            total += stock.price * self.portfolio.get(stock.name, 0)
        return total

class InvestmentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Investimentos Emocionais")
        self.geometry("500x550")
        self.resizable(False, False)

        self.investor = Investor(1000)
        self.stocks = [
            Stock("TechCorp", 100),
            Stock("FoodInc", 50),
            Stock("AutoMakers", 75)
        ]
        self.emotions = ["pânico", "ganância", "estabilidade", "normal"]
        self.day = 1
        self.total_days = 10

        self.create_widgets()
        self.update_market()

    def create_widgets(self):
        self.day_label = tk.Label(self, text="", font=("Arial", 16))
        self.day_label.pack(pady=10)

        self.emotion_label = tk.Label(self, text="", font=("Arial", 14))
        self.emotion_label.pack(pady=5)

        self.stock_frame = tk.Frame(self)
        self.stock_frame.pack(pady=10)

        self.stock_labels = []
        for stock in self.stocks:
            label = tk.Label(self.stock_frame, text="", font=("Arial", 12))
            label.pack()
            self.stock_labels.append(label)

        self.cash_label = tk.Label(self, text="", font=("Arial", 14))
        self.cash_label.pack(pady=10)

        self.portfolio_label = tk.Label(self, text="", font=("Arial", 12))
        self.portfolio_label.pack(pady=5)

        # Action widgets
        action_frame = tk.Frame(self)
        action_frame.pack(pady=10)

        self.action_var = tk.StringVar(value="passar")
        tk.Radiobutton(action_frame, text="Comprar", variable=self.action_var, value="comprar").grid(row=0, column=0)
        tk.Radiobutton(action_frame, text="Vender", variable=self.action_var, value="vender").grid(row=0, column=1)
        tk.Radiobutton(action_frame, text="Passar", variable=self.action_var, value="passar").grid(row=0, column=2)

        stock_select_frame = tk.Frame(self)
        stock_select_frame.pack(pady=5)

        tk.Label(stock_select_frame, text="Ação: ").grid(row=0, column=0)
        self.stock_var = tk.StringVar(value=self.stocks[0].name)
        stock_names = [s.name for s in self.stocks]
        self.stock_menu = tk.OptionMenu(stock_select_frame, self.stock_var, *stock_names)
        self.stock_menu.grid(row=0, column=1)

        tk.Label(stock_select_frame, text="Quantidade: ").grid(row=1, column=0)
        self.amount_entry = tk.Entry(stock_select_frame, width=10)
        self.amount_entry.grid(row=1, column=1)

        self.confirm_button = tk.Button(self, text="Confirmar Ação", command=self.perform_action)
        self.confirm_button.pack(pady=10)

        self.net_worth_label = tk.Label(self, text="", font=("Arial", 14))
        self.net_worth_label.pack(pady=10)

    def update_market(self):
        if self.day > self.total_days:
            messagebox.showinfo("Fim do jogo", f"Jogo finalizado!\nValor líquido final: ${self.investor.net_worth(self.stocks):.2f}")
            self.confirm_button.config(state=tk.DISABLED)
            return

        self.day_label.config(text=f"Dia {self.day}")
        self.current_emotion = random.choice(self.emotions)
        self.emotion_label.config(text=f"Evento do mercado: {self.current_emotion.upper()}")

        for i, stock in enumerate(self.stocks):
            stock.update_price(self.current_emotion)
            self.stock_labels[i].config(text=str(stock))

        self.cash_label.config(text=f"Dinheiro disponível: ${self.investor.cash:.2f}")
        portfolio_text = ", ".join([f"{k}: {v}" for k, v in self.investor.portfolio.items() if v > 0])
        if not portfolio_text:
            portfolio_text = "Carteira vazia"
        self.portfolio_label.config(text=f"Sua carteira: {portfolio_text}")
        self.net_worth_label.config(text=f"Valor líquido total: ${self.investor.net_worth(self.stocks):.2f}")

    def perform_action(self):
        action = self.action_var.get()
        if action == "passar":
            self.day += 1
            self.amount_entry.delete(0, tk.END)
            self.update_market()
            return

        stock_name = self.stock_var.get()
        stock = next((s for s in self.stocks if s.name == stock_name), None)
        if not stock:
            messagebox.showerror("Erro", "Ação inválida selecionada.")
            return

        try:
            amount = int(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro positivo.")
            return

        if action == "comprar":
            success, msg = self.investor.buy(stock, amount)
        else:
            success, msg = self.investor.sell(stock, amount)

        if success:
            messagebox.showinfo("Sucesso", msg)
            self.day += 1
            self.amount_entry.delete(0, tk.END)
            self.update_market()
        else:
            messagebox.showerror("Erro", msg)

if __name__ == "__main__":
    app = InvestmentApp()
    app.mainloop()
