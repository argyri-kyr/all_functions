import ast
import os
import xlsxwriter

def extract_imports(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=filename)

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)

    return imports

def extract_called_functions(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=filename)

    called_functions = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if hasattr(node.func, 'id'):
                called_functions.add(node.func.id)

    return called_functions

def extract_all_imports(filename, base_directory, folder_paths=None, visited=None):
    if folder_paths is None:
        folder_paths = []

    if visited is None:
        visited = set()

    all_imports = set()
    stack = [filename]

    while stack:
        current_file = stack.pop()
        if current_file in visited:
            continue

        visited.add(current_file)

        current_imports = extract_imports(current_file)
        all_imports.update(current_imports)

        called_functions = extract_called_functions(current_file)
        for func in called_functions:
            func_file = os.path.join(base_directory, func + '.py')
            if os.path.exists(func_file):
                stack.append(func_file)
            else:
                for folder_path in folder_paths:
                    func_file_in_folder = os.path.join(folder_path, func + '.py')
                    if os.path.exists(func_file_in_folder):
                        stack.append(func_file_in_folder)

        # Extract imports from called functions
        for import_file in current_imports:
            import_path = os.path.join(base_directory, import_file + '.py')
            if os.path.exists(import_path):
                stack.append(import_path)
            else:
                for folder_path in folder_paths:
                    import_path_in_folder = os.path.join(folder_path, import_file + '.py')
                    if os.path.exists(import_path_in_folder):
                        stack.append(import_path_in_folder)

    return all_imports



def main(filename):
    base_directory = "./"  # Replace with the base directory where the main Python file and function files are located
    full_main_path = os.path.join(base_directory, filename)

    folder_paths = ["./semiauto_or_auto_process_for_old_data", "./semiauto_or_auto_process", "./procedures", "./my_main_processes", "./"]  # Replace with the paths to the procedures folders
    all_imports = extract_all_imports(full_main_path, base_directory, folder_paths)
    
    if all_imports:
        
        workbook = xlsxwriter.Workbook('./write_data.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write_column(0, 0, all_imports)
        workbook.close()
    
        print("\nAll imports:\n")
        for imp in all_imports:
            print(imp)
    
    else:
        print("No imports found.")



main("./my_main_processes/ofthalmos_multiple_options_main.py")
