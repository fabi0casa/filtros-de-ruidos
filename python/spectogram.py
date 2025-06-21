import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Caminhos principais
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILTRADOS_DIR = os.path.join(BASE_DIR, '..', 'filtrados')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'espectogramas')

# Pastas das plataformas (exceto a dos áudios base)
PLATAFORMAS = ['discord', 'krisp', 'teams', 'telegram', 'whatsapp', 'zoom']

# Ruídos considerados
RUIDOS = ['bebe', 'cachorro', 'caminhao', 'multidao', 'obras']

# Função para garantir que diretórios existam
def garantir_pasta(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Função para plotar espectrograma simples
def gerar_onda_base(caminho_audio, nome_ruido, output_path):
    y, sr = librosa.load(caminho_audio, sr=None)
    tempo = np.linspace(0, len(y) / sr, num=len(y))
    
    plt.figure(figsize=(12, 4))
    plt.plot(tempo, y, color='red', alpha=0.8)
    plt.title(f'Forma de Onda - Áudio Base: {nome_ruido}')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Áudio base salvo: {output_path}")

# Função para sobrepor
def sobrepor_ondas(base_audio_path, filtrado_path, nome_plataforma, nome_ruido, output_path):
    y_base, sr_base = librosa.load(base_audio_path, sr=None)
    y_filt, sr_filt = librosa.load(filtrado_path, sr=None)

    # Reamostragem se necessário
    if sr_base != sr_filt:
        y_filt = librosa.resample(y_filt, orig_sr=sr_filt, target_sr=sr_base)
        sr_filt = sr_base

    min_len = min(len(y_base), len(y_filt))
    y_base = y_base[:min_len]
    y_filt = y_filt[:min_len]
    tempo = np.linspace(0, min_len / sr_base, num=min_len)

    plt.figure(figsize=(12, 4))
    plt.plot(tempo, y_base, label='Base', color='red', alpha=0.5)
    plt.plot(tempo, y_filt, label='Filtrado', color='blue', alpha=0.6)
    plt.title(f'Sobreposição - {nome_plataforma.upper()} - {nome_ruido}')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Sobreposição salva: {output_path}")

# Executa geração
def gerar_todos():
    base_folder = os.path.join(FILTRADOS_DIR, 'Filtro desativado')
    base_output = os.path.join(OUTPUT_DIR, 'audios base')
    garantir_pasta(base_output)

    for ruido in RUIDOS:
        nome_arquivo_base = f'(desativado) romulo + {ruido}.mp3'
        caminho_base = os.path.join(base_folder, nome_arquivo_base)
        if not os.path.exists(caminho_base):
            print(f"Arquivo base não encontrado: {caminho_base}")
            continue

        # Gera espectrograma do áudio base sozinho
        output_base = os.path.join(base_output, f'{ruido}.png')
        gerar_onda_base(caminho_base, ruido, output_base)

        # Para cada plataforma, gera sobreposição
        for plataforma in PLATAFORMAS:
            nome_arquivo_filt = f"{plataforma.split()[0].upper()} - romulo + {ruido}.mp3"
            caminho_filt = os.path.join(FILTRADOS_DIR, plataforma, nome_arquivo_filt)
            if not os.path.exists(caminho_filt):
                print(f"Arquivo filtrado não encontrado: {caminho_filt}")
                continue

            pasta_out = os.path.join(OUTPUT_DIR, plataforma)
            garantir_pasta(pasta_out)

            output_path = os.path.join(pasta_out, f'{ruido}.png')
            sobrepor_ondas(caminho_base, caminho_filt, plataforma, ruido, output_path)

# Executar
if __name__ == "__main__":
    gerar_todos()
