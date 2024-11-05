import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Image and ImageTk for handling images

class FoodItem:
    def __init__(self, name, calories, nutrition_value):
        self.name = name
        self.calories = calories
        self.nutrition_value = nutrition_value
        self.value_per_calorie = nutrition_value / calories  # Calculate value per calorie

def fractional_knapsack(calorie_limit, food_items):
    food_items.sort(key=lambda item: item.value_per_calorie, reverse=True)

    total_nutrition_value = 0
    selected_items = []

    for item in food_items:
        if calorie_limit <= 0:
            break

        if item.calories <= calorie_limit:
            selected_items.append((item.name, 1))  # 1 means whole item is taken
            total_nutrition_value += item.nutrition_value
            calorie_limit -= item.calories
        else:
            fraction = calorie_limit / item.calories
            selected_items.append((item.name, fraction))  # Fraction of the item taken
            total_nutrition_value += item.nutrition_value * fraction
            calorie_limit = 0  # No more calorie limit left

    return total_nutrition_value, selected_items

def zero_one_knapsack(calorie_limit, food_items):
    n = len(food_items)
    dp = [[0] * (calorie_limit + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, calorie_limit + 1):
            if food_items[i-1].calories <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-food_items[i-1].calories] + food_items[i-1].nutrition_value)
            else:
                dp[i][w] = dp[i-1][w]

    total_nutrition_value = dp[n][calorie_limit]
    selected_items = []
    w = calorie_limit

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append((food_items[i-1].name, 1))  # Whole item is taken
            w -= food_items[i-1].calories

    return total_nutrition_value, selected_items

def calculate_diet():
    try:
        calorie_limit = float(calorie_entry.get())
        if calorie_limit <= 0:
            raise ValueError("Calorie limit must be greater than 0.")

        # Convert calorie_limit to an integer for knapsack functions
        calorie_limit = int(calorie_limit)

        food_items = [
            FoodItem("Apple", 95, 52),
            FoodItem("Banana", 105, 89),
            FoodItem("Chicken Breast", 165, 31),
            FoodItem("Rice", 206, 16),
            FoodItem("Broccoli", 55, 11),
            FoodItem("Almonds", 579, 21)
        ]

        if knapsack_type.get() == "Fractional Knapsack":
            total_nutrition_value, selected_items = fractional_knapsack(calorie_limit, food_items)
        else:
            total_nutrition_value, selected_items = zero_one_knapsack(calorie_limit, food_items)

        result = f"Total Nutrition Value: {total_nutrition_value:.2f}\n\nSelected Items:\n"
        for item_name, fraction in selected_items:
            if knapsack_type.get() == "Fractional Knapsack":
                result += f"{item_name}: {fraction * 100:.2f}% of the item\n"
            else:
                result += f"{item_name}: Whole item\n"

        messagebox.showinfo("Diet Planning Results", result)
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Set up the main application window
app = tk.Tk()
app.title("Diet Planning: Knapsack Problem")
app.geometry("400x300")
app.configure(bg="#f0f0f0")

# Load the background image
try:
    background_image = Image.open("daim1.jpg")  # Make sure you have this image
    background_image = background_image.resize((400, 300), Image.LANCZOS)  # Resize the image
    background_image.putalpha(120) 
    bg_image = ImageTk.PhotoImage(background_image)

    # Create a label to display the background image
    background_label = tk.Label(app, image=bg_image)
    background_label.place(relwidth=1, relheight=1)  # Make it cover the entire window
except Exception as e:
    print(f"Error loading background image: {e}")

# Create a title label at the top
title_label = tk.Label(app, text="Diet Planning", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# Create a label for calorie limit
calorie_label = tk.Label(app, text="Enter your calorie limit:", bg="#f0f0f0")
calorie_label.pack(pady=10)

# Create an entry for calorie limit
calorie_entry = tk.Entry(app)
calorie_entry.pack(pady=5)

# Create a label for knapsack type selection
knapsack_type = tk.StringVar(value="Fractional Knapsack")
knapsack_label = tk.Label(app, text="Select Knapsack Type:", bg="#f0f0f0")
knapsack_label.pack(pady=10)

# Create radio buttons for knapsack type selection
fractional_button = tk.Radiobutton(app, text="Fractional Knapsack", variable=knapsack_type, value="Fractional Knapsack", bg="#f0f0f0")
fractional_button.pack(anchor=tk.W)

zero_one_button = tk.Radiobutton(app, text="0/1 Knapsack", variable=knapsack_type, value="0/1 Knapsack", bg="#f0f0f0")
zero_one_button.pack(anchor=tk.W)

# Create a button to calculate the diet
calculate_button = tk.Button(app, text="Calculate", command=calculate_diet, bg="#4CAF50", fg="white")
calculate_button.pack(pady=20)

# Start the Tkinter event loop
app.mainloop()
