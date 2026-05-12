import customtkinter as ctk
import math
import time

# Theme: Deep Blue & Gold (Professional Engineering Look)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

class SalehaProEngineerCalc(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Saleha Engineering Master v3.0")
        self.geometry("460x820") 
        self.resizable(False, False)

        self.data_input = ""
        self.vaani = ctk.StringVar()
        self.mode = "DEG" 

        self.setup_ui()
        self.bind("<Key>", self.keyboard_logic)

    def setup_ui(self):
        # Premium Glass-morphism style Frame
        self.main_container = ctk.CTkFrame(self, fg_color="#0a192f", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        # Header Info
        self.info_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.info_frame.pack(fill="x", padx=20, pady=(15, 0))

        self.mode_tag = ctk.CTkLabel(self.info_frame, text="ENG MODE", font=("Consolas", 11, "bold"), text_color="#64ffda")
        self.mode_tag.pack(side="left")

        self.time_tag = ctk.CTkLabel(self.info_frame, text="", font=("Consolas", 11), text_color="#8892b0")
        self.time_tag.pack(side="right")
        self.update_time()

        # Luxury Display
        self.display = ctk.CTkEntry(self.main_container, textvariable=self.vaani, font=("Digital-7", 48) if self.is_font_installed("Digital-7") else ("Arial", 42, "bold"),
                                   height=110, corner_radius=15, fg_color="#112240", 
                                   text_color="#64ffda", border_color="#233554", border_width=2, justify="right")
        self.display.pack(pady=25, padx=20, fill="x")

        # Control Panel (Tabs)
        self.tool_tabs = ctk.CTkTabview(self.main_container, fg_color="#112240", segmented_button_selected_color="#64ffda",
                                       segmented_button_selected_hover_color="#52d1b2",
                                       segmented_button_unselected_color="#233554")
        self.tool_tabs.pack(padx=15, pady=10, fill="both", expand=True)
        
        tab_math = self.tool_tabs.add("Standard")
        tab_eng = self.tool_tabs.add("Advanced")

        # Layouts
        math_layout = [
            ['CLR', 'DEL', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['RAD/DEG', '0', '.', '=']
        ]

        eng_layout = [
            ['sin', 'cos', 'tan', 'sqrt'],
            ['log', 'ln', 'exp', '^'],
            ['(', ')', 'pi', 'e'],
            ['x²', 'x³', 'fact', 'abs'],
            ['CLR', 'DEL', '0', '=']
        ]

        self.generate_buttons(tab_math, math_layout)
        self.generate_buttons(tab_eng, eng_layout)

    def generate_buttons(self, parent, schema):
        for r, row in enumerate(schema):
            for c, txt in enumerate(row):
                # Custom Color Logic
                b_color = "#1d2d44"
                t_color = "#ccd6f6"
                
                if txt == "=": b_color = "#64ffda"; t_color = "#0a192f"
                elif txt in ["CLR", "DEL"]: t_color = "#f57d7d"
                elif not txt.isdigit() and txt not in [".", "RAD/DEG"]: t_color = "#64ffda"

                btn = ctk.CTkButton(parent, text=txt, width=90, height=60, corner_radius=8,
                                   fg_color=b_color, text_color=t_color, 
                                   hover_color="#233554",
                                   font=("Arial", 16, "bold"),
                                   command=lambda x=txt: self.engine_logic(x))
                btn.grid(row=r, column=c, padx=6, pady=6)

    def update_time(self):
        self.time_tag.configure(text=time.strftime("%H:%M"))
        self.after(1000, self.update_time)

    def is_font_installed(self, name):
        # Placeholder for font check logic
        return False

    def engine_logic(self, val):
        if val == "=":
            try:
                # Engineering conversion
                query = self.data_input.replace("pi", str(math.pi)).replace("e", str(math.e))
                query = query.replace("^", "**").replace("sqrt", "math.sqrt").replace("ln", "math.log")
                query = query.replace("exp", "math.exp").replace("abs", "math.fabs")
                
                # Dynamic Trig handling
                def trig(func, x):
                    angle = math.radians(x) if self.mode == "DEG" else x
                    return getattr(math, func)(angle)

                result = eval(query, {"math": math, "sin": lambda x: trig('sin', x), 
                                     "cos": lambda x: trig('cos', x), "tan": lambda x: trig('tan', x),
                                     "fact": math.factorial, "log": math.log10})
                
                final_res = f"{result:.8g}"
                self.vaani.set(final_res)
                self.data_input = str(final_res)
            except:
                self.vaani.set("SYNTAX ERROR")
                self.data_input = ""

        elif val == "CLR":
            self.data_input = ""
            self.vaani.set("")
        elif val == "DEL":
            self.data_input = self.data_input[:-1]
            self.vaani.set(self.data_input)
        elif val == "RAD/DEG":
            self.mode = "RAD" if self.mode == "DEG" else "DEG"
            self.mode_tag.configure(text=f"{self.mode} MODE")
        elif val == "x²": self.data_input += "**2"; self.engine_logic("=")
        elif val == "x³": self.data_input += "**3"; self.engine_logic("=")
        elif val in ["sin", "cos", "tan", "log", "ln", "sqrt", "fact", "abs"]:
            self.data_input += f"{val}("
            self.vaani.set(self.data_input)
        else:
            self.data_input += str(val)
            self.vaani.set(self.data_input)

    def keyboard_logic(self, event):
        if event.keysym == "Return": self.engine_logic("=")
        elif event.keysym == "BackSpace": self.engine_logic("DEL")
        elif event.char in "0123456789+-*/.()": self.engine_logic(event.char)

if __name__ == "__main__":
    app = SalehaProEngineerCalc()
    app.mainloop()