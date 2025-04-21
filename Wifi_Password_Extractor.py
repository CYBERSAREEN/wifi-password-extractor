from customtkinter import *
import subprocess as sb
import re

class WiFiPasswordExtractor:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x700")
        self.master.title("Wi-Fi Password Extractor")
        self.master.resizable(False, False)
        
        self.create_widgets()
    
    def create_widgets(self):
        self.main_frame = CTkFrame(self.master)
        self.main_frame.pack(padx=20, pady=20 ,fill = "both",expand = True)
        
        self.scroll_frame = CTkScrollableFrame(self.main_frame, width=600, height=350)
        self.scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        CTkButton(
            self.main_frame, 
            text="Show All Wi-Fi Profiles & Passwords", 
            command=self.show_profiles
        ).pack(pady=5)
        
        CTkButton(
            self.main_frame, 
            text="Clear Result", 
            command=self.clear_result
        ).pack(pady=5)
        
        CTkButton(
            self.main_frame, 
            text="Exit", 
            command=self.exit_app
        ).pack(pady=5)
    
    def show_profiles(self):
        
        try:
            
            self.clear_result()
            
            profiles_data = sb.check_output("netsh wlan show profiles", shell=True).decode()
            
            profiles = re.findall(r"All User Profile\s*:\s*(.*)", profiles_data)
            
            if not profiles:
               
                CTkLabel(
                    self.scroll_frame, 
                    text="No Wi-Fi profiles found.", 
                    font=("Arial", 14)
                ).pack(anchor="w", padx=10, pady=5)
                return
            
            for profile in profiles:
                try:
                   
                    details = sb.check_output(
                        f'netsh wlan show profile name="{profile}" key=clear', 
                        shell=True
                    ).decode()
                    
                    
                    password_match = re.search(r"Key Content\s*:\s*(.*)", details)
                    password = password_match.group(1) if password_match else "No password (Open Network)"
                    
                    CTkLabel(
                        self.scroll_frame, 
                        text=f"📶 Wifi Name (A.P): {profile}\n🔑 Password (Key Content):  {password}\n\n", 
                        font=("Arial", 15), 
                        justify="left", 
                        anchor="w", 
                        wraplength=600
                    ).pack(anchor="w", padx=10, pady=5)
                except Exception:
                    
                    CTkLabel(
                        self.scroll_frame, 
                        text=f"📶 {profile}\n❌ Error retrieving password", 
                        font=("Arial", 13), 
                        justify="left", 
                        anchor="w", 
                        wraplength=600
                    ).pack(anchor="w", padx=10, pady=5)
        
        except Exception as e:
            
            CTkLabel(
                self.scroll_frame, 
                text=f"❌ Failed to retrieve profiles.\n{e}", 
                font=("Arial", 13)
            ).pack(anchor="w", padx=10, pady=5)
    
    def clear_result(self):
       
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
    
    def exit_app(self):
        
        self.master.destroy()

if __name__ == "__main__":
    root = CTk()
    app = WiFiPasswordExtractor(root)
    root.mainloop()