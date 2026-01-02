import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import webbrowser
import os
import markdown2

# CSS templates (shortened for clarity, you can keep the full ones)
CSS_TEMPLATES = {
    "Dark Mode": "body { background:#1e1e1e; color:#e6e6e6; font-family:sans-serif; }",
    "Light Mode": "body { background:#fff; color:#222; font-family:sans-serif; }",
    "Minimal": "body { font-family:Georgia, serif; margin:40px auto; max-width:700px; }",
    "Fancy": "body { background:linear-gradient(120deg,#fdfbfb,#ebedee); font-family:Inter,sans-serif; }"
}

HTML_SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="container">
{body}
</div>
<footer style="text-align:center; margin:2rem 0; opacity:0.7;">Created by Kian Pourali</footer>
</body>
</html>
"""

md_path = None

def select_md_file():
    global md_path
    file_path = filedialog.askopenfilename(
        title="Select Markdown file",
        filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt")]
    )
    if file_path:
        md_path = file_path
        messagebox.showinfo("File Selected", f"Markdown file:\n{md_path}")

def do_convert():
    global md_path
    if not md_path:
        messagebox.showerror("Error", "Please select a Markdown file first.")
        return

    css_key = css_var.get()
    title = title_var.get().strip() or "Document"

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_body = markdown2.markdown(md_text, extras=["fenced-code-blocks", "tables"])
    css = CSS_TEMPLATES.get(css_key, CSS_TEMPLATES["Light Mode"])
    html = HTML_SHELL.format(title=title, css=css, body=html_body)

    save_path = filedialog.asksaveasfilename(
        title="Save HTML",
        defaultextension=".html",
        filetypes=[("HTML files", "*.html")]
    )
    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(html)
        messagebox.showinfo("Success", f"Saved HTML:\n{save_path}")
        if preview_var.get():
            webbrowser.open(f"file://{os.path.abspath(save_path)}")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Markdown → HTML Converter")
root.geometry("500x300")
root.configure(bg="#1e1e1e")

tk.Label(root, text="Markdown → HTML Converter", font=("Arial", 16, "bold"),
         bg="#1e1e1e", fg="white").pack(pady=12)

# Button only for file selection
btn_select = tk.Button(root, text="Select Markdown File", command=select_md_file,
                       bg="#3498DB", fg="white", relief="flat", font=("Arial", 12))
btn_select.pack(pady=10)

# Title input
title_var = tk.StringVar(value="Document")
tk.Label(root, text="HTML Title:", bg="#1e1e1e", fg="white").pack()
tk.Entry(root, textvariable=title_var, width=40).pack(pady=5)

# CSS selector
css_var = tk.StringVar(value="Dark Mode")
tk.Label(root, text="CSS Template:", bg="#1e1e1e", fg="white").pack()
ttk.Combobox(root, textvariable=css_var, values=list(CSS_TEMPLATES.keys()), state="readonly").pack(pady=5)

# Preview checkbox
preview_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Open in browser after saving", variable=preview_var,
               bg="#1e1e1e", fg="white", selectcolor="#1e1e1e").pack(pady=5)

# Convert button
tk.Button(root, text="Convert & Save HTML", command=do_convert,
          bg="#2ECC71", fg="white", font=("Arial", 12), relief="flat").pack(pady=12)

tk.Label(root, text="Created by MasterK", font=("Arial", 10, "italic"),
         bg="#1e1e1e", fg="#888888").pack(side="bottom", pady=8)

root.mainloop()
