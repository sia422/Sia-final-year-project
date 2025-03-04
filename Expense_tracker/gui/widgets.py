import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ExpenseChart:
    def __init__(self, root, expenses):
        self.root = root
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        self.update_chart(expenses)

    def update_chart(self, expenses):
        self.ax.clear()
        categories = [expense["category_id"] for expense in expenses]
        amounts = [expense["amount"] for expense in expenses]

        self.ax.bar(categories, amounts)
        self.ax.set_xlabel("Category")
        self.ax.set_ylabel("Amount")
        self.ax.set_title("Expenses by Category")
        self.canvas.draw()