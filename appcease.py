import platform
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import psutil

class ProcessManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Manager")
        self.allow_update = True  # Initialize the allow_update attribute
        
        self.process_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=50)
        self.process_listbox.grid(row=0, column=0, padx=10, pady=10, rowspan=4, sticky="nsew")  # Span rows and expand both directions

        self.process_scrollbar_y = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.process_listbox.yview)
        self.process_listbox.config(yscrollcommand=self.process_scrollbar_y.set)
        self.process_scrollbar_y.grid(row=0, column=1, sticky="ns", rowspan=4, pady=10, ipadx=2)  # Span rows and adjust ipadx



        self.update_process_list()

        self.update_button = tk.Button(root, text="Update List", command=self.update_process_list_manually)
        self.update_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")  # Span columns

        self.schedule_label = tk.Label(root, text="Enter schedule time (HH:MM):")
        self.schedule_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")  # Align label to the left

        self.schedule_entry = tk.Entry(root)
        self.schedule_entry.grid(row=5, column=0, padx=10, pady=5, sticky="e")  # Align entry to the right

        self.schedule_button = tk.Button(root, text="Schedule Stop", command=self.schedule_process)
        self.schedule_button.grid(row=5, column=1, padx=10, pady=5, sticky="e")  # Align button to the right

        # Add the clock label and initialize it
        self.clock_label = tk.Label(root, text="", font=("Helvetica", 18))
        self.clock_label.grid(row=6, column=0, padx=10, pady=5, columnspan=2, sticky="e")  # Align clock to the right
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

    def schedule_process(self):
        selected_index = self.process_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select an application to schedule.")
            return

        selected_app = self.process_listbox.get(selected_index)
        pid = int(selected_app.split()[1])

        schedule_time = self.schedule_entry.get()
        try:
            hours, minutes = map(int, schedule_time.split(":"))
            now = datetime.now()
            scheduled_time = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)
            if scheduled_time < now:
                scheduled_time += timedelta(days=1)  # Schedule for the next day if the time has passed

            time_difference = scheduled_time - now 
            time_difference = int(time_difference.total_seconds() * 1000)
            self.root.after(time_difference, lambda: self.stop_process(pid))
            messagebox.showinfo("Scheduled", f"Application {pid} has been scheduled to stop at {scheduled_time}.")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")

    def stop_process(self, pid):
        try:
            process = psutil.Process(pid)
            process.terminate()
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

# TODO: search option - multiple program killer - feedback when prgram is killed - reset input field when program is killed
