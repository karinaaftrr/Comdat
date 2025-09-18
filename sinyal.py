import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def keseluruhan_konversi(digits):
    return format(int(digits), 'b')

def gambar_encoding(binary, opsi, ax):
    Tb = 0.5      
    N = 100        
    total_time = len(binary) * Tb
    t = np.linspace(0, total_time, len(binary) * N)
    signal = np.zeros_like(t)

    if opsi == 1: # Digital
        for i, bit in enumerate(binary):
            signal[i*N:(i+1)*N] = 1 if bit == '1' else 0
        ax.step(t, signal, where="post")
        ax.set_ylim(0.0, 1.05)
        ax.set_title("Digital Signal")

    elif opsi == 2: # Analog
        f = 5
        signal = np.sin(2*np.pi*f*t)
        ax.plot(t, signal)
        ax.set_title("Analog Signal")

    elif opsi == 3: # AM
        fc = 10
        for i, bit in enumerate(binary):
            tt = t[i*N:(i+1)*N]
            if bit == '1':
                signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*(tt - tt[0]))
            else:
                signal[i*N:(i+1)*N] = 0
        ax.plot(t, signal)
        ax.set_title("Amplitude Modulation (AM)")

    elif opsi == 4: # FM
        cycles_0, cycles_1 = 4, 1
        for i, bit in enumerate(binary):
            tt = np.linspace(0, 1, N, endpoint=False)
            cycles = cycles_0 if bit == '0' else cycles_1
            signal[i*N:(i+1)*N] = np.sin(2*np.pi*cycles*tt)
        ax.plot(t, signal)
        ax.set_title("Frequency Modulation (FM)")

    elif opsi == 5: # PM
        fc = 10
        for i, bit in enumerate(binary):
            phase = np.pi if bit == '1' else 0
            tt = t[i*N:(i+1)*N]
            signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*(tt-tt[0]) + phase)
        ax.plot(t, signal)
        ax.set_title("Phase Modulation (PM)")

    elif opsi == 6:  # ASK
        fc = 4
        for i, bit in enumerate(binary):
            tt = np.linspace(0, 1, N, endpoint=False)
            if bit == '1':
                signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*tt)
            else:
                signal[i*N:(i+1)*N] = 0
        ax.plot(t, signal)
        ax.set_title("Amplitude Shift Keying (ASK)")

    elif opsi == 7:  # FSK
        f0, f1 = 4, 8
        for i, bit in enumerate(binary):
            tt = np.linspace(0, 1, N, endpoint=False)
            freq = f1 if bit == '1' else f0
            signal[i*N:(i+1)*N] = np.sin(2 * np.pi * freq * tt)
        ax.plot(t, signal)
        ax.set_title("Frequency Shift Keying (FSK)")

    elif opsi == 8:  # PSK
        fc = 4
        for i, bit in enumerate(binary):
            tt = np.linspace(0, 1, N, endpoint=False)
            if bit == '1':
                signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*tt + np.pi)
            else:
                signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*tt)
        ax.plot(t, signal)
        ax.set_title("Phase Shift Keying (PSK)")

    elif opsi == 9:  # NRZ-L
        for i, bit in enumerate(binary):
            signal[i*N:(i+1)*N] = 1 - int(bit)
        ax.step(t, signal, where="post")
        ax.set_ylim(0.0, 1.05)
        ax.set_title("NRZ-L")

    elif opsi == 10: # NRZ-I
        level = 0
        for i, bit in enumerate(binary):
            if bit == '1':
                level = 1 - level
            signal[i*N:(i+1)*N] = level
        ax.step(t, signal, where="post")
        ax.set_ylim(0.0, 1.05)
        ax.set_title("NRZ-I")

    elif opsi == 11: # RZ
        for i, bit in enumerate(binary):
            if bit == '1':
                signal[i*N:i*N+N//2] = 1
                signal[i*N+N//2:(i+1)*N] = 0
            else:
                signal[i*N:i*N+N//2] = -1
                signal[i*N+N//2:(i+1)*N] = 0
        ax.step(t, signal, where="post")
        ax.set_ylim(-1.2, 1.2)
        ax.set_title("Return to Zero (RZ)")

    elif opsi == 12: # Manchester
        for i, bit in enumerate(binary):
            if bit == '1':
                signal[i*N:i*N+N//2] = 0
                signal[i*N+N//2:(i+1)*N] = 1
            else:
                signal[i*N:i*N+N//2] = 1
                signal[i*N+N//2:(i+1)*N] = 0
        ax.step(t, signal, where="post")
        ax.set_ylim(0.0, 1.05)
        ax.set_title("Manchester")

    elif opsi == 13: # Differential Manchester
        level = 1
        for i, bit in enumerate(binary):
            if bit == '0':
                level = 1 - level
            signal[i*N:i*N+N//2] = level
            level = 1 - level
            signal[i*N+N//2:(i+1)*N] = level
        ax.step(t, signal, where="post")
        ax.set_ylim(0.0, 1.05)
        ax.set_title("Differential Manchester")

    # Sumbu
    ax.set_xlabel("Waktu (detik)")
    ax.set_ylabel("Amplitudo")
    ax.set_xlim(0, total_time)
    ax.axhline(0, color="purple", linewidth=0.8) 
    ax.axvline(0, color="purple", linewidth=0.8)  

def generate_signal():
    digits = entry_digit.get()
    if not digits.isdigit():
        messagebox.showerror("Error", "Input harus angka / Kamu belum memasukkan input")
        return

    binary = keseluruhan_konversi(digits)
    selected_indices = listbox.curselection()
    if not selected_indices:
        messagebox.showerror("Error", "Pilih minimal satu skema!")
        return

    # Buat figure
    fig, axes = plt.subplots(len(selected_indices), 1, figsize=(13.5, 3*len(selected_indices)))
    if len(selected_indices) == 1:
        axes = [axes]

    for ax, idx in zip(axes, selected_indices):
        opsi = idx + 1
        gambar_encoding(binary, opsi, ax)

    plt.tight_layout(pad=3.0)
    plt.subplots_adjust(hspace=1.2)

    # ==== Scrollbar ====
    top = Toplevel(root)
    top.title("Generated Signals")
    top.geometry("960x400")

    frame_canvas = Frame(top)
    frame_canvas.pack(fill=BOTH, expand=True)

    canvas = Canvas(frame_canvas)
    scrollbar = Scrollbar(frame_canvas, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollable_frame = Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", update_scrollregion)

    fig_canvas = FigureCanvasTkAgg(fig, scrollable_frame)
    fig_canvas.get_tk_widget().pack(fill=BOTH, expand=True)

# ================== GUI ==================
root = Tk()
root.title("Hi, I'm your digital modulation simulator!")
root.state("zoomed")
root.config(bg="#EBD6FB")

main_frame = Frame(root, bg="#EBD6FB")
main_frame.place(relx=0.5, rely=0.5, anchor="center")
Label(main_frame, text="⋆˚꩜｡ Hi, I'm your digital modulation simulator! ⋆˚꩜｡",
      font=("Helvetica", 24, "bold"), bg="#EBD6FB").pack(pady=20)

frame_input = Frame(main_frame, bg="#EBD6FB")
frame_input.pack(pady=10)
Label(frame_input, text="Input your decimal :", font=("System", 14), bg="#EBD6FB").pack(side=LEFT, padx=8)
entry_digit = Entry(frame_input, width=20, font=("System", 14))
entry_digit.pack(side=LEFT)

options = [
    ' Digital Signal', ' Analog Signal', ' AM', ' FM', ' PM',
    ' ASK', ' FSK', ' PSK', ' NRZ-L', ' NRZ-I', ' RZ',
    ' Manchester', ' Differential Manchester'
]

frame_listbox = Frame(main_frame, bg="#898AC4")
frame_listbox.pack(pady=15)
Label(frame_listbox, text="Choose your signals!",
      font=("Helvetica", 12, "bold"), bg="#898AC4").pack()
listbox = Listbox(frame_listbox, selectmode=MULTIPLE,
                  height=5, width=50, font=("System", 12))
listbox.pack()
for opt in options:
    listbox.insert(END, opt)

Button(main_frame, text="Generate Signal", command=generate_signal,
       bg="#898AC4", fg="white", font=("System", 16, "bold"),
       width=22, height=2).pack(pady=25)

label_info = Label(main_frame, text="", font=("Helvetica", 12, "bold"), bg="#EBD6FB")
label_info.pack()

root.mainloop()
