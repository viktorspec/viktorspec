import os  # Импорт встроенного модуля os

def rename_files_in_folder(folder_path, prefix="image_"):
    files = os.listdir(folder_path)  # Получаем список всех файлов
    count = 1

    for filename in files:
        file_extension = os.path.splitext(filename)[1]  # Получаем расширение (.jpg и т.д.)
        new_name = f"{prefix}{count}{file_extension}"  # Пример: image_1.jpg
        source = os.path.join(folder_path, filename)
        destination = os.path.join(folder_path, new_name)
        os.rename(source, destination)
        count += 1

    print("Файлы переименованы успешно!")

# Заменяем путь на свой
rename_files_in_folder("C:/Users/Viktor/Downloads/test_folder")
