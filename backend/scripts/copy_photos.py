import os
import shutil

def copy_images(src_dir, dst_dir):
    # Проверяем, существует ли целевая директория, и создаем ее, если нет
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Перебираем файлы в исходной директории
    for filename in os.listdir(src_dir):
        if filename.lower().endswith(('.png')):
            # Путь к исходному файлу
            src_file = os.path.join(src_dir, filename)
            # Путь к целевому файлу
            dst_file = os.path.join(dst_dir, filename)
            # Копирование файла
            shutil.copy(src_file, dst_file)
            print(f'Copied {filename}')

# Использование функции
src_directory = 'tmp/member_photos'
dst_directory = 'mediafiles/member_photos'
copy_images(src_directory, dst_directory)