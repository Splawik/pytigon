import json
from pathlib import Path


def scan_and_save(target_folder):
    start_path = Path(target_folder).resolve()
    output_data = []

    # File extensions to scan
    extensions = ["*.py", "*.md"]

    # We manually traverse to safely handle symlinked directories
    # and avoid infinite loops via 'visited' set
    visited_paths = set()

    def traverse_directory(current_dir):
        # Resolve symlinks to get the real path and prevent infinite recursion
        try:
            real_path = current_dir.resolve(strict=True)
        except (FileNotFoundError, PermissionError):
            return

        if real_path in visited_paths:
            return
        visited_paths.add(real_path)

        # 1. Process files matching patterns in the current directory
        for ext in extensions:
            # glob() looks only at the current directory level
            for file_path in current_dir.glob(ext):
                # is_file() is True for regular files and symlinks to files
                if file_path.is_file():
                    try:
                        # Read content (follows symlink automatically)
                        content = file_path.read_text(encoding="utf-8")

                        # If it's a symlink, relative_to might fail if it points outside.
                        # We use the path as it appears inside the scanned folder.
                        try:
                            relative_path = file_path.relative_to(start_path)
                        except ValueError:
                            # Fallback if symlink points completely outside the tree
                            relative_path = file_path.name

                        if "frontend/" in str(relative_path):
                            break
                        if "tests/" in str(relative_path):
                            break
                        output_data.append({"nazwa": str(relative_path), "content": content})
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")

        # 2. Recursively enter subdirectories (including symlinked folders)
        try:
            for item in current_dir.iterdir():
                if item.is_dir():
                    traverse_directory(item)
        except PermissionError:
            print(f"Permission denied for directory: {current_dir}")

    # Start recursion
    traverse_directory(start_path)

    # Save to prj.json in the current working directory
    output_file = Path("prj.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Successfully saved {len(output_data)} files to {output_file.absolute()}")


# --- Script Execution ---
folder_to_scan = "."
scan_and_save(folder_to_scan)
