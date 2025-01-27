import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os

class GameEngine:
    def __init__(self):
        self.running = True
        self.current_scene = None

    def change_scene(self, scene):
        self.current_scene = scene

    def run(self):
        while self.running:
            if self.current_scene:
                self.current_scene.update()  # Güncelleme çağrısı
                self.current_scene.render()   # Render çağrısı
            time.sleep(0.01)  # Oyun döngüsünü yavaşlat

class CodeEditor:
    def __init__(self, engine):
        self.engine = engine
        self.root = tk.Tk()
        self.root.title("Oyun Motoru - Kod Editörü")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E2E2E")

        # Metin alanı
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier New", 12), bg="#1E1E1E", fg="#D4D4D4", insertbackground='white')
        self.text_area.pack(expand=True, fill='both')

        # Satır numaraları
        self.line_numbers = tk.Text(self.root, width=4, bg="#2E2E2E", fg="#D4D4D4", font=("Courier New", 12), padx=3, pady=3)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_area.bind("<KeyRelease>", self.update_line_numbers)
        self.text_area.bind("<KeyRelease>", self.on_key_release)

        # Çalıştır butonu
        self.run_button = tk.Button(self.root, text="▶", command=self.run_code, font=("Arial", 16), bg="#4CAF50", fg="white", width=3)
        self.run_button.pack(side=tk.TOP, anchor='ne', padx=10, pady=10)

        # Terminal alanı
        self.output_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier New", 12), bg="#1E1E1E", fg="#D4D4D4", insertbackground='white', height=10)
        self.output_area.pack(expand=True, fill='x')

        # Otomatik tamamlama için öneriler
        self.suggestions = ["def", "class", "import", "from", "as", "if", "else", "elif", "for", "while", "return", "print"]

    def update(self):
        # Oyun döngüsü sırasında yapılacak güncellemeler
        pass  # Buraya güncellemeleri ekleyebilirsiniz

    def render(self):
        # Ekranı güncellemek için kullanılacak
        self.root.update_idletasks()
        self.root.update()

    def on_key_release(self, event):
        if event.char.isalnum() or event.char in ['_', ' ']:
            self.update_suggestions()
        if event.keysym == "Return":  # Enter tuşuna basıldığında
            self.insert_function_template()
        if event.keysym == "parenleft":  # ( tuşuna basıldığında
            self.insert_parentheses()

    def update_suggestions(self):
        typed_text = self.text_area.get("1.0", tk.END).strip().split()[-1]
        self.suggestion_box.delete(0, tk.END)

        for word in self.suggestions:
            if word.startswith(typed_text):
                self.suggestion_box.insert(tk.END, word)

        if self.suggestion_box.size() > 0:
            self.suggestion_box.place(x=10, y=self.text_area.winfo_height() - 100)
        else:
            self.suggestion_box.place_forget()

    def insert_function_template(self):
        # Kullanıcı "def" yazdıysa otomatik olarak fonksiyon şablonu ekle
        current_text = self.text_area.get("1.0", tk.END).strip()
        if current_text.endswith("def "):
            function_name = "function_name"  # Burada kullanıcıdan fonksiyon adı alabilirsiniz
            template = f"def {function_name}():\n    pass\n"
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, template)

    def insert_parentheses(self):
        # Kullanıcı ( yazdığında otomatik olarak () ekle
        current_text = self.text_area.get("1.0", tk.END).strip()
        if current_text.endswith("("):
            self.text_area.insert(tk.END, ")")  # ) ekle
            self.text_area.mark_set("insert", "end-2c")  # İmleci ( işaretinin öncesine yerleştir

    def update_line_numbers(self, event=None):
        line_count = int(self.text_area.index('end-1c').split('.')[0])
        self.line_numbers.delete(1.0, tk.END)
        for i in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f"{i}\n")

    def run_code(self):
        code = self.text_area.get("1.0", tk.END).strip()
        if code:
            with open("temp_script.py", "w") as f:
                f.write(code)

            result = subprocess.run(["python", "temp_script.py"], capture_output=True, text=True)

            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, "Çıktı:\n")
            self.output_area.insert(tk.END, result.stdout)
            self.output_area.insert(tk.END, "Hata:\n")
            self.output_area.insert(tk.END, result.stderr)

            os.remove("temp_script.py")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    engine = GameEngine()
    editor = CodeEditor(engine)
    engine.change_scene(editor)
    editor.run()