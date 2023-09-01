import platform
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import psutil

class ProcessManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AppCease")
        self.allow_update = True  # Initialize the allow_update attribute

        self.process_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50)
        self.process_listbox.grid(row=0, column=0, padx=10, pady=10, rowspan=4, sticky="nsew")  # Span rows and expand both directions

        self.process_scrollbar_y = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.process_listbox.yview)
        self.process_listbox.config(yscrollcommand=self.process_scrollbar_y.set)
        self.process_scrollbar_y.grid(row=0, column=1, sticky="ns", rowspan=4, pady=10, ipadx=2)  # Span rows and adjust ipadx

        self.search_label = tk.Label(root, text="Search:")
        self.search_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")  # Align label to the left

        self.search_entry = tk.Entry(root)
        self.search_entry.grid(row=4, column=0, padx=10, pady=5, sticky="ew")  # Align entry to the right
        self.search_entry.bind('<KeyRelease>', self.update_search)

        self.update_process_list()

        self.update_button = tk.Button(root, text="Update List", command=self.update_process_list_manually)
        self.update_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")  # Span columns

        self.schedule_label = tk.Label(root, text="Enter schedule time (HH:MM):")
        self.schedule_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")  # Align label to the left

        self.schedule_entry = tk.Entry(root)
        self.schedule_entry.grid(row=6, column=0, padx=10, pady=5, sticky="ew")  # Align entry to the right

        self.schedule_selected_button = tk.Button(root, text="Schedule Selected", command=self.schedule_selected_processes)
        self.schedule_selected_button.grid(row=6, column=1, padx=10, pady=5, sticky="e")  # Align button to the right

        # Add the clock label and initialize it
        self.clock_label = tk.Label(root, text="", font=("Helvetica", 18))
        self.clock_label.grid(row=7, column=0, padx=10, pady=5, columnspan=2, sticky="e")  # Align clock to the right
        self.update_clock()  # Initialize the clock

        self.process_listbox.bind('<<ListboxSelect>>', self.toggle_update)

    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)  # Update every 1 second

    def toggle_update(self, event):
        self.allow_update = not self.allow_update

    def update_process_list(self):
        if self.allow_update:
            applications = self.get_user_applications()
            self.process_listbox.delete(0, tk.END)
            for app in applications:
                self.process_listbox.insert(tk.END, app)

        # self.root.after(1000, self.update_process_list)  # Update every 1 second

    def update_process_list_manually(self):
        self.allow_update = True
        self.update_process_list()

    def get_user_applications(self):
        applications = []
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            try:
                process = psutil.Process(proc.info['pid'])
                if process.exe() and "python" not in process.exe().lower():  # Exclude this Python script
                    applications.append(f"PID: {proc.info['pid']} - Name: {process.name()}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return applications

    def update_search(self, event):
        search_keyword = self.search_entry.get().lower()
        applications = self.get_user_applications()
        self.process_listbox.delete(0, tk.END)
        for app in applications:
            if search_keyword in app.lower():
                self.process_listbox.insert(tk.END, app)

    def schedule_selected_processes(self):
        selected_indices = self.process_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select at least one application to schedule.")
            return

        selected_pids = [int(self.process_listbox.get(index).split()[1]) for index in selected_indices]
        schedule_time = self.schedule_entry.get()
        try:
            hours, minutes = map(int, schedule_time.split(":"))
            now = datetime.now()
            scheduled_time = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)
            if scheduled_time < now:
                scheduled_time += timedelta(days=1)  # Schedule for the next day if the time has passed

            time_difference = scheduled_time - now
            time_difference = int(time_difference.total_seconds() * 1000)

            for pid in selected_pids:
                self.root.after(time_difference, lambda p=pid: self.stop_process(p))

            messagebox.showinfo("Scheduled", f"Selected applications will be terminated at {scheduled_time}.")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")

    def stop_process(self, pid):
        try:
            process = psutil.Process(pid)
            process.terminate()
            messagebox.showinfo("Killed", "Terminated!")
        except psutil.NoSuchProcess:
            pass

def main():
    if platform.system() == "Windows" or platform.system() == "Linux":
        root = tk.Tk()
        app = ProcessManagerApp(root)
        root.mainloop()
    else:
        print("This script supports Windows and Linux only.")

if __name__ == "__main__":
    main()
