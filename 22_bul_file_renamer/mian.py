import os
from pathlib import Path

def bulk_rename_files(
    folder_path: str,
    to_lowercase: bool = True,
    add_prefix: str = "",
    add_suffix: str = "",
    rename_ext: str = None,
    file_ext_filter: list = None
):
    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        print("❌ Invalid folder path. Please check again.")
        return

    files = list(folder.iterdir())

    renamed_count = 0
    print(f"\n📂 Renaming files in: {folder.resolve()}")

    for file in files:
        if file.is_file():
            name, ext = os.path.splitext(file.name)

            # Skip if filtering by extension and is not match
            if file_ext_filter and ext.lower() not in file_ext_filter:
                continue

            new_name = name

            if to_lowercase:
                new_name = new_name.lower()

            if add_prefix:
                new_name = add_prefix + new_name

            if add_suffix:
                new_name = new_name + add_suffix

            new_ext = rename_ext if rename_ext else ext
            new_file_name = new_name + new_ext

            new_path = file.with_name(new_file_name)
            file.rename(new_path)
            print(f"✅ {file.name} → {new_file_name}")
            renamed_count += 1

    print(f"\n🎉 Renamed {renamed_count} file(s).")

def main():
    print("📁 Bulk File Renamer")
    print("----------------------")
    folder = input("Enter the full path of the folder: ").strip()

    bulk_rename_files(
        folder_path=folder,
        to_lowercase=True,          # Rename files to lowercase
        add_prefix="renamed_",      # Add prefix to file names
        add_suffix="",              # Optional: add suffix to file names
        rename_ext=None,            # Optional: change extension e.g; .txt
        file_ext_filter=None        # Optional: filter e.g; .jpg, .png
    )

if __name__ == "__main__":
    main()

