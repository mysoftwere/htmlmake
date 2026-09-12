import os
import re
import json
import time
import base64
import shutil
import mimetypes
import threading
import html as html_lib
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import openpyxl

# ─────────────────────────────────────────────────────────────
#  DEFAULT PATHS & CONSTANTS
# ─────────────────────────────────────────────────────────────
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_EXCEL = os.path.join(CURRENT_DIR, "HTML MAKE.xlsx")
DEFAULT_OUTPUT_DIR = os.path.join(CURRENT_DIR, "Output")
DEFAULT_TEMPLATE_FILE = os.path.join(CURRENT_DIR, "template.html")
CONFIG_FILE = os.path.join(CURRENT_DIR, "config.json")
DEFAULT_SCRIPT_LINK = "https://portalbsc.github.io/let/sp.js"
DEFAULT_TEMPLATE_IMAGE = "https://cdnb.artstation.com/p/assets/images/images/076/569/795/large/full-video-video-adik-kakak-viral-tiktok-baju-biru-full-7-menit-link-hd-30.jpg"

def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_config(data):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def load_base_template():
    if os.path.exists(DEFAULT_TEMPLATE_FILE):
        with open(DEFAULT_TEMPLATE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# ─────────────────────────────────────────────────────────────
#  SLUG GENERATOR
# ─────────────────────────────────────────────────────────────
def generate_file_slug(raw_title: str) -> str:
    """
    Generates a clean, safe lowercase filename slug like:
    'bangla-xxx-bangla-adult-video-young.html'
    """
    if not raw_title:
        return "video.html"
    
    # Remove special punctuation and symbols, keep alphanumeric and spaces
    clean = re.sub(r'[^a-zA-Z0-9\s_-]', ' ', raw_title)
    words = clean.strip().split()
    if not words:
        return "video.html"
    
    slug = '-'.join(words[:7]).lower()
    return f"{slug}.html"

# ─────────────────────────────────────────────────────────────
#  IMAGE HANDLING (LOCAL OR URL)
# ─────────────────────────────────────────────────────────────
def prepare_image_for_html(image_input: str, output_dir: str = "") -> str:
    """
    Handles both web URLs and local image file paths.
    Converts local image to Base64 so it works completely self-contained.
    """
    if not image_input:
        return ""
    clean_path = str(image_input).strip().strip('"').strip("'")
    if os.path.exists(clean_path) and os.path.isfile(clean_path):
        try:
            if output_dir and os.path.exists(output_dir):
                dest = os.path.join(output_dir, os.path.basename(clean_path))
                if not os.path.exists(dest) or os.path.abspath(clean_path) != os.path.abspath(dest):
                    shutil.copy2(clean_path, dest)
            mime_type, _ = mimetypes.guess_type(clean_path)
            if not mime_type:
                mime_type = "image/jpeg"
            with open(clean_path, "rb") as f:
                b64_str = base64.b64encode(f.read()).decode("utf-8")
            return f"data:{mime_type};base64,{b64_str}"
        except Exception:
            pass
    return clean_path

# ─────────────────────────────────────────────────────────────
#  HTML BUILDER / TEMPLATE INJECTOR
# ─────────────────────────────────────────────────────────────
def build_html_content(raw_title: str, custom_link: str = "", image_url: str = "") -> str:
    """
    Builds the complete HTML by injecting the title from Column A,
    the script link (Column C or fixed https://portalbsc.github.io/let/sp.js),
    and optional custom image into the template accurately.
    """
    base_template = load_base_template()
    if not base_template:
        raise FileNotFoundError("template.html not found! Please place template.html in the software folder.")

    html = base_template
    clean_title = raw_title.strip()
    safe_title_attr = html_lib.escape(clean_title, quote=True)
    safe_json_title = clean_title.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')

    # 1. Script Tag Injection (Column C link or fixed sp.js)
    active_script = custom_link.strip() if custom_link and custom_link.strip() else DEFAULT_SCRIPT_LINK
    # If full script tag was pasted, extract URL or use as is
    if active_script.startswith("<script"):
        m = re.search(r'src=[\'"]([^\'"]+)[\'"]', active_script)
        if m:
            active_script = m.group(1)
        else:
            active_script = DEFAULT_SCRIPT_LINK

    if re.search(r'<script\s+src=[\'"][^\'"]*?(?:sp\.js|m1\.js|epl1\.js)[^\'"]*?[\'"]\s*></script>', html, flags=re.IGNORECASE):
        html = re.sub(
            r'<script\s+src=[\'"][^\'"]*?(?:sp\.js|m1\.js|epl1\.js)[^\'"]*?[\'"]\s*></script>',
            f'<script src="{active_script}"></script>',
            html,
            count=1,
            flags=re.IGNORECASE
        )
    else:
        # Fallback: insert before </head>
        html = re.sub(r'(</head>)', f'  <script src="{active_script}"></script>\n\\1', html, count=1, flags=re.IGNORECASE)

    # 2. Update <title>...</title>
    html = re.sub(r'<title>.*?</title>', f'<title>\n{clean_title}\n  </title>', html, count=1, flags=re.DOTALL | re.IGNORECASE)

    # 3. Update Meta tags (name="title", name="description", name="x:title", name="x:description", property="og:title", property="og:description")
    html = re.sub(r'(<meta\s+content=)["][^"]*?["](\s+name=[\'"]title[\'"])', rf'\1"{safe_title_attr}"\2', html, flags=re.IGNORECASE)
    html = re.sub(r'(<meta\s+content=)["][^"]*?["](\s+name=[\'"]description[\'"])', rf'\1"{safe_title_attr}"\2', html, flags=re.IGNORECASE)
    html = re.sub(r'(<meta\s+content=)["][^"]*?["](\s+name=[\'"]x:title[\'"])', rf'\1"{safe_title_attr}"\2', html, flags=re.IGNORECASE)
    html = re.sub(r'(<meta\s+content=)["][^"]*?["](\s+name=[\'"]x:description[\'"])', rf'\1"{safe_title_attr}"\2', html, flags=re.IGNORECASE)
    html = re.sub(r'(<meta\s+content=)["][^"]*?["](\s+property=[\'"]og:title[\'"])', rf'\1"{safe_title_attr}"\2', html, flags=re.IGNORECASE)
    html = re.sub(r'(<meta\s+content=)["][^"]*?["](\s+property=[\'"]og:description[\'"])', rf'\1"{safe_title_attr}"\2', html, flags=re.IGNORECASE)

    # 4. Update Article Header & Headline
    html = re.sub(r'(<span\s+class=[\'"]sdc-article-header__long-title[\'"]>).*?(</span>)', rf'\1\n       {clean_title}\n         \2', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'(data-short-title=)["][^"]*?["]', rf'\1"{safe_title_attr}"', html, flags=re.IGNORECASE)

    # 5. Update Video Widget Caption & Caption Text
    html = re.sub(r'(data-caption=)["][^"]*?["]', rf'\1"{safe_title_attr}"', html, flags=re.IGNORECASE)
    html = re.sub(r'(<span\s+class=[\'"]ui-media-caption__caption-text[\'"][^>]*>).*?(</span>)', rf'\1\n     {clean_title}\n       \2', html, flags=re.DOTALL | re.IGNORECASE)

    # 6. Update All Related Video Tiles Headlines
    html = re.sub(r'(<span\s+class=[\'"]sdc-site-tile__headline-text[\'"][^>]*>).*?(</span>)', rf'\1\n           {clean_title}\n             \2', html, flags=re.DOTALL | re.IGNORECASE)

    # 7. Update JSON-LD Schemas (NewsArticle & VideoObject)
    html = re.sub(r'("headline"\s*:\s*")[^"]*?(")', rf'\1{safe_json_title}\2', html)
    html = re.sub(r'("alternativeHeadline"\s*:\s*")[^"]*?(")', rf'\1{safe_json_title}\2', html)
    html = re.sub(r'("articleBody"\s*:\s*")[^"]*?(")', rf'\1{safe_json_title}\2', html)
    html = re.sub(r'("description"\s*:\s*")[^"]*?(")', rf'\1{safe_json_title}\2', html)
    html = re.sub(r'("name"\s*:\s*")[^"]*?(")', rf'\1{safe_json_title}\2', html)

    # 8. Update Advert-Manager Config JSON (title & description)
    html = re.sub(r'("consumption"\s*:\s*\{"metadata"\s*:\s*\{"type"\s*:\s*"story"\s*,\s*"description"\s*:\s*")[^"]*?(")', rf'\1{safe_json_title}\2', html)
    html = re.sub(r'(,\s*"title"\s*:\s*")[^"]*?(")', rf'\1{safe_json_title}\2', html)
    html = re.sub(r'("mediaTitle"\s*:\s*")[^"]*?(")', rf'\1{safe_json_title}\2', html)

    # 9. Update Dates to Current Date
    today_str = datetime.now().strftime('%Y-%m-%d')
    html = re.sub(r'(<p\s+class=[\'"]sdc-article-date__date-time[\'"]>).*?(</p>)', rf'\1\n           {today_str}\n          \2', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'("datePublished"\s*:\s*")[^"]*?(")', rf'\1{today_str}T23:59:00+0000\2', html)
    html = re.sub(r'("uploadDate"\s*:\s*")[^"]*?(")', rf'\1{today_str}T23:59:00+0000\2', html)

    # 10. Optional Image Replacement (if Column D image is provided)
    if image_url and image_url.strip():
        img = image_url.strip()
        html = re.sub(r'https://cdnb\.artstation\.com/p/assets/images/images/076/569/795/large/full-video-video-adik-kakak-viral-tiktok-baju-biru-full-7-menit-link-hd-30\.jpg(?:\?[0-9a-zA-Z_=&-]*)?', img, html)

    return html

# ─────────────────────────────────────────────────────────────
#  MAIN EXCEL PROCESSING WORKER
# ─────────────────────────────────────────────────────────────
def process_excel_to_html(excel_path: str, output_dir: str, log_callback, progress_callback, is_stopped_callback):
    """
    Reads Excel file and generates one HTML file per row using Column A (Title),
    Column C (Link, default https://portalbsc.github.io/let/sp.js), and Column D (Image).
    """
    if not os.path.exists(excel_path):
        log_callback(f"[ERROR] Excel file not found: {excel_path}", "red")
        return

    os.makedirs(output_dir, exist_ok=True)
    log_callback(f"[INFO] Opening Excel: {os.path.basename(excel_path)}", "blue")

    try:
        wb = openpyxl.load_workbook(excel_path, data_only=True)
        sheet = wb.active
    except Exception as e:
        log_callback(f"[ERROR] Failed to load Excel file: {e}", "red")
        return

    # Extract rows (skip header row)
    rows_to_process = []
    for row_idx, row in enumerate(sheet.iter_rows(values_only=True), start=1):
        if not row:
            continue
        col_a = str(row[0]).strip() if len(row) > 0 and row[0] is not None else ""
        col_b = str(row[1]).strip() if len(row) > 1 and row[1] is not None else ""
        col_c = str(row[2]).strip() if len(row) > 2 and row[2] is not None else ""
        col_d = str(row[3]).strip() if len(row) > 3 and row[3] is not None else ""

        # Check if header row
        if row_idx == 1 and (
            col_a.lower() in ["titel", "title"] or 
            col_b.lower() in ["body", "content"] or 
            col_c.lower() in ["link", "url", "script"] or
            col_d.lower() in ["image", "images", "img", "photo", "picture"]
        ):
            continue

        if col_a:
            rows_to_process.append((row_idx, col_a, col_c, col_d))

    total = len(rows_to_process)
    if total == 0:
        log_callback("[WARNING] No data rows found in Column A of Excel sheet!", "orange")
        return

    log_callback(f"[INFO] Found {total} title row(s) to process.", "blue")
    log_callback(f"[INFO] Script Link: Column C (Fixed/Default: {DEFAULT_SCRIPT_LINK})", "darkgreen")

    success_count = 0
    fail_count = 0

    for idx, (row_idx, title, link, col_img) in enumerate(rows_to_process, start=1):
        if is_stopped_callback():
            log_callback("[STOPPED] Process stopped by user.", "orange")
            break

        safe_title = title.encode("ascii", "replace").decode("ascii")
        log_callback(f"\n[{idx}/{total}] Row #{row_idx}: {safe_title[:65]}...", "darkblue")

        try:
            # 1. Script link selection (Column C or Fixed default)
            active_link = link if link else DEFAULT_SCRIPT_LINK

            # 2. Image selection (Column D or default template image)
            final_image = ""
            if col_img:
                clean_img = col_img.strip().strip('"').strip("'")
                if os.path.exists(clean_img) and os.path.isfile(clean_img):
                    final_image = prepare_image_for_html(clean_img, output_dir)
                    log_callback(f"  -> Image: Converted local file {os.path.basename(clean_img)} to Base64", "blue")
                else:
                    final_image = clean_img
                    log_callback(f"  -> Image: Using Column D URL", "blue")

            # 3. Generate HTML with updated title and script link
            html_output = build_html_content(raw_title=title, custom_link=active_link, image_url=final_image)

            # 4. Generate clean filename slug
            filename = generate_file_slug(title)
            output_file_path = os.path.join(output_dir, filename)

            # Avoid overwriting duplicates by adding index
            counter = 1
            base_name, ext = os.path.splitext(filename)
            while os.path.exists(output_file_path):
                output_file_path = os.path.join(output_dir, f"{base_name}_{counter}{ext}")
                counter += 1

            # 5. Save HTML File
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(html_output)

            success_count += 1
            log_callback(f"  -> Created: {os.path.basename(output_file_path)}", "darkgreen")

        except Exception as ex:
            fail_count += 1
            log_callback(f"  -> Error row #{row_idx}: {ex}", "red")

        # Update progress bar
        progress_callback(int((idx / total) * 100), success_count, fail_count, total)
        time.sleep(0.05)

    log_callback(f"\n========================================", "blue")
    log_callback(f"[COMPLETED] Total: {total} | Success: {success_count} | Failed: {fail_count}", "darkgreen" if fail_count == 0 else "orange")
    log_callback(f"Output Directory: {output_dir}", "blue")

# ─────────────────────────────────────────────────────────────
#  TKINTER DESKTOP GUI APPLICATION
# ─────────────────────────────────────────────────────────────
class HTMLMakerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HTML Make Generator (Fixed Script & Auto Title)")
        self.geometry("820x680")
        self.minsize(700, 550)
        self.configure(bg="#F4F6F9")

        self.config_data = load_config()
        self.is_running = False
        self.stop_requested = False

        self._init_ui()

    def _init_ui(self):
        # Header Banner
        header = tk.Frame(self, bg="#1E293B", height=70)
        header.pack(fill=tk.X, side=tk.TOP)
        
        title_lbl = tk.Label(header, text="HTML Make Generator", font=("Segoe UI", 16, "bold"), fg="#FFFFFF", bg="#1E293B")
        title_lbl.pack(anchor="w", padx=20, pady=(12, 2))
        
        sub_lbl = tk.Label(header, text=f"Excel Column A = Title | Column C = Link (Fixed: {DEFAULT_SCRIPT_LINK})", font=("Segoe UI", 9), fg="#94A3B8", bg="#1E293B")
        sub_lbl.pack(anchor="w", padx=20, pady=(0, 10))

        # Main Container
        main_frame = tk.Frame(self, bg="#F4F6F9")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # File Selection Card
        card = tk.LabelFrame(main_frame, text=" Configuration ", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#334155", padx=15, pady=12)
        card.pack(fill=tk.X, pady=(0, 15))

        # Excel Row
        tk.Label(card, text="Excel File (.xlsx):", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#475569").grid(row=0, column=0, sticky="w", pady=6)
        self.excel_var = tk.StringVar(value=self.config_data.get("excel_path", DEFAULT_EXCEL))
        excel_entry = tk.Entry(card, textvariable=self.excel_var, font=("Segoe UI", 9), bg="#F8FAFC", relief=tk.SOLID, bd=1)
        excel_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=6)
        tk.Button(card, text="Browse...", command=self._browse_excel, font=("Segoe UI", 9), bg="#E2E8F0", relief=tk.GROOVE, padx=10).grid(row=0, column=2, pady=6)

        # Output Row
        tk.Label(card, text="Output Folder:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#475569").grid(row=1, column=0, sticky="w", pady=6)
        self.output_var = tk.StringVar(value=self.config_data.get("output_dir", DEFAULT_OUTPUT_DIR))
        output_entry = tk.Entry(card, textvariable=self.output_var, font=("Segoe UI", 9), bg="#F8FAFC", relief=tk.SOLID, bd=1)
        output_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=6)
        
        btn_frame = tk.Frame(card, bg="#FFFFFF")
        btn_frame.grid(row=1, column=2, pady=6)
        tk.Button(btn_frame, text="Browse...", command=self._browse_output, font=("Segoe UI", 9), bg="#E2E8F0", relief=tk.GROOVE, padx=6).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Open Output", command=self._open_output, font=("Segoe UI", 9), bg="#E2E8F0", relief=tk.GROOVE, padx=6).pack(side=tk.LEFT, padx=2)

        card.columnconfigure(1, weight=1)

        # Control & Progress Frame
        ctrl_frame = tk.Frame(main_frame, bg="#F4F6F9")
        ctrl_frame.pack(fill=tk.X, pady=(0, 10))

        self.start_btn = tk.Button(ctrl_frame, text="Start HTML Make", command=self._start_process, font=("Segoe UI", 11, "bold"), bg="#2563EB", fg="#FFFFFF", activebackground="#1D4ED8", activeforeground="#FFFFFF", relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_btn = tk.Button(ctrl_frame, text="Stop", command=self._stop_process, font=("Segoe UI", 10, "bold"), bg="#EF4444", fg="#FFFFFF", activebackground="#DC2626", activeforeground="#FFFFFF", relief=tk.FLAT, padx=15, pady=8, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT)

        self.status_lbl = tk.Label(ctrl_frame, text="Ready", font=("Segoe UI", 9, "bold"), bg="#F4F6F9", fg="#64748B")
        self.status_lbl.pack(side=tk.RIGHT, pady=8)

        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, mode="determinate")
        self.progress.pack(fill=tk.X, pady=(0, 10))

        # Log Console Card
        log_card = tk.LabelFrame(main_frame, text=" Real-Time Process Logs ", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#334155", padx=10, pady=10)
        log_card.pack(fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(log_card, font=("Consolas", 9), bg="#0F172A", fg="#F8FAFC", relief=tk.FLAT, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(log_card, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Log color tags
        self.log_text.tag_config("red", foreground="#F87171")
        self.log_text.tag_config("green", foreground="#4ADE80")
        self.log_text.tag_config("darkgreen", foreground="#22C55E")
        self.log_text.tag_config("blue", foreground="#60A5FA")
        self.log_text.tag_config("darkblue", foreground="#93C5FD")
        self.log_text.tag_config("orange", foreground="#FBBF24")
        self.log_text.tag_config("gray", foreground="#94A3B8")

        self.log("[READY] HTML Make Generator is ready. Click 'Start HTML Make' to run.", "blue")
        self.log(f"[INFO] Script link is fixed to: {DEFAULT_SCRIPT_LINK} (or Column C if provided)", "gray")

    def log(self, message: str, color_tag=""):
        self.log_text.config(state=tk.NORMAL)
        if color_tag:
            self.log_text.insert(tk.END, message + "\n", color_tag)
        else:
            self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _browse_excel(self):
        f = filedialog.askopenfilename(title="Select HTML MAKE Excel File", filetypes=[("Excel Files", "*.xlsx *.xls")])
        if f:
            self.excel_var.set(f)
            self._save_paths()

    def _browse_output(self):
        d = filedialog.askdirectory(title="Select Output Folder")
        if d:
            self.output_var.set(d)
            self._save_paths()

    def _open_output(self):
        d = self.output_var.get().strip()
        if os.path.exists(d):
            os.startfile(d)
        else:
            messagebox.showinfo("Notice", f"Directory does not exist yet:\n{d}")

    def _save_paths(self):
        save_config({
            "excel_path": self.excel_var.get().strip(),
            "output_dir": self.output_var.get().strip()
        })

    def _start_process(self):
        if self.is_running:
            return

        excel_path = self.excel_var.get().strip()
        output_dir = self.output_var.get().strip()

        if not excel_path or not os.path.exists(excel_path):
            messagebox.showerror("Error", f"Excel file does not exist:\n{excel_path}")
            return

        self._save_paths()
        self.is_running = True
        self.stop_requested = False
        self.start_btn.config(state=tk.DISABLED, bg="#94A3B8")
        self.stop_btn.config(state=tk.NORMAL)
        self.progress["value"] = 0
        self.status_lbl.config(text="Processing...", fg="#2563EB")

        threading.Thread(target=self._worker_thread, args=(excel_path, output_dir), daemon=True).start()

    def _stop_process(self):
        if self.is_running:
            self.stop_requested = True
            self.status_lbl.config(text="Stopping...", fg="#EF4444")
            self.stop_btn.config(state=tk.DISABLED)

    def _worker_thread(self, excel_path, output_dir):
        def log_cb(msg, tag=""):
            self.after(0, self.log, msg, tag)

        def prog_cb(pct, success, fail, total):
            self.after(0, self._update_progress, pct, success, fail, total)

        def is_stop():
            return self.stop_requested

        process_excel_to_html(excel_path, output_dir, log_cb, prog_cb, is_stop)

        self.after(0, self._on_finished)

    def _update_progress(self, pct, success, fail, total):
        self.progress["value"] = pct
        self.status_lbl.config(text=f"Processed: {success + fail}/{total} (Success: {success}, Failed: {fail})", fg="#0F172A")

    def _on_finished(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL, bg="#2563EB")
        self.stop_btn.config(state=tk.DISABLED)
        self.status_lbl.config(text="Done / Ready", fg="#22C55E")

if __name__ == "__main__":
    app = HTMLMakerApp()
    app.mainloop()
