import os
import shutil
import pathlib
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.ext import Extension

BUILD_DIR = "./build"
TEMPLATE_DIR = "./templates"
IGNORE_DIRS = [".git", "assets"]

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(),
)

def render_html(path):
    if pathlib.Path(path).is_dir():
        for subpath in os.listdir(path):
            render_html(os.path.join(path, subpath))
        return
    # print(path, get_depth(path))
    relpath = pathlib.Path(path).relative_to(TEMPLATE_DIR)
    parts = str(relpath).split(os.path.sep)
    depth = len(parts) - 1
    static_shake_css = os.path.join(*([".."] * depth + ["css/shake.css"]))
    template = env.get_template(str(relpath))
    html = template.render(static_shake_css=static_shake_css)
    os.makedirs(os.path.join(BUILD_DIR, relpath.parent), exist_ok=True)
    with open(os.path.join(BUILD_DIR, str(relpath)), "w") as f:
        f.write(html)


def main():
    os.makedirs(BUILD_DIR, exist_ok=True)
    shutil.copy("assets/robots.txt", os.path.join(BUILD_DIR, "robots.txt"))
    shutil.copy("assets/favicon.ico", os.path.join(BUILD_DIR, "favicon.ico"))
    shutil.copytree("assets/css", os.path.join(BUILD_DIR, "css"))
    shutil.copytree("assets/images", os.path.join(BUILD_DIR, "images"))
    html = render_html(TEMPLATE_DIR)

if __name__ == "__main__":
    main()
