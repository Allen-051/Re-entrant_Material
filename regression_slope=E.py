
import numpy as np
import matplotlib as plt
import os

def get_stress_unit():

    unit_options = {"1": "kPa",
                    "2": "MPa",
                    "3": "GPa"}

    while True:  # 迴圈確保輸入有效
        choice = input(
            "請選擇應力單位:\n"
            "輸入1 >>> kPa\n"
            "輸入2 >>> MPa\n"
            "輸入3 >>> GPa\n"
            "輸入4 >>> 自訂單位\n"
            "請輸入對應數字 (1-4): ")

        if choice in unit_options:
            return unit_options[choice]  # 回傳對應的應力單位
        elif choice == "4":
            return input("請輸入您自訂的應力單位: ")  # 允許自訂應力單位
        else:
            print("輸入錯誤，請輸入 1-4 的數字！\n")  # 提示重新輸入


def read_txt_file():
    file_path = input("請輸入欲分析txt檔的檔案路徑: ")
    with open(file_path, 'r') as f:
        headers = f.readline().strip().split()
        print("偵測並讀取關鍵字:", headers)

        stress_index = headers.index("STRESS")
        strain_index = headers.index("STRAIN")

    data = np.genfromtxt(file_path, skip_header=1)
    stress_y = data[:, stress_index]
    strain_x = data[:, strain_index]

    if len(stress_y) == len(strain_x):
        print(f'應變及應力數據完整，共 {len(stress_y)} 筆資料')
    else:
        print(f'數據長度不一致: 應變 {len(strain_x)} 筆，應力 {len(stress_y)} 筆')

    return strain_x, stress_y


def first_d(x, y):
    n = len(x)
    first_d_arr = np.zeros(n)
    for i in range(1, n):
        first_d_arr[i] = (y[i] - y[i - 1]) / (x[i] - x[i - 1])
    return np.column_stack((x, y, first_d_arr))


def rela_er(first_d, x_y_d):
    n = len(first_d)
    rela_er_arr = np.zeros(n)
    for i in range(2, n):
        if first_d[i] != 0:
            rela_er_arr[i] = round((first_d[i] - first_d[i - 1]) / first_d[i - 1], 5)
    return np.column_stack((x_y_d, rela_er_arr))


def check_re_02(x_y_d_r):
    x_y_valid = [row for row in x_y_d_r if abs(row[3]) <= 0.2]
    x_y_valid = np.array(x_y_valid)
    print(f'符合條件的資料: {len(x_y_valid)} 筆')
    return np.array([",  ".join(map(str, row)) for row in x_y_valid])


def regression(x_y_valid_formatted, unit):

    valid = np.array([list(map(float, row.split(",  "))) for row in x_y_valid_formatted])
    x = valid[:, 0]
    y = valid[:, 1]
    slope, intercept = np.polyfit(x, y, 1)

    print(f"\n線性回歸方程式: y = {slope:.4f}x + {intercept:.4f} [{unit}]\n")

    plt.figure()
    plt.plot(x, y, 'o', label='Valid Data', markersize=1, color='black')
    plt.plot(x, slope * x + intercept, '-', label=f'y = {slope:.4f}x + {intercept:.4f}', color='red')
    plt.xlabel("Strain")
    plt.ylabel(f"Valid Stress ({unit})")
    plt.legend()

    sample_id = input('請輸入試體編號(例：1A、2B): ')
    plt.title(f"{sample_id}, Linear Regression of Strain-Stress Data")

    return slope, intercept


def save_results(x_y_valid_formatted, unit):

    valid = np.array([list(map(float, row.split(",  "))) for row in x_y_valid_formatted])
    title = ['Strain', 'Valid_Stress', '1st_derivative', 'Relative error']
    slope, intercept = np.polyfit(valid[:, 0], valid[:, 1], 1)

    regression_line = f"Linear regression equation: y = {slope:.2f} x + {intercept:.2f}\n"
    regression_line += f"Young's Modulus = {slope:.2f} {unit}.\n* * *"

    document = [[regression_line]] + [title] + [[f"{val:.3f}" for val in row] for row in valid]

    save_path = '*********************'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    result_name = input("請輸入檔案名稱,無須副檔名(ex: 1A_result): ")
    txt_path = os.path.join(save_path, f"{result_name}.txt")
    with open(txt_path, 'w') as file:
        for row in document:
            file.write(",  ".join(row) + '\n')

    plt.savefig(os.path.join(save_path, f"{result_name}.jpg"))
    plt.close()

    print(f"{result_name}.txt and {result_name}.jpg 已儲存到 {save_path}.")


# **主程式執行**
strain_x, stress_y = read_txt_file()
unit = get_stress_unit()  # 讓使用者選擇應力單位
x_y_d = first_d(strain_x, stress_y)
x_y_d_r = rela_er(x_y_d[:, 2], x_y_d)
x_y_valid_formatted = check_re_02(x_y_d_r)
regression(x_y_valid_formatted, unit)
save_results(x_y_valid_formatted, unit)
