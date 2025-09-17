# ===================== 1. IMPORT & SETUP =====================
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox, ttk


# ===================== 2. FUNGSI UTAMA =====================

def keseluruhan_konversi(digits):
    """Konversi angka desimal ke biner (string)."""
    return format(int(digits), 'b')


def gambar_encoding(binary, opsi):
    """Gambar grafik sesuai opsi encoding/modulasi."""
    Tb = 0.1       # durasi 1 bit
    N = 100        # titik per bit
    total_time = len(binary) * Tb
    t = np.linspace(0, total_time, len(binary) * N)
    signal = np.zeros_like(t)

    # === Sinyal Digital ===
    if opsi == 1:
        for i, bit in enumerate(binary):
            signal[i*N:(i+1)*N] = 1 if bit == '1' else 0
        plt.step(t, signal, where="post")
        plt.ylim(0.0, 1.05)
        plt.title("Sinyal Digital")

    # === Sinyal Analog ===
    elif opsi == 2:
        f = 5
        signal = np.sin(2*np.pi*f*t)
        plt.plot(t, signal)
        plt.title("Sinyal Analog")

    # === Amplitude Modulation (AM) ===
    elif opsi == 3:
        fc = 10
        for i, bit in enumerate(binary):
            tt = t[i*N:(i+1)*N]
            if bit == '1':
                signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*(tt - tt[0]))
            else:
                signal[i*N:(i+1)*N] = 0
        plt.plot(t, signal)
        plt.title("Amplitude Modulation (AM)")

    # === Frequency Modulation (FM) ===
    elif opsi == 4:
        cycles_0, cycles_1 = 4, 1
        for i, bit in enumerate(binary):
            tt = np.linspace(0, 1, N, endpoint=False)
            cycles = cycles_0 if bit == '0' else cycles_1
            signal[i*N:(i+1)*N] = np.sin(2*np.pi*cycles*tt)
        plt.plot(t, signal)
        plt.title("Frequency Modulation (FM)")

    # === Phase Modulation (PM) ===
    elif opsi == 5:
        fc = 10
        for i, bit in enumerate(binary):
            phase = np.pi if bit == '1' else 0
            tt = t[i*N:(i+1)*N]
            signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*(tt-tt[0]) + phase)
        plt.plot(t, signal)
        plt.title("Phase Modulation (PM)")

    elif opsi == 6:  # ASK
        fc = 4
        for i, bit in enumerate(binary):
            tt = np.linspace(0, 1, N, endpoint=False)
            if bit == '1':
                signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*tt)
            else:
                signal[i*N:(i+1)*N] = 0
        plt.plot(t, signal)
        plt.title("Amplitude Shift Keying (ASK)")

    elif opsi == 7:  # FSK
        f0, f1 = 4, 8   # jumlah siklus per bit (bukan Hz absolut)
        for i, bit in enumerate(binary):
            tt = np.linspace(0, 1, N, endpoint=False)
            freq = f1 if bit == '1' else f0
            signal[i*N:(i+1)*N] = np.sin(2 * np.pi * freq * tt)
        plt.plot(t, signal)
        plt.title("Frequency Shift Keying (FSK)")


    elif opsi == 8:  # PSK
        fc = 4
        for i, bit in enumerate(binary):
            tt = np.linspace(0, 1, N, endpoint=False)
            if bit == '1':
                signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*tt + np.pi)
            else:
                signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*tt)
        plt.plot(t, signal)
        plt.title("Phase Shift Keying (PSK)")

    # === NRZ-L ===
    elif opsi == 9:
        for i, bit in enumerate(binary):
            signal[i*N:(i+1)*N] = 1 if bit == '1' else 0
        plt.step(t, signal, where="post")
        plt.ylim(0.0, 1.05)
        plt.title("NRZ-L")

    # === NRZ-I ===
    elif opsi == 10:
        level = 0
        for i, bit in enumerate(binary):
            if bit == '1':
                level = 1 - level
            signal[i*N:(i+1)*N] = level
        plt.step(t, signal, where="post")
        plt.ylim(0.0, 1.05)
        plt.title("NRZ-I")

    # === Return to Zero (RZ) ===
    elif opsi == 11:
        for i, bit in enumerate(binary):
            if bit == '1':
                signal[i*N:i*N+N//2] = 1
                signal[i*N+N//2:(i+1)*N] = 0
            else:
                signal[i*N:i*N+N//2] = -1
                signal[i*N+N//2:(i+1)*N] = 0
        plt.step(t, signal, where="post")
        plt.ylim(-1.2, 1.2)
        plt.title("Return to Zero (RZ)")

    # === Manchester ===
    elif opsi == 12:
        for i, bit in enumerate(binary):
            if bit == '1':
                signal[i*N:i*N+N//2] = 0
                signal[i*N+N//2:(i+1)*N] = 1
            else:
                signal[i*N:i*N+N//2] = 1
                signal[i*N+N//2:(i+1)*N] = 0
        plt.step(t, signal, where="post")
        plt.ylim(0.0, 1.05)
        plt.title("Manchester")

    # === Differential Manchester ===
    elif opsi == 13:
        level = 1
        for i, bit in enumerate(binary):
            if bit == '0':
                level = 1 - level
            signal[i*N:i*N+N//2] = level
            level = 1 - level
            signal[i*N+N//2:(i+1)*N] = level
        plt.step(t, signal, where="post")
        plt.ylim(0.0, 1.05)
        plt.title("Differential Manchester")

    # === Sumbu & Layout ===
    plt.xlabel("Waktu (detik)", labelpad=200)
    plt.ylabel("Amplitudo")
    plt.xlim(0, total_time)
    plt.grid(False)

    ax = plt.gca()
    ax.spines['bottom'].set_position(('data', 0))

    plt.show()


# ===================== 3. EVENT HANDLER =====================

def generate_signal():
    digits = entry_digit.get()
    if not digits.isdigit():
        messagebox.showerror("Error", "Input harus angka")
        return

    binary = keseluruhan_konversi(digits)
    opsi = combo_box.current() + 1
    label_info.config(text=f"Biner: {binary}\nSkema: {combo_box.get()}")
    gambar_encoding(binary, opsi)


# ===================== 4. GUI (TKINTER) =====================

root = Tk()
root.title("Digital Modulation Simulator")
root.state("zoomed")
root.config(bg="#f8f8f8")

# Frame utama
main_frame = Frame(root, bg="#f8f8f8")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Judul
Label(main_frame, text="Digital Modulation Simulator",
      font=("Arial", 24, "bold"), bg="#f8f8f8").pack(pady=20)

# Input angka
frame_input = Frame(main_frame, bg="#f8f8f8")
frame_input.pack(pady=10)
Label(frame_input, text="Masukkan Angka:", font=("Arial", 12), bg="#f8f8f8").pack(side=LEFT, padx=8)
entry_digit = Entry(frame_input, width=20, font=("Arial", 14))
entry_digit.pack(side=LEFT)

# Dropdown skema
options = [
    'Sinyal Digital', 'Sinyal Analog', 'AM', 'FM', 'PM',
    'ASK', 'FSK', 'PSK', 'NRZ-L', 'NRZ-I', 'RZ',
    'Manchester', 'Differential Manchester'
]
frame_combo = Frame(main_frame, bg="#f8f8f8")
frame_combo.pack(pady=15)
Label(frame_combo, text="Pilih Skema:", font=("Arial", 12), bg="#f8f8f8").pack(side=LEFT, padx=8)
combo_box = ttk.Combobox(frame_combo, values=options, state="readonly", width=28, font=("Arial", 12))
combo_box.pack(side=LEFT)
combo_box.current(0)

# Tombol generate
Button(main_frame, text="Generate Signal", command=generate_signal,
       bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
       width=22, height=2).pack(pady=25)

# Info hasil
label_info = Label(main_frame, text="", font=("Arial", 11), bg="#f8f8f8")
label_info.pack()

root.mainloop()
