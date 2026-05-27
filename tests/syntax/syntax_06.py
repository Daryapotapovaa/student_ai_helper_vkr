# Задание: работа с матрицами

def create_matrix(rows, cols, default=0):
    return [[default] * cols for _ in range(rows)]

def matrix_sum(matrix_a matrix_b):
    rows = len(matrix_a)
    cols = len(matrix_a[0])
    result = create_matrix(rows, cols)

    for i in range(rows):
        for j in range(cols):
            result[i][j] = matrix_a[i][j] + matrix_b[i][j]

    return result

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(x) for x in row))


a = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]

b = [[9, 8, 7],
     [6, 5, 4],
     [3, 2, 1]]

result = matrix_sum(a, b)
print("Сумма матриц:")
print_matrix(result)
