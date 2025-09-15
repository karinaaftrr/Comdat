import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox, ttk

# ===================== Fungsi Encoding ======================
def keseluruhan_konversi(digits):
    return format(int(digits), 'b')

def gambar_encoding(binary, opsi):
    Tb = 0.1        # durasi 1 bit = 0.1 detik
    N = 100         # titik per bit
    total_time = len(binary) * Tb
    t = np.linspace(0, total_time, len(binary) * N)
    signal = np.zeros_like(t)

    # --- Sinyal Digital (default untuk semua metode) ---
    if opsi == 1:  # Sinyal Digital
        for i, bit in enumerate(binary):
            signal[i*N:(i+1)*N] = 1 if bit == '1' else 0
        plt.plot(t, signal, drawstyle='steps-pre')
        plt.ylim(-0.2, 1.2)
        plt.title("Sinyal Digital (0 dan 1)")

    elif opsi == 2:  # Sinyal Analog
        f = 5
        signal = np.sin(2*np.pi*f*t)
        plt.plot(t, signal)
        plt.title("Sinyal Analog (Sinus)")

    elif opsi == 3:  # AM
        fc = 10
        carrier = np.sin(2*np.pi*fc*t)
        m = np.repeat([int(b) for b in binary], N)
        signal = (1 + m) * carrier
        plt.plot(t, signal)
        plt.title("Amplitude Modulation (AM)")

    elif opsi == 4:  # FM
        fc0, fc1 = 5, 15
        for i, bit in enumerate(binary):
            fc = fc1 if bit == '1' else fc0
            tt = t[i*N:(i+1)*N]
            signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*(tt - tt[0]))
        plt.plot(t, signal)
        plt.title("Frequency Modulation (FM)")

    elif opsi == 5:  # PM
        fc = 10
        for i, bit in enumerate(binary):
            phase = np.pi if bit == '1' else 0
            tt = t[i*N:(i+1)*N]
            signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*(tt-tt[0]) + phase)
        plt.plot(t, signal)
        plt.title("Phase Modulation (PM)")

    elif opsi == 6:  # ASK
        fc = 10
        for i, bit in enumerate(binary):
            amp = 1 if bit == '1' else 0.3
            tt = t[i*N:(i+1)*N]
            signal[i*N:(i+1)*N] = amp*np.sin(2*np.pi*fc*(tt-tt[0]))
        plt.plot(t, signal)
        plt.title("Amplitude Shift Keying (ASK)")

    elif opsi == 7:  # FSK
        fc0, fc1 = 5, 15
        for i, bit in enumerate(binary):
            fc = fc1 if bit == '1' else fc0
            tt = t[i*N:(i+1)*N]
            signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*(tt-tt[0]))
        plt.plot(t, signal)
        plt.title("Frequency Shift Keying (FSK)")

    elif opsi == 8:  # PSK
        fc = 10
        for i, bit in enumerate(binary):
            phase = 0 if bit == '0' else np.pi
            tt = t[i*N:(i+1)*N]
            signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*(tt-tt[0]) + phase)
        plt.plot(t, signal)
        plt.title("Phase Shift Keying (PSK)")

    elif opsi == 9:  # NRZ-L
        for i, bit in enumerate(binary):
            signal[i*N:(i+1)*N] = 1 if bit == '1' else 0
        plt.plot(t, signal, drawstyle='steps-pre')
        plt.ylim(-0.2, 1.2)
        plt.title("NRZ-L")

    elif opsi == 10:  # NRZ-I
        level = 0
        for i, bit in enumerate(binary):
            if bit == '1':
                level = 1 - level  # toggle antara 0 dan 1
            signal[i*N:(i+1)*N] = level
        plt.plot(t, signal, drawstyle='steps-pre')
        plt.ylim(-0.2, 1.2)
        plt.title("NRZ-I")

    elif opsi == 11:  # RZ
        for i, bit in enumerate(binary):
            if bit == '1':
                signal[i*N:i*N+N//2] = 1
            signal[i*N+N//2:(i+1)*N] = 0
        plt.plot(t, signal, drawstyle='steps-pre')
        plt.ylim(-0.2, 1.2)
        plt.title("Return to Zero (RZ)")

    elif opsi == 12:  # Manchester
        for i, bit in enumerate(binary):
            if bit == '1':  # 1 = low → high
                signal[i*N:i*N+N//2] = 0
                signal[i*N+N//2:(i+1)*N] = 1
            else:          # 0 = high → low
                signal[i*N:i*N+N//2] = 1
                signal[i*N+N//2:(i+1)*N] = 0
        plt.plot(t, signal, drawstyle='steps-pre')
        plt.ylim(-0.2, 1.2)
        plt.title("Manchester")

    elif opsi == 13:  # Differential Manchester
        level = 1
        for i, bit in enumerate(binary):
            if bit == '0':  # transition at start
                level = 1 - level
            signal[i*N:i*N+N//2] = level
            level = 1 - level
            signal[i*N+N//2:(i+1)*N] = level
        plt.plot(t, signal, drawstyle='steps-pre')
        plt.ylim(-0.2, 1.2)
        plt.title("Differential Manchester")

    plt.xlabel("Waktu (detik)")
    plt.ylabel("Amplitudo")
    plt.xlim(0, total_time)
    plt.grid(True)
    plt.show()

# ===================== GUI Tkinter ======================
def generate_signal():
    digits = entry_digit.get()
    if len(digits) != 5 or not digits.isdigit():
        messagebox.showerror("Error", "Input harus tepat 5 angka (0-9)")
        return

    binary = keseluruhan_konversi(digits)
    opsi = combo_box.current() + 1  # index tkinter mulai dari 0

    label_info.config(text=f"Biner: {binary}\nSkema: {combo_box.get()}")
    gambar_encoding(binary, opsi)

# Membuat window utama
root = Tk()
root.title("Digital Modulation Simulator")
root.geometry("450x300")
root.config(bg="#f8f8f8")

# Label Judul
Label(root, text="Digital Modulation Simulator", font=("Arial", 14, "bold"), bg="#f8f8f8").pack(pady=10)

# Input angka 5 digit
frame_input = Frame(root, bg="#f8f8f8")
frame_input.pack(pady=5)
Label(frame_input, text="Masukkan 5 Digit Angka:", bg="#f8f8f8").pack(side=LEFT, padx=5)
entry_digit = Entry(frame_input, width=10, font=("Arial", 12))
entry_digit.pack(side=LEFT)

# Dropdown pilihan encoding
options = [
    'Sinyal Digital', 'Sinyal Analog', 'AM', 'FM', 'PM',
    'ASK', 'FSK', 'PSK', 'NRZ-L', 'NRZ-I', 'RZ',
    'Manchester', 'Differential Manchester'
]

frame_combo = Frame(root, bg="#f8f8f8")
frame_combo.pack(pady=10)
Label(frame_combo, text="Pilih Skema:", bg="#f8f8f8").pack(side=LEFT, padx=5)
combo_box = ttk.Combobox(frame_combo, values=options, state="readonly", width=25)
combo_box.pack(side=LEFT)
combo_box.current(0)

# Tombol generate
Button(root, text="Generate Signal", command=generate_signal, bg="#4CAF50", fg="white",
       font=("Arial", 11), width=20).pack(pady=15)

# Label info hasil
label_info = Label(root, text="", font=("Arial", 10), bg="#f8f8f8")
label_info.pack()

# Jalankan GUI
root.mainloop()
