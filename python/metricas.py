import os
import numpy as np
import librosa
import csv

# Configuração de caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILTRADOS_DIR = os.path.join(BASE_DIR, '..', 'filtrados')
OUTPUT_CSV = os.path.join(BASE_DIR, 'metricas_comparativas.csv')

# Ruídos e plataformas
RUIDOS = ['bebe', 'cachorro', 'caminhao', 'multidao', 'obras']
PLATAFORMAS = ['discord', 'krisp', 'teams', 'telegram', 'whatsapp', 'zoom']

# Funções de métricas

def calcular_rms(signal):
    return np.sqrt(np.mean(signal**2))

def snr(signal, noise):
    power_signal = np.mean(signal**2)
    power_noise = np.mean(noise**2)
    if power_noise == 0:
        return float('inf')
    return 10 * np.log10(power_signal / power_noise)

def sdr(original, estimate):
    noise = original - estimate
    return snr(original, noise)

def dbfs(rms):
    if rms == 0:
        return -float('inf')
    return 20 * np.log10(rms)

# Cria e escreve o CSV
with open(OUTPUT_CSV, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        'Ruído', 'Plataforma', 
        'SNR (dB)', 'SDR (dB)', 
        'Nível Médio (Base) [dBFS]', 'Nível Médio (Filtrado) [dBFS]'
    ])

    for ruido in RUIDOS:
        nome_base = f'(desativado) romulo + {ruido}.mp3'
        caminho_base = os.path.join(FILTRADOS_DIR, 'Filtro desativado', nome_base)

        if not os.path.exists(caminho_base):
            print(f"[AVISO] Áudio base não encontrado: {caminho_base}")
            continue

        y_base, sr_base = librosa.load(caminho_base, sr=None)

        for plataforma in PLATAFORMAS:
            nome_filtrado = f"{plataforma.split()[0].upper()} - romulo + {ruido}.mp3"
            caminho_filtrado = os.path.join(FILTRADOS_DIR, plataforma, nome_filtrado)

            if not os.path.exists(caminho_filtrado):
                print(f"[AVISO] Áudio filtrado não encontrado: {caminho_filtrado}")
                continue

            y_filt, sr_filt = librosa.load(caminho_filtrado, sr=None)

            # Reamostragem se necessário
            if sr_base != sr_filt:
                y_filt = librosa.resample(y_filt, orig_sr=sr_filt, target_sr=sr_base)

            min_len = min(len(y_base), len(y_filt))
            y_base_crop = y_base[:min_len]
            y_filt_crop = y_filt[:min_len]

            erro = y_base_crop - y_filt_crop

            # Métricas
            valor_snr = snr(y_base_crop, erro)
            valor_sdr = sdr(y_base_crop, y_filt_crop)
            rms_base = calcular_rms(y_base_crop)
            rms_filt = calcular_rms(y_filt_crop)
            db_base = dbfs(rms_base)
            db_filt = dbfs(rms_filt)

            writer.writerow([
                ruido, plataforma, 
                round(valor_snr, 2), round(valor_sdr, 2), 
                round(db_base, 2), round(db_filt, 2)
            ])

print(f"✅ Métricas salvas em: {OUTPUT_CSV}")
