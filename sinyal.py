import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ---------------- Fungsi bikin rounded rectangle ----------------
def create_rounded_rect(canvas, x1, y1, x2, y2, r=20, **kwargs):
    points = [
        x1+r, y1,
        x2-r, y1,
        x2, y1,
        x2, y1+r,
        x2, y2-r,
        x2, y2,
        x2-r, y2,
        x1+r, y2,
        x1, y2,
        x1, y2-r,
        x1, y1+r,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# ---------------- Halaman Welcome ----------------
class WelcomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome Page")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.original_image = Image.open("asset/Background_.png")
        self.bg_photo = None

        self.resize_job = None
        self.update_background()
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        if self.resize_job:
            self.root.after_cancel(self.resize_job)
        # delay 200ms supaya tidak redraw terus
        self.resize_job = self.root.after(200, self.update_background)

    def update_background(self):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        if w > 1 and h > 1:
            resized = self.original_image.resize((w, h), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized)

            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

            box_w, box_h = 320, 80
            x_box, y_box = w * 0.6, h * 0.3
            create_rounded_rect(
                self.canvas,
                x_box - box_w//2, y_box - box_h//2,
                x_box + box_w//2, y_box + box_h//2,
                r=20, fill="#e6e6e6", outline=""
            )
            self.canvas.create_text(x_box, y_box,
                                    text="Konversi Signal Encoding",
                                    font=("Helvetica", 16, "bold"),
                                    fill="black")

            create_button = tk.Button(self.root, text="create",
                                      font=("Helvetica", 12, "bold"),
                                      bg="#4e2c1e", fg="white",
                                      width=10, command=self.next_page,
                                      relief="flat", bd=0)
            self.canvas.create_window(x_box, y_box + 80, window=create_button)

            about_button = tk.Button(self.root, text="About Us",
                                     font=("Helvetica", 12, "bold"),
                                     bg="#fbc97f", fg="black",
                                     width=10, command=self.about_page,
                                     relief="flat", bd=0)
            self.canvas.create_window(w - 100, h - 50, window=about_button)

    def next_page(self):
        self.canvas.destroy()
        KonversiPage(self.root)

    def about_page(self):
        messagebox.showinfo("About Us", "Aplikasi Konversi Sinyal Encoding\nDibuat dengan Tkinter")


# ---------------- Halaman Input 5 Digit ----------------
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class KonversiPage:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.original_image = Image.open("asset/tampilan.png")
        self.bg_photo = None

        self.resize_job = None
        self.update_background()
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        if self.resize_job:
            self.root.after_cancel(self.resize_job)
        self.resize_job = self.root.after(200, self.update_background)

    def update_background(self):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        if w > 1 and h > 1:
            resized = self.original_image.resize((w, h), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized)

            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

            # --- Kotak semi transparan di tengah ---
            box_w, box_h = 350, 220
            x_box, y_box = w // 2, h // 2
            self.canvas.create_rectangle(
                x_box - box_w//2, y_box - box_h//2,
                x_box + box_w//2, y_box + box_h//2,
                fill="#f9f9f9", outline="#cccccc", width=2
            )

            # --- Label judul ---
            label = tk.Label(
                self.root, text="Masukkan 5 Digit Angka",
                font=("Helvetica", 14, "bold"),
                bg="#f9f9f9", fg="#333333"
            )
            self.canvas.create_window(x_box, y_box - 60, window=label)

            # --- Input field ---
            self.entry = tk.Entry(
                self.root, font=("Helvetica", 14),
                justify="center", bg="#ffffff", fg="#000000",
                relief="solid", bd=1
            )
            self.canvas.create_window(x_box, y_box - 20, window=self.entry, width=200, height=35)

            # --- Tombol Generate ---
            generate_btn = tk.Button(
                self.root, text="Generate",
                font=("Helvetica", 12, "bold"),
                bg="#4e2c1e", fg="white",
                relief="flat", padx=10, pady=5,
                command=self.check_input
            )
            self.canvas.create_window(x_box, y_box + 30, window=generate_btn, width=120, height=35)

            # --- Tombol Back ---
            back_btn = tk.Button(
                self.root, text="Back",
                font=("Helvetica", 12, "bold"),
                bg="#fbc97f", fg="black",
                relief="flat", padx=10, pady=5,
                command=self.back_to_welcome
            )
            self.canvas.create_window(x_box, y_box + 80, window=back_btn, width=120, height=35)

    def check_input(self):
        value = self.entry.get().strip()
        if value.isdigit() and len(value) == 5:
            messagebox.showinfo("Sukses", f"Input valid: {value}")
        else:
            messagebox.showerror("Error", "Harus 5 Digit")

    def back_to_welcome(self):
        self.canvas.destroy()
        WelcomePage(self.root)  # pastikan WelcomePage sudah didefinisikan

# ---------------- Main ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = WelcomePage(root)
    root.mainloop()
