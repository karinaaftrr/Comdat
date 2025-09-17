import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox, ttk

def keseluruhan_konversi(digits):
    return format(int(digits), 'b')

def gambar_encoding(binary, opsi):
    Tb = 0.1       
    N = 100         
    total_time = len(binary) * Tb
    t = np.linspace(0, total_time, len(binary) * N)
    signal = np.zeros_like(t)

    if opsi == 1:  
        for i, bit in enumerate(binary):
            signal[i*N:(i+1)*N] = 1 if bit == '1' else 0
        plt.step(t, signal, where="post")
        plt.ylim(0.0, 1.05)
        plt.title("Sinyal Digital")

    elif opsi == 2:
        f = 5
        signal = np.sin(2*np.pi*f*t)
        plt.plot(t, signal)
        plt.title("Sinyal Analog")

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

    elif opsi == 4:
        cycles_0 = 4
        cycles_1 = 1
        for i, bit in enumerate(binary):
            tt = np.linspace(0, 1, N, endpoint=False)
            if bit == '0':
                cycles = cycles_0
            else:
                cycles = cycles_1
            signal[i*N:(i+1)*N] = np.sin(2*np.pi*cycles*tt)
        plt.plot(t, signal)
        plt.title("Frequency Modulation (FM)")


    elif opsi == 5:
        fc = 10
        for i, bit in enumerate(binary):
            phase = np.pi if bit == '1' else 0
            tt = t[i*N:(i+1)*N]
            signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*(tt-tt[0]) + phase)
        plt.plot(t, signal)
        plt.title("Phase Modulation (PM)")

    elif opsi == 6:
        fc = 10
        for i, bit in enumerate(binary):
            amp = 1 if bit == '1' else 0.3
            tt = t[i*N:(i+1)*N]
            signal[i*N:(i+1)*N] = amp*np.sin(2*np.pi*fc*(tt-tt[0]))
        plt.plot(t, signal)
        plt.title("Amplitude Shift Keying (ASK)")

    elif opsi == 7:
        fc0, fc1 = 5, 15
        for i, bit in enumerate(binary):
            fc = fc1 if bit == '1' else fc0
            tt = t[i*N:(i+1)*N]
            signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*(tt-tt[0]))
        plt.plot(t, signal)
        plt.title("Frequency Shift Keying (FSK)")

    elif opsi == 8:
        fc = 10
        for i, bit in enumerate(binary):
            phase = 0 if bit == '0' else np.pi
            tt = t[i*N:(i+1)*N]
            signal[i*N:(i+1)*N] = np.sin(2*np.pi*fc*(tt-tt[0]) + phase)
        plt.plot(t, signal)
        plt.title("Phase Shift Keying (PSK)")

    elif opsi == 9: 
        for i, bit in enumerate(binary):
            signal[i*N:(i+1)*N] = 1 if bit == '1' else 0
        plt.step(t, signal, where="post")
        plt.ylim(0.0, 1.05)
        plt.title("NRZ-L")

    elif opsi == 10: 
        level = 0
        for i, bit in enumerate(binary):
            if bit == '1':
                level = 1 - level
            signal[i*N:(i+1)*N] = level
        plt.step(t, signal, where="post")
        plt.ylim(0.0, 1.05)
        plt.title("NRZ-I")

    elif opsi == 11:
        for i, bit in enumerate(binary):
            if bit == '1':
                signal[i*N:i*N+N//2] = 1
            signal[i*N+N//2:(i+1)*N] = 0
        plt.step(t, signal, where="post")
        plt.ylim(0.0, 1.05)
        plt.title("Return to Zero (RZ)")

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

    plt.xlabel("Waktu (detik)")
    plt.ylabel("Amplitudo")
    plt.xlim(0, total_time)
    plt.grid(False)
    plt.show()

def generate_signal():
    digits = entry_digit.get()
    if not digits.isdigit():
        messagebox.showerror("Error", "Input harus berupa angka (0-9)")
        return

    binary = keseluruhan_konversi(digits)
    opsi = combo_box.current() + 1 

    label_info.config(text=f"Biner: {binary}\nSkema: {combo_box.get()}")
    gambar_encoding(binary, opsi)

root = Tk()
root.title("Digital Modulation Simulator")
root.geometry("480x300")
root.config(bg="#f8f8f8")

Label(root, text="Digital Modulation Simulator", font=("Arial", 14, "bold"), bg="#f8f8f8").pack(pady=10)

frame_input = Frame(root, bg="#f8f8f8")
frame_input.pack(pady=5)
Label(frame_input, text="Masukkan Angka:", bg="#f8f8f8").pack(side=LEFT, padx=5)
entry_digit = Entry(frame_input, width=15, font=("Arial", 12))
entry_digit.pack(side=LEFT)

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

Button(root, text="Generate Signal", command=generate_signal, bg="#4CAF50", fg="white",
       font=("Arial", 11), width=20).pack(pady=15)

label_info = Label(root, text="", font=("Arial", 10), bg="#f8f8f8")
label_info.pack()

root.mainloop()

