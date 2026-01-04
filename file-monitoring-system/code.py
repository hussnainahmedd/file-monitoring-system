import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import os
from datetime import datetime
import hashlib
import json

class SimpleFileSystemMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 SIMPLE FILE SYSTEM MONITOR")
        self.root.geometry("1400x800")
       
        # Monitoring
        self.monitoring = False
        self.monitored_paths = []
        self.known_files = {}
       
        # Integrity - Bas yeh add kiya hai
        self.file_hashes = {}
       
        # Statistics
        self.events_count = 0
        self.file_changes = 0
        self.deleted_files = 0
        self.created_files = 0
        self.renamed_files = 0
       
        self.setup_gui()
        self.setup_default_paths()
   
    def setup_default_paths(self):
        """Setup default paths to monitor"""
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        documents = os.path.join(os.path.expanduser("~"), "Documents")
        downloads = os.path.join(os.path.expanduser("~"), "Downloads")
       
        self.monitored_paths = [desktop, documents, downloads]
       
        # Store initial file states
        for path in self.monitored_paths:
            if os.path.exists(path):
                self.scan_path(path)
   
    def scan_path(self, path):
        """Scan path and store file information"""
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        self.known_files[filepath] = {
                            'size': os.path.getsize(filepath),
                            'modified': os.path.getmtime(filepath),
                            'created': os.path.getctime(filepath)
                        }
                    except:
                        continue
        except:
            pass
   
    def setup_gui(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
       
        # Header
        header = tk.Label(main_frame, text="🔍 SIMPLE FILE SYSTEM MONITOR",
                         font=('Arial', 18, 'bold'), fg='#2c3e50')
        header.pack(pady=10)
       
        subtitle = tk.Label(main_frame,
                          text="No External Packages Required • Monitors File Changes • Real-time Alerts",
                          font=('Arial', 11), fg='#7f8c8d')
        subtitle.pack(pady=(0, 10))
       
        # Control Panel
        control_frame = ttk.LabelFrame(main_frame, text="🎛️ Monitoring Controls")
        control_frame.pack(fill=tk.X, pady=(0, 10))
       
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(pady=10)
       
        self.monitor_btn = tk.Button(btn_frame, text="🟢 Start System Monitoring",
                                   command=self.toggle_monitoring,
                                   font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                                   width=22, height=1)
        self.monitor_btn.pack(side=tk.LEFT, padx=5)
       
        tk.Button(btn_frame, text="📁 Add Folder",
                 command=self.add_folder, font=('Arial', 11),
                 bg='#3498db', fg='white', width=15).pack(side=tk.LEFT, padx=5)
       
        tk.Button(btn_frame, text="🧪 Create Test File",
                 command=self.create_test_file, font=('Arial', 11),
                 bg='#f39c12', fg='white', width=15).pack(side=tk.LEFT, padx=5)
       
        tk.Button(btn_frame, text="🧹 Clear Logs",
                 command=self.clear_logs, font=('Arial', 11),
                 bg='#95a5a6', fg='white', width=12).pack(side=tk.LEFT, padx=5)
       
        # Statistics Frame
        stats_frame = ttk.LabelFrame(main_frame, text="📊 Live Statistics")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
       
        stats_inner = ttk.Frame(stats_frame)
        stats_inner.pack(fill=tk.X, padx=10, pady=10)
       
        self.stats_labels = {}
        stats_data = [
            ("📈 Total Events", "total_events", "0"),
            ("📝 File Changes", "file_changes", "0"),
            ("🆕 Files Created", "files_created", "0"),
            ("🗑️ Files Deleted", "files_deleted", "0")
        ]
       
        for text, key, value in stats_data:
            frame = ttk.Frame(stats_inner)
            frame.pack(side=tk.LEFT, expand=True)
           
            lbl = tk.Label(frame, text=text, font=('Arial', 10), fg='#7f8c8d')
            lbl.pack()
           
            value_lbl = tk.Label(frame, text=value, font=('Arial', 14, 'bold'), fg='#2c3e50')
            value_lbl.pack()
           
            self.stats_labels[key] = value_lbl
       
        # Main Content
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
       
        # Left - Monitored Paths
        left_frame = ttk.LabelFrame(content_frame, text="📁 Monitored Folders")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
       
        self.paths_text = scrolledtext.ScrolledText(left_frame, font=('Consolas', 9), height=15)
        self.paths_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
       
        # Right - Event Logs
        right_frame = ttk.LabelFrame(content_frame, text="📋 System Events Log (Real-time)")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
       
        self.logs_text = scrolledtext.ScrolledText(right_frame, font=('Consolas', 9), height=15)
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
       
        # Status bar
        self.status_var = tk.StringVar(value="🔴 System Monitoring Stopped")
        status_bar = tk.Label(main_frame, textvariable=self.status_var,
                            font=('Arial', 10, 'bold'), fg='#e74c3c')
        status_bar.pack(fill=tk.X, pady=(5, 0))
       
        # Update paths display
        self.update_paths_display()
   
    def update_paths_display(self):
        """Update monitored paths display"""
        self.paths_text.delete(1.0, tk.END)
       
        for path in self.monitored_paths:
            if os.path.exists(path):
                status = "✅ Monitoring"
                file_count = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
            else:
                status = "❌ Not Found"
                file_count = 0
           
            display_text = f"{os.path.basename(path)}:\n"
            display_text += f"  Path: {path}\n"
            display_text += f"  Status: {status}\n"
            display_text += f"  Files: {file_count}\n"
            display_text += "-" * 50 + "\n"
           
            self.paths_text.insert(tk.END, display_text)
   
    def calculate_file_hash(self, filepath):
        """Bas yeh function add kiya hai - file ka hash calculate karta hai"""
        if not os.path.exists(filepath):
            return None
        try:
            with open(filepath, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except:
            return None
   
    def check_integrity(self, filepath):
        """Bas yeh function add kiya hai - integrity check karta hai"""
        current_hash = self.calculate_file_hash(filepath)
       
        if filepath in self.file_hashes:
            if self.file_hashes[filepath] == current_hash:
                return True, "✅ Hash match - No changes"
            else:
                return False, "🚨 HASH CHANGED - File modified!"
        else:
            # Pehli baar file dekhi hai, hash store karo
            if current_hash:
                self.file_hashes[filepath] = current_hash
            return True, "🔐 New file - Hash stored"
   
    def log_event(self, event_type, file_path, details=""):
        """Add event to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        filename = os.path.basename(file_path)
       
        log_entry = f"[{timestamp}] {event_type}: {filename}\n"
        log_entry += f"    Path: {file_path}\n"
        log_entry += f"    Details: {details}\n"
       
        # BAS YEH LINE ADD KI HAI - Integrity check for modified files
        if event_type == "MODIFIED":
            integrity_ok, integrity_msg = self.check_integrity(file_path)
            log_entry += f"    Integrity Check: {integrity_msg}\n"
           
            if not integrity_ok:
                # Alert show karo agar hash change hua hai
                messagebox.showwarning(
                    "🚨 HASH CHANGED!",
                    f"File integrity compromised!\n\n"
                    f"File: {filename}\n"
                    f"Path: {file_path}\n\n"
                    f"The file's hash has changed!",
                    parent=self.root
                )
       
        log_entry += "-" * 80 + "\n"
       
        # Color coding
        if event_type in ["DELETED", "TAMPERED"]:
            self.logs_text.insert(tk.END, log_entry)
            # Apply red color
            self.logs_text.tag_add("critical", "end-4l", "end-1l")
            self.logs_text.tag_config("critical", foreground='red')
        elif event_type in ["CREATED", "RENAMED"]:
            self.logs_text.insert(tk.END, log_entry)
            self.logs_text.tag_add("warning", "end-4l", "end-1l")
            self.logs_text.tag_config("warning", foreground='orange')
        elif event_type == "MODIFIED":
            self.logs_text.insert(tk.END, log_entry)
            self.logs_text.tag_add("info", "end-4l", "end-1l")
            self.logs_text.tag_config("info", foreground='blue')
        else:
            self.logs_text.insert(tk.END, log_entry)
       
        self.logs_text.see(tk.END)
       
        # Update statistics
        self.events_count += 1
        self.stats_labels['total_events'].config(text=str(self.events_count))
       
        if event_type == "MODIFIED":
            self.file_changes += 1
            self.stats_labels['file_changes'].config(text=str(self.file_changes))
        elif event_type == "CREATED":
            self.created_files += 1
            self.stats_labels['files_created'].config(text=str(self.created_files))
        elif event_type == "DELETED":
            self.deleted_files += 1
            self.stats_labels['files_deleted'].config(text=str(self.deleted_files))
   
    def monitor_files(self):
        """Main file monitoring loop"""
        self.log_event("SYSTEM", "Monitoring", "Started file system monitoring")
       
        check_count = 0
        while self.monitoring:
            try:
                current_files = {}
               
                # Scan all monitored paths
                for path in self.monitored_paths:
                    if os.path.exists(path):
                        for root, dirs, files in os.walk(path):
                            for file in files:
                                filepath = os.path.join(root, file)
                                try:
                                    current_files[filepath] = {
                                        'size': os.path.getsize(filepath),
                                        'modified': os.path.getmtime(filepath),
                                        'created': os.path.getctime(filepath)
                                    }
                                   
                                    # Check if file is new
                                    if filepath not in self.known_files:
                                        self.log_event("CREATED", filepath, "New file detected")
                                   
                                    # Check if file is modified
                                    elif (self.known_files[filepath]['modified'] !=
                                          current_files[filepath]['modified']):
                                        self.log_event("MODIFIED", filepath, "File content changed")
                                   
                                    # Check if file size changed
                                    elif (self.known_files[filepath]['size'] !=
                                          current_files[filepath]['size']):
                                        self.log_event("MODIFIED", filepath, "File size changed")
                                       
                                except Exception as e:
                                    continue
               
                # Check for deleted files
                for old_file in self.known_files:
                    if old_file not in current_files:
                        self.log_event("DELETED", old_file, "File deleted from system")
               
                # Update known files
                self.known_files = current_files
               
                # Update display every 10 cycles
                if check_count % 10 == 0:
                    self.update_paths_display()
               
                check_count += 1
                time.sleep(3)  # Check every 3 seconds
               
            except Exception as e:
                self.log_event("ERROR", "Monitoring", f"Error: {str(e)}")
                time.sleep(5)
   
    def toggle_monitoring(self):
        """Start/stop monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_btn.config(text="🔴 Stop Monitoring", bg='#e74c3c')
            self.status_var.set("🟢 Monitoring Active - Watching for file changes")
           
            # Start monitoring thread
            monitor_thread = threading.Thread(target=self.monitor_files, daemon=True)
            monitor_thread.start()
           
        else:
            self.monitoring = False
            self.monitor_btn.config(text="🟢 Start System Monitoring", bg='#27ae60')
            self.status_var.set("🔴 Monitoring Stopped")
            self.log_event("SYSTEM", "Monitoring", "Monitoring stopped")
   
    def add_folder(self):
        """Add a folder to monitor"""
        folder_path = filedialog.askdirectory(title="Select folder to monitor")
        if folder_path and folder_path not in self.monitored_paths:
            self.monitored_paths.append(folder_path)
            self.scan_path(folder_path)
            self.update_paths_display()
            self.log_event("SYSTEM", folder_path, "Added to monitoring")
   
    def create_test_file(self):
        """Create a test file to demonstrate monitoring"""
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        test_file = os.path.join(desktop, f"test_file_{int(time.time())}.txt")
       
        try:
            with open(test_file, 'w') as f:
                f.write(f"Test file created at {datetime.now()}\n")
                f.write("This file is being monitored for changes!\n")
           
            self.log_event("TEST", test_file, "Test file created - should appear in logs")
           
        except Exception as e:
            self.log_event("ERROR", "Test", f"Could not create test file: {e}")
   
    def clear_logs(self):
        """Clear all logs"""
        self.logs_text.delete(1.0, tk.END)
       
        # Reset counters
        self.events_count = 0
        self.file_changes = 0
        self.deleted_files = 0
        self.created_files = 0
       
        for label in self.stats_labels.values():
            label.config(text="0")
       
        self.log_event("SYSTEM", "Logs", "All logs cleared")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleFileSystemMonitor(root)
    root.mainloop()
