from flask import Flask, request, render_template
import os
import re

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "indiana_jones_secret"

# Change to use local directories instead of system directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIRTUAL_FS_DIR = os.path.join(BASE_DIR, "virtual_fs")

# Virtual paths for the CTF challenge
SECURE_FLAG_PATH = "/root/flags/true_flag.txt"
VIRTUAL_FLAG_PATH = os.path.join(VIRTUAL_FS_DIR, "root", "flags", "true_flag.txt")

# Define the real flag
REAL_FLAG = "O24{c0ngr4tul4t10ns_y0u_f0und_th3_r34l_fl4g!}"

# Map of all virtual files and their contents
VIRTUAL_FILES = {
    "/var/www/html/index.html": "<html><body><h1>Temple of Anubis</h1></body></html>",
    "/var/www/html/flags/ancient_scroll.txt": "O24{this_is_not_the_real_flag}",
    "/var/www/html/flags/cursed_tablet.txt": "O24{so_close_but_not_it}",
    "/etc/passwd": "root:x:0:0:root:/root:/bin/bash\nanubis:x:1000:1000:Temple Guard:/home/anubis:/bin/bash",
    "/etc/hosts": "127.0.0.1 localhost\n127.0.1.1 temple",
    "/root/flags/true_flag.txt": REAL_FLAG
}

# Map of directory contents in the virtual filesystem
VIRTUAL_DIRS = {
    "/": ["var", "etc", "root", "home"],
    "/var": ["www"],
    "/var/www": ["html"],
    "/var/www/html": ["flags", "index.html"],
    "/var/www/html/flags": ["ancient_scroll.txt", "cursed_tablet.txt"],
    "/etc": ["passwd", "hosts"],
    "/root": ["flags"],
    "/root/flags": ["true_flag.txt"],
    "/home": ["anubis"],
    "/home/anubis": []
}

# Valid paths - only these should work
ALLOWED_EXPLOIT_PATHS = [
    "..././..././root",
    "..././..././root/flags",
    "..././..././root/flags/true_flag.txt"
]

# Check if a path should be blocked
def is_path_allowed(path):
    # Allow access to regular directories without traversal
    if not any(traversal in path for traversal in ["../", "..\\"]):
        # But still block direct access to /root
        if path.startswith("/root") or path.startswith("root"):
            return False
        return True
    
    # Only allow our specific exploit paths
    if path in ALLOWED_EXPLOIT_PATHS:
        return True
    
    # Block all other path traversal attempts
    return False

# Normalize the path based on allowed patterns
def normalize_path(path):
    # Special handling for our exact allowed exploit paths
    if path == "..././..././root":
        return "/root"
    elif path == "..././..././root/flags":
        return "/root/flags"
    elif path == "..././..././root/flags/true_flag.txt":
        return "/root/flags/true_flag.txt"
    
    # Standard path normalization for other paths
    normalized = os.path.normpath("/" + path)
    return normalized

# Create the directories for local storage
os.makedirs(VIRTUAL_FS_DIR, exist_ok=True)
os.makedirs(os.path.join(VIRTUAL_FS_DIR, "root", "flags"), exist_ok=True)
os.makedirs(os.path.join(VIRTUAL_FS_DIR, "var", "www", "html", "flags"), exist_ok=True)

# Create the flag file in local storage for reference
with open(os.path.join(VIRTUAL_FS_DIR, "root", "flags", "true_flag.txt"), "w") as f:
    f.write(REAL_FLAG)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/papyrus", methods=["GET", "POST"])
def papyrus():
    requested_file = request.form.get("file", "").strip()
    if not requested_file:
        return render_template("papyrus.html")
    
    # Log the request for debugging
    print(f"Requested file: {requested_file}")
    
    # Check if the path is allowed
    if not is_path_allowed(requested_file):
        print(f"Path blocked: {requested_file}")
        return render_template("papyrus.html", 
                              hint="🚫 Path traversal blocked! The temple guardians have detected your tricks.")
    
    # Handle the specific exploit paths
    if requested_file == "..././..././root/flags/true_flag.txt":
        print(f"Flag found via exploit path: {REAL_FLAG}")
        return render_template("papyrus.html", content=REAL_FLAG)
    
    # Normalize the path for allowed requests
    normalized_path = normalize_path(requested_file)
    print(f"Normalized path: {normalized_path}")
    
    # Check if it's a directory in our virtual filesystem
    if normalized_path in VIRTUAL_DIRS:
        files = VIRTUAL_DIRS[normalized_path]
        print(f"Directory contents for {normalized_path}: {files}")
        return render_template("papyrus.html", file_list=files)
    
    # Check if it's a file in our virtual filesystem
    if normalized_path in VIRTUAL_FILES:
        content = VIRTUAL_FILES[normalized_path]
        print(f"File content found: {content[:30]}...")
        return render_template("papyrus.html", content=content)
    
    # If nothing matches, return file not found
    return render_template("papyrus.html", hint="📜 The file or directory was not found.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6003, debug=True)