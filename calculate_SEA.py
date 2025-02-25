
import os
import numpy as np
import matplotlib as plt

def ask_unit():
    while True:
        choice = input("請告訴我應力單位：\n按下1，單位為kPa\n按下2，單位為MPa\n按下3，單位為GPa\n按下4，自行輸入：")
        if choice == '1':
            unit = 'kPa'
            break
        elif choice == '2':
            unit = 'MPa'
            break
        elif choice == '3':
            unit = 'GPa'
            break
        elif choice == '4':
            unit = input("請輸入應力單位：")
            break
        else:
            print("請輸入1-4之間的數字！")
    return unit

def read_txt():
    while True:
        file_path = input("請輸入欲讀取的檔案路徑(完整路徑)：")
        if os.path.exists(file_path):
            break
        print("該檔案不存在，請重新輸入。")

    with open(file_path, 'r') as f:
        headers = f.readline().strip().split()
        print("偵測並讀取關鍵字:", headers)

        stress_index = headers.index("STRESS")
        strain_index = headers.index("STRAIN")

    data = np.genfromtxt(file_path, skip_header=1)
    stress_y = data[:, stress_index]
    strain_x = data[:, strain_index]

    stress_y = np.array(stress_y)
    strain_x = np.array(strain_x)

    #### 檢查stress、strain陣列 ###
    #print(stress_y)
    #print(strain_x)

    if len(stress_y) == len(strain_x):
        print(f'應變及應力數據完整，共 {len(stress_y)} 筆資料')
    else:
        print(f'數據長度不一致: 應變 {len(strain_x)} 筆，應力 {len(stress_y)} 筆')

    return strain_x, stress_y


def energy_ab(strain_x, stress_y):
    EA = np.zeros(len(stress_y))
    for i in range(1, len(stress_y)):
        if stress_y[i] + stress_y[i - 1] <= 0:
            EA[i] = EA[i - 1]
        else:
            EA[i] = round((stress_y[i] + stress_y[i - 1]) * (strain_x[i] - strain_x[i - 1]) / 2 + EA[i - 1], 4)

    if len(EA) == len(strain_x):
        print("Energy Absorption陣列數據齊全")

    EA_form = np.column_stack((strain_x, stress_y, EA))
    print("EA_form shape:", EA_form.shape)
    return EA_form


def find_EE_and_SEA(EA_form):
    EE = np.zeros(len(EA_form))
    for i in range(len(EA_form)):
        if EA_form[i, 1] <= 0:
            EE[i] = 0
        else:
            EE[i] = round(EA_form[i, 2] / EA_form[i, 1], 4)

    EE_form = np.column_stack((EA_form, EE))
    print("EE_form shape:", EE_form.shape)

    ### 找出最大的能量吸收效率點 ###
    Max_EE = np.max(EE_form[:, 3])
    print(f'Energy Efficiency最大值為 {Max_EE:.4f}')
    max_index = np.argmax(EE_form[:, 3])
    Max_EA = EE_form[max_index, 2]
    print(f'對應的最大Energy Absorption為 {Max_EA:.2f}')
    EE_form[max_index, 2] = Max_EA

    while True:
        ask_number = float(input("請輸入試體重量(g)："))
        if 15 <= ask_number <= 26:
            break
        Double_ask = int(input("您確定這是對的試體重量嗎？按1表示確定，按2重新輸入："))
        if Double_ask == 1:
            break
    SEA = Max_EA / ask_number
    print(f'SEA: {SEA:.4f}')

    return EE_form, Max_EE, SEA

def plot(unit, EE_form, path, name):

    x = EE_form[:, 0]
    y1 = EE_form[:, 1]
    y2 = EE_form[:, 3]

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    line1, = ax1.plot(x, y1, 'k-', label='Stress')
    line2, = ax2.plot(x, y2, 'r-', label='Energy Efficiency')

    ax1.set_xlabel('Strain')
    ax1.set_ylabel(f'Stress ({unit})', color='black')
    ax2.set_ylabel('Energy Efficiency', color='red')
    plt.title(name)

    plt.figtext(0.74, 0.9, f'SEA: {SEA_value:.3f}', ha='left', fontsize=10,
                bbox={'facecolor': 'white', 'alpha': 0, 'pad': 3})


    plt.legend([line1, line2], ['Stress', 'Energy Efficiency'], loc='upper left')

    plt.savefig(path)
    plt.show()


def txt(unit, EE_form, path, name, SEA):
    title1  = f'NAME, SEA VALUE \n{name}, {SEA:.3f}\n* * * * *'
    title2  = ['Strain', f'Stress({unit})', 'Energy Absorption', 'Energy Efficiency']
    txt_title = [[title1]] + [title2] + EE_form.tolist()

    with open(path, 'w', encoding='utf-8') as f:
        for row in txt_title:
            f.write(',    '.join(map(str, row)) + '\n')



### 主要修改內容 ###
unit = ask_unit()
strain_x, stress_y = read_txt()
EA_form = energy_ab(strain_x, stress_y)
EE_form, Max_EE, SEA_value = find_EE_and_SEA(EA_form)
save_path = r'D:\auxetic_E\FE_result\FE_SEA'
file_name = input("請輸入檔案名稱（不含副檔名），這同時也會是圖片標題：")
path_txt = os.path.join(save_path, f"{file_name}.txt")
path_jpg = os.path.join(save_path, f"{file_name}.jpg")

plot(unit, EE_form, path_jpg, file_name)

txt(unit, EE_form, path_txt, file_name, SEA_value)

print(f'「txt檔」及「圖片」皆已經儲存至 {save_path}.')

