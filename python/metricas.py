import os
import numpy as np
import librosa
import csv
from scipy.signal import correlate

# Compatibilidade com numpy > 1.24
if not hasattr(np, 'complex'):
    np.complex = complex

# Configuração de caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILTRADOS_DIR = os.path.join(BASE_DIR, '..', 'filtrados')
ORIGINAL_PATH = os.path.join(BASE_DIR, '..', 'Audios originais', 'romulo falando.mp3')
OUTPUT_CSV = os.path.join(BASE_DIR, 'metricas_comparativas.csv')

# Ruídos e plataformas
RUIDOS = ['bebe', 'cachorro', 'caminhao', 'multidao', 'obras']
PLATAFORMAS = ['discord', 'krisp', 'teams', 'telegram', 'whatsapp', 'zoom']

# Funções
def calcular_rms(signal):
    return np.sqrt(np.mean(signal**2))

def dbfs(rms):
    if rms == 0:
        return -float('inf')
    return 20 * np.log10(rms)

def normalizar(signal, eps=1e-4):
    max_abs = np.max(np.abs(signal))
    return signal / (max_abs + eps)

def alinhar_sinais(ref, est, max_lag=88200):
    trecho = min(len(ref), len(est), 10 * max_lag)
    ref_seg = ref[:trecho] - np.mean(ref[:trecho])
    est_seg = est[:trecho] - np.mean(est[:trecho])
    corr = correlate(ref_seg, est_seg, mode='full')
    lags = np.arange(-len(est_seg) + 1, len(ref_seg))
    lag = lags[np.argmax(corr)]

    if lag > 0:
        ref = ref[lag:]
        est = est[:len(ref)]
    elif lag < 0:
        est = est[-lag:]
        ref = ref[:len(est)]

    min_len = min(len(ref), len(est))
    return ref[:min_len], est[:min_len]

def similaridade_espectral(ref, est, sr, n_fft=1024, hop_length=512):
    S_ref = np.abs(librosa.stft(ref, n_fft=n_fft, hop_length=hop_length))
    S_est = np.abs(librosa.stft(est, n_fft=n_fft, hop_length=hop_length))

    min_frames = min(S_ref.shape[1], S_est.shape[1])
    S_ref = S_ref[:, :min_frames]
    S_est = S_est[:, :min_frames]

    ref_flat = S_ref.flatten()
    est_flat = S_est.flatten()
    if np.std(ref_flat) == 0 or np.std(est_flat) == 0:
        return 0.0
    corr = np.corrcoef(ref_flat, est_flat)[0, 1]
    return corr

# Carrega o áudio original limpo
if not os.path.exists(ORIGINAL_PATH):
    raise FileNotFoundError(f"Áudio original limpo não encontrado em: {ORIGINAL_PATH}")

y_original, sr_original = librosa.load(ORIGINAL_PATH, sr=None, mono=True)
y_original = normalizar(y_original)

# Cria e escreve o CSV
with open(OUTPUT_CSV, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        'Ruído', 'Plataforma',
        'Similaridade Espectral com Original (%)',
        'Nível Médio (Base) [dBFS]', 'Nível Médio (Filtrado) [dBFS]'
    ])

    for ruido in RUIDOS:
        nome_base = f'(desativado) romulo + {ruido}.mp3'
        caminho_base = os.path.join(FILTRADOS_DIR, 'Filtro desativado', nome_base)

        if not os.path.exists(caminho_base):
            print(f"[AVISO] Áudio base não encontrado: {caminho_base}")
            continue

        y_base, sr_base = librosa.load(caminho_base, sr=None, mono=True)
        y_base = normalizar(y_base)

        for plataforma in PLATAFORMAS:
            nome_filtrado = f"{plataforma.split()[0].upper()} - romulo + {ruido}.mp3"
            caminho_filtrado = os.path.join(FILTRADOS_DIR, plataforma, nome_filtrado)

            if not os.path.exists(caminho_filtrado):
                print(f"[AVISO] Áudio filtrado não encontrado: {caminho_filtrado}")
                continue

            y_filt, sr_filt = librosa.load(caminho_filtrado, sr=None, mono=True)
            y_filt = normalizar(y_filt)

            if sr_filt != sr_original:
                y_filt = librosa.resample(y_filt, orig_sr=sr_filt, target_sr=sr_original)

            # Alinhar o áudio filtrado com o original limpo
            y_original_alinhado, y_filt_alinhado = alinhar_sinais(y_original, y_filt)

            # Similaridade espectral
            sim_esp = similaridade_espectral(y_original_alinhado, y_filt_alinhado, sr_original)
            sim_esp_percent = max(0.0, round(sim_esp * 100, 2))

            # Níveis médios (com base no áudio com ruído)
            if sr_base != sr_filt:
                y_base = librosa.resample(y_base, orig_sr=sr_base, target_sr=sr_filt)
                sr_base = sr_filt

            y_base_alinhado, y_filt_alinhado_db = alinhar_sinais(y_base, y_filt)
            db_base = dbfs(calcular_rms(y_base_alinhado))
            db_filt = dbfs(calcular_rms(y_filt_alinhado_db))

            writer.writerow([
                ruido, plataforma,
                sim_esp_percent,
                round(db_base, 2), round(db_filt, 2)
            ])

print(f"✅ Métricas salvas em: {OUTPUT_CSV}")
