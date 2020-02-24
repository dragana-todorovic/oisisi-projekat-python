import os


def walk_recursively(path):
    paths = []
    for folder, subs, files in os.walk(path):
        for filename in files:
            if filename.endswith('.html') or filename.endswith('.htm'):
                current_path = os.path.join(folder, filename)
                paths.append(current_path)
    return paths
