import tkinter as tk
from tkinter import filedialog
import time

def browse_file():
    file_path = filedialog.askopenfilename()
    file_name.set(file_path)

def run_main():
    if file_name.get():
        num_cities, start_city, end_city, adjacent_cities = read_input_data(file_name.get())
        start_time = time.time()
        min_cost, path = min_cost_travel(num_cities, start_city, end_city, adjacent_cities)
        end_time = time.time()
        time_taken = end_time - start_time
        route = reconstruct_path(start_city, end_city, path)
        result.set(f"The minimum cost for traveling from city {start_city} to city {end_city} is: {min_cost}\n"
                f"The path is: {' -> '.join(map(str, route))}\n"
                f"Time taken: {time_taken:.4f} seconds")

root = tk.Tk()
root.geometry("400x400")
root.title("Minimum Cost Travel")

file_name = tk.StringVar()
result = tk.StringVar()

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=10)

file_label = tk.Label(root, textvariable=file_name)
file_label.pack(pady=10)

run_button = tk.Button(root, text="Run", command=run_main)
run_button.pack(pady=10)

result_label = tk.Label(root, textvariable=result, justify=tk.LEFT)
result_label.pack(pady=10)

def read_input_data(file_name):
    with open(file_name, 'r') as file:
        num_cities = int(file.readline().strip())
        start_city, end_city = map(int, file.readline().strip().split(','))
        adjacent_cities = [list(map(int, line.strip().split(','))) for line in file]

    return num_cities, start_city, end_city, adjacent_cities


def min_cost_travel(num_cities, start_city, end_city, adjacent_cities):
    dp = [[float('inf')] * num_cities for _ in range(num_cities)]
    path = [[-1] * num_cities for _ in range(num_cities)]

    for city_info in adjacent_cities:
        city1, city2, petrol_cost, hotel_cost = city_info
        dp[city1][city2] = petrol_cost + hotel_cost
        dp[city2][city1] = petrol_cost + hotel_cost
        path[city1][city2] = city2
        path[city2][city1] = city1

    for k in range(num_cities):
        for i in range(num_cities):
            for j in range(num_cities):
                if dp[i][j] > dp[i][k] + dp[k][j]:
                    dp[i][j] = dp[i][k] + dp[k][j]
                    path[i][j] = path[i][k]

    return dp[start_city][end_city], path 


def reconstruct_path(start_city, end_city, path):
    if path[start_city][end_city] == -1:
        return None

    route = [start_city]
    while start_city != end_city:
        start_city = path[start_city][end_city]
        route.append(start_city)
    return route
root.mainloop()