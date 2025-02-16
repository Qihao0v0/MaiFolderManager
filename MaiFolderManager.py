# This code is based on the original work by cyanire,
# click https://github.com/cyanire/AstroDX-Tools to find the original work.
# The original code is licensed under the MIT License.
# Changes made by Qihao to adapt the functionality for personal usage.
import os
import shutil
import json
import argparse

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def move_folder_to_directory(folder_path, target_directory, log_callback=None, log_message=None):
    shutil.move(folder_path, target_directory)
    log_message = log_message or f"Moved {os.path.basename(folder_path)}"
    if log_callback:
        log_callback(log_message)
    else:
        print(log_message)

def organize_folders(parent_dir, log_callback=None):
    parent_dir = os.path.normpath(parent_dir).encode('utf-8').decode('utf-8')
    levels_dir = os.path.join(parent_dir, 'levels')
    collections_dir = os.path.join(parent_dir, 'collections')

    create_directory(levels_dir)
    create_directory(collections_dir)

    for folder in os.listdir(parent_dir):
        folder_path = os.path.join(parent_dir, folder)
        
        if os.path.isdir(folder_path) and folder not in ["levels", "collections"]:
            if not any(os.path.isdir(os.path.join(folder_path, subfolder)) for subfolder in os.listdir(folder_path)):
                move_folder_to_directory(folder_path, collections_dir, log_callback, f"Moved {folder} to collections.")
            else:
                for subfolder in os.listdir(folder_path):
                    subfolder_path = os.path.join(folder_path, subfolder)
                    if os.path.isdir(subfolder_path):
                        move_folder_to_directory(subfolder_path, levels_dir, log_callback, f"Moved {subfolder} to levels.")
                
                move_folder_to_directory(folder_path, collections_dir, log_callback, f"Moved {folder} to collections.")

def create_manifest_for_collection(collection_folder, parent_folder, log_callback=None):
    level_ids = sorted([d for d in os.listdir(collection_folder) if os.path.isdir(os.path.join(collection_folder, d))])

    manifest_data = {
        "name": os.path.basename(collection_folder),
        "id": None,
        "serverUrl": None,
        "levelIds": level_ids
    }

    manifest_path = os.path.join(collection_folder, "manifest.json")

    if os.path.exists(manifest_path):
        os.remove(manifest_path)

    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=4)
    
    log_message = f"Manifest created at: {manifest_path}"

    if log_callback:
        log_callback(log_message)
    else:
        print(log_message)

def copy_and_clean_folder(src_folder):
    dst_folder = src_folder + "_i"
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)  
    shutil.copytree(src_folder, dst_folder)  


    for root, dirs, files in os.walk(dst_folder):
        for file in files:
            if file.endswith('.mp4'):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted {file_path}")

    collections_dir = os.path.join(dst_folder, 'collections')
    create_directory(collections_dir)  

    for folder in os.listdir(dst_folder):
        folder_path = os.path.join(dst_folder, folder)
        if os.path.isdir(folder_path) and folder not in ["levels", "collections"]:
            create_manifest_for_collection(folder_path, dst_folder)

    organize_folders(dst_folder)

    for folder in os.listdir(dst_folder):
        folder_path = os.path.join(dst_folder, folder)
        if os.path.isdir(folder_path) and folder not in ["levels", "collections"]:
            collections_folder = os.path.join(dst_folder, "collections", folder)
            if os.path.exists(collections_folder):
                manifest_path = os.path.join(folder_path, "manifest.json")
                if os.path.exists(manifest_path):
                    shutil.move(manifest_path, collections_folder)
                    print(f"Moved manifest.json to {collections_folder}")

def get_directory_from_args():
    parser = argparse.ArgumentParser(description="Organize folders and create manifests for AstroDX.")
    parser.add_argument(
        "directory", nargs="?", default=os.getcwd(),
        help="The directory to process (default: current directory)."
    )
    args = parser.parse_args()
    return args.directory

if __name__ == "__main__":
    directory = get_directory_from_args()

    mai_folder = os.path.join(directory, 'mai')
    if os.path.exists(mai_folder):
        copy_and_clean_folder(mai_folder)
    else:
        print(f"The 'mai' folder does not exist in the specified directory: {directory}.")
