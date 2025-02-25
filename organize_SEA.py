import os
import matplotlib as plt


def read_second_line(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if len(lines) < 2:
                print("txt檔案內沒有第二行，請檢查內容。")
                return None, None

            second_line = lines[1].strip()  # 取得第二行
            parts = second_line.split(',')  # 以逗號分割

            if len(parts) == 2:
                sp_name = parts[0].strip()  # 取得名稱部分 (string)
                try:
                    sp_sea = float(parts[1].strip())  # 取得數值部分並轉換為 float
                    return sp_name, sp_sea
                except ValueError:
                    print("數值轉換失敗，請檢查格式是否正確。")
                    return None, None
            else:
                print("第二行格式錯誤，應該包含逗號分隔的兩個值。")
                return None, None
    except Exception as e:
        print(f"讀取檔案失敗: {e}")
        return None, None


def main():
    print('你好，使用者。請輸入包含 txt 檔案的資料夾路徑，程式將自動讀取所有檔案。')

    while True:
        folder_path = input('請輸入資料夾路徑：').strip()
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            break
        print("該資料夾不存在，請確認後再試。")

    sp_names = []
    sp_seas = []

    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    if not txt_files:
        print("該資料夾內沒有 txt 檔案。")
        return

    for n, file_name in enumerate(txt_files, start=1):
        file_path = os.path.join(folder_path, file_name)
        sp_name, sp_sea = read_second_line(file_path)
        if sp_name and sp_sea is not None:
            sp_names.append(sp_name)
            sp_seas.append(sp_sea)
            print(f'sp_name_{n}: {sp_name}, sp_SEA_{n}: {sp_sea}')
        else:
            print(f"檔案 {file_name} 內容無法解析，請檢查格式。")

    print('所有數據接收完畢')

    while True:
        series = input('請問這是1系列還是2系列的成果(輸入1或2)：').strip()
        if series == '1':
            pic_title = 'SEA of structures 1'
            file_name = 'SEA_st1_FE'
            break
        elif series == '2':
            pic_title = 'SEA of structures 2'
            file_name = 'SEA_st2_FE'
            break
        else:
            print('請按1或2，再輸入一次：')

    # 設定顏色為藍、紫、深紅、深綠這類型的顏色
    color_palette = ['blue', 'purple', 'red', 'orange', 'green', 'magenta', 'teal']
    ### 直條圖
    colors = [color_palette[(i // 2) % len(color_palette)] for i in range(len(sp_names))]


    plt.figure(figsize=(10, 5))
    # 畫散佈圖
    #plt.scatter(range(len(sp_names)), sp_seas, s=32, c=colors)
    # 畫直條圖
    plt.bar(sp_names, sp_seas, color=colors)
    plt.xlabel('Specimen name')
    plt.ylabel('SEA')
    plt.title(pic_title)
    #plt.xticks(ticks=range(len(sp_names)), labels=sp_names, rotation=60, ha='right')

    plt.xticks(rotation=60, ha='right')
    plt.tight_layout()

    # 輸出圖片
    path = input('請輸入圖片儲存路徑：').strip()
    output_path = os.path.join(path, f"{file_name}.jpg")
    plt.savefig(output_path)
    print(f'圖片已儲存至 {output_path}')
    plt.show()


if __name__ == "__main__":
    main()
