import scipy.optimize
# Цільова функція: 50x_1 + 80x_2 - minimization 
# Обмеження 1: 5x_1 + 2x_2 <= 20
# Обмеження 2: -10x_1 + -12x_2 <= -90
result = scipy.optimize.linprog(
    [50, 80],  # Вартісна функція: 50x_1 + 80x_2, positive for minimization
    A_ub=[[5, 2], [-10, -12]],  # Коефіцієнти для рівняння
    b_ub=[20, -90],  # Коефіцієнти для рівняння: 20 і -90
)
if result.success:
    print("Factory:")
    print(f"X1: {round(result.x[0], 2)} hours")
    print(f"X2: {round(result.x[1], 2)} hours")
else:
    print("Factory: No solution")

# Цільова функція: 500c_1 + 400c_2 - maximization 
# Обмеження 1: 3c_1 + 2x_2 <= 12
# Ліміти: c_1 <=10, c_2 <= 4
result_2 = scipy.optimize.linprog(
    [-500, -400],  # Вартісна функція: 500c_1 + 400c_2, negate for maximization
    A_ub=[[3, 2]],   # Коефіцієнти для рівняння
    b_ub=[12],  # Коефіцієнти для рівняння: 3c_1 + 2c_2 <= 12
    bounds = [(0, 10), (0, 4)],  # Границя для c_1 <=10 і c_2 <= 4
    method='highs'
)

# print(result_2)
if result_2.success:
    print("Farmer:")
    print(f"C1: {round(result_2.x[0], 2)} acres")
    print(f"C2: {round(result_2.x[1], 2)} acres")
else:
    print("Farmer: No solution")

optimal_values = result_2.x
max_value = -result_2.fun  # Negate back to get the true maximum

print("Optimal values (c1, c2):", optimal_values)
print("Maximum objective value:", max_value)