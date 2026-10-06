import os

FRONTEND_SRC = r"C:\Users\Profesor\Desktop\Frontend\tienda-frontend\src"

def write(relpath, content):
    fullpath = os.path.join(FRONTEND_SRC, relpath)
    os.makedirs(os.path.dirname(fullpath), exist_ok=True)
    with open(fullpath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Written: {fullpath}")
