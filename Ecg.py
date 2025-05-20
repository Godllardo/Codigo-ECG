import matplotlib.pyplot as plt
import serial
import numpy as np
from scipy.signal import find_peaks
import csv

# Configuración
bluetooth_port = 'COM4'
baud_rate = 9600
num_samples = 300  # Más valores para mostrar varios latidos
sampling_rate = 50  # Estimación en Hz (ajusta si sabes el real)
ecg_data = []

# Conexión serial
try:
    ser = serial.Serial(bluetooth_port, baud_rate, timeout=1)
    print(f"Conectado a {bluetooth_port}")
except serial.SerialException:
    print(f"No se pudo conectar a {bluetooth_port}")
    exit()

# Captura de datos
print("Capturando datos...")
while len(ecg_data) < num_samples:
    try:
        raw = ser.readline().decode('utf-8').strip()
        if raw.isdigit():
            value = int(raw)
            ecg_data.append(value)
            print(f"{len(ecg_data)}: {value}")
    except Exception as e:
        print(f"Error: {e}")

ser.close()
print("Captura completa.")

# Convertir a array para análisis
ecg_array = np.array(ecg_data)

# Detección de picos R
peaks, _ = find_peaks(ecg_array, height=2000, distance=30)

# Estimación de frecuencia cardíaca
duracion_seg = len(ecg_array) / sampling_rate
bpm = (len(peaks) / duracion_seg) * 60
print(f"Frecuencia cardíaca estimada: {bpm:.2f} BPM")

# Guardar los datos en un archivo CSV
with open("ecg_datos.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Muestra", "Valor_ECG"])
    for i, value in enumerate(ecg_data):
        writer.writerow([i, value])

# Graficar
plt.figure(figsize=(10, 4))
plt.plot(ecg_array, linewidth=1.5, color='red', label="ECG")
plt.plot(peaks, ecg_array[peaks], "ko", label="Picos R")  # Puntos negros
plt.ylim(1000, 3000)
plt.title(f"Captura de ECG - {bpm:.1f} BPM")
plt.xlabel("Muestras")
plt.ylabel("Valor ECG")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("ecg_con_picos_R.png")
plt.show()