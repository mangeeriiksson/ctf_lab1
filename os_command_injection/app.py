from flask import Flask, request, render_template, send_from_directory
import subprocess
import os
import shlex
import json

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "indiana_jones_secret"

# Create a directory for our fake files in the local project folder
LOCAL_FILES_DIR = "./virtual_fs"

# Define the real flag (this would be the flag players need to find)
REAL_FLAG = "O24{command_of_the_pharaoh}"

# Define the fake flag that will mislead players initially
FAKE_FLAG = "O24{almost_there_but_not_the_real_flag}"

# Local copies of important files
FAKE_FLAGS = {
    f"{LOCAL_FILES_DIR}/root/ancient_curse.txt": FAKE_FLAG
}

# Simulated filesystem structure
FAKE_FILESYSTEM = {
    "/": ["bin", "etc", "home", "root", "var", "usr", "tmp"],
    "/bin": ["bash", "ls", "cat", "pwd", "whoami", "grep", "find"],
    "/etc": ["passwd", "shadow", "hosts", "apache2", "nginx"],
    "/home": ["anubis", "pharaoh", "explorer"],
    "/home/anubis": ["notes.txt", ".bash_history", "temple_map.jpg"],
    "/home/pharaoh": ["secret_scroll.txt", ".bash_history", "treasure.dat"],
    "/home/explorer": ["README.md", ".bash_history", "clues.txt"],
    "/root": ["ancient_curse.txt", ".bash_history", "admin_notes.txt", "secret_key"],
    "/var": ["log", "www"],
    "/var/log": ["auth.log", "system.log", "access.log"],
    "/usr": ["bin", "local", "share"],
    "/usr/bin": ["python", "perl", "ruby", "gcc"],
    "/tmp": ["cache", "session.1", "artifacts.old"]
}

# Create a .bash_history with the real flag hidden among commands
EXPLORER_HISTORY = [
    "ls -la",
    "cd /home/anubis",
    "cat notes.txt",
    "grep 'treasure' /home/pharaoh/secret_scroll.txt",
    "cd /root",
    "cat ancient_curse.txt",
    "echo 'This is not working'",
    "find / -name '*flag*' 2>/dev/null",
    f"echo '{REAL_FLAG}' > found_it.txt  # OH! I found it!", 
    "rm found_it.txt  # Better remove this quickly",
    "cd /var/log",
    "grep 'suspicious' auth.log",
    "cd /home/explorer",
    "clear",
    "exit"
]

# Simulated file contents
FAKE_FILE_CONTENTS = {
    "/home/anubis/notes.txt": "I've hidden the sacred artifact somewhere in the temple. The pharaoh must never find it.",
    "/home/anubis/.bash_history": "\n".join([
        "ls -la", 
        "cd /root", 
        "cat ancient_curse.txt", 
        "exit"
    ]),
    "/home/pharaoh/secret_scroll.txt": "The curse of Anubis protects the sacred treasure. Only those who walk the path of the gods may find the true artifact.",
    "/home/pharaoh/.bash_history": "\n".join([
        "cd /var/log", 
        "grep 'intruder' auth.log", 
        "cd /home/anubis", 
        "ls -la", 
        "exit"
    ]),
    "/home/explorer/.bash_history": "\n".join(EXPLORER_HISTORY),
    "/root/ancient_curse.txt": FAKE_FLAG,
    "/root/.bash_history": "\n".join([
        "cd /etc", 
        "nano shadow", 
        "systemctl restart ssh", 
        "exit"
    ]),
    "/root/admin_notes.txt": "Remember to rotate all keys and check for unauthorized access attempts in the logs."
}

# Check if our local storage directory exists
if not os.path.exists(LOCAL_FILES_DIR):
    os.makedirs(LOCAL_FILES_DIR, exist_ok=True)

# Create the root directory in our local storage
if not os.path.exists(f"{LOCAL_FILES_DIR}/root"):
    os.makedirs(f"{LOCAL_FILES_DIR}/root", exist_ok=True)

# Create the fake flag file in our local storage
for path, content in FAKE_FLAGS.items():
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)

# Fix for static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route("/")
def index():
    return render_template("temple_anubis.html")

# Helper function to handle simulated commands
def handle_simulated_command(command):
    parts = shlex.split(command)
    base_cmd = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    
    # Handle ls command
    if base_cmd == "ls":
        path = "/"
        show_hidden = False
        
        # Check for -a or -la flags
        if "-a" in args or "-la" in args or "-al" in args:
            show_hidden = True
            
        # Get the path argument
        for arg in args:
            if not arg.startswith("-"):
                path = arg
                break
                
        # Normalize path
        if not path.startswith("/"):
            path = f"/{path}"
            
        if path in FAKE_FILESYSTEM:
            files = FAKE_FILESYSTEM[path]
            if show_hidden and path.startswith("/home") or path == "/root":
                files = [".bash_profile", ".bashrc", "."] + files + ["..", ".bash_history"]
            return "\n".join(files)
        else:
            return f"ls: cannot access '{path}': No such file or directory"
    
    # Handle cat command
    elif base_cmd == "cat":
        if not args:
            return "cat: missing operand"
            
        path = args[0]
        if not path.startswith("/"):
            path = f"/{path}"
            
        # For simulated files
        if path in FAKE_FILE_CONTENTS:
            return FAKE_FILE_CONTENTS[path]
        else:
            return f"cat: {path}: No such file or directory"
    
    # Handle grep command
    elif base_cmd == "grep":
        if len(args) < 2:
            return "grep: missing operand"
            
        pattern = args[0]
        file_path = args[1]
        
        if not file_path.startswith("/"):
            file_path = f"/{file_path}"
            
        if file_path in FAKE_FILE_CONTENTS:
            content = FAKE_FILE_CONTENTS[file_path]
            result = []
            for line in content.split("\n"):
                if pattern in line:
                    result.append(line)
            if result:
                return "\n".join(result)
            else:
                return ""
        else:
            return f"grep: {file_path}: No such file or directory"
    
    # Handle pwd command
    elif base_cmd == "pwd":
        return "/temple/of/anubis"
    
    # Handle whoami command
    elif base_cmd == "whoami":
        return "explorer"
    
    # Handle id command
    elif base_cmd == "id":
        return "uid=1000(explorer) gid=1000(explorers) groups=1000(explorers)"
    
    # Handle find command (simplified)
    elif base_cmd == "find":
        if not args or args[0] != "/":
            return "find: missing operand"
            
        if "-name" in args and len(args) > args.index("-name") + 1:
            pattern = args[args.index("-name") + 1].replace("*", "")
            results = []
            for path in FAKE_FILE_CONTENTS:
                if pattern in os.path.basename(path):
                    results.append(path)
            return "\n".join(results) if results else ""
        return ""
    
    return f"Command not found: {base_cmd}"

@app.route("/temple", methods=["GET", "POST"])
def temple_of_anubis():
    result = None
    if request.method == "POST":
        command = request.form.get("command", "").strip()
        
        # Commands we'll simulate
        simulated_commands = ["ls", "cat", "pwd", "whoami", "id", "grep", "find"]
        
        cmd_parts = shlex.split(command)
        if cmd_parts:
            base_cmd = cmd_parts[0]
            
            # Check if it's a command we want to simulate
            if base_cmd in simulated_commands:
                result = handle_simulated_command(command)
            else:
                result = "⚠️ Forbidden command! The gods do not approve of this magic."
        
    return render_template("temple_anubis.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6002, debug=True)