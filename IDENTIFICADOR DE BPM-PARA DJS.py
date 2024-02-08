import os
import librosa
from mutagen.id3 import ID3, TXXX

# Pasta contendo as músicas
pasta_musica = r"C:\Users\Bruno\Desktop\INDENTIFICADOR DE BPM"

# Lista de extensões de arquivo de áudio suportadas (adicione mais se necessário)
extensoes_audio = [".mp3"]

# Parâmetros ajustáveis
start_bpm = 120  # Taxa de início em BPM (ajuste conforme necessário)
hop_length = 250  # Tamanho do salto (ajuste conforme necessário)

# Função para calcular o BPM em um segmento da música
def calcular_bpm_segmento(segmento, sr):
    onset_env = librosa.onset.onset_strength(y=segmento, sr=sr, hop_length=hop_length)
    return librosa.beat.beat_track(onset_envelope=onset_env, sr=sr, units='time', start_bpm=start_bpm, hop_length=hop_length)

# Função para processar uma única música
def processar_musica(caminho_audio):
    try:
        # Carregue o arquivo de áudio
        y, sr = librosa.load(caminho_audio, sr=None)  # Use sr=None para manter a taxa de amostragem original
        
        # Calcular o BPM em todo o comprimento da música
        bpm, _ = calcular_bpm_segmento(y, sr)
        
        # Abra o arquivo de áudio para leitura e escrita de metadados com mutagen
        audiofile = ID3(caminho_audio)
        
        # Verifique se há um campo BPM nos metadados
        if "TXXX:BPM" in audiofile:
            bpm_atual = float(audiofile["TXXX:BPM"].text[0])
            print(f"BPM atual da música '{caminho_audio}': {bpm_atual:.2f}")
            print(f"Novo BPM calculado: {bpm:.2f}")
            
            # Se o novo BPM for diferente do atual, atualize os metadados
            if round(bpm_atual) != round(bpm):
                audiofile["TXXX:BPM"] = TXXX(encoding=3, desc='BPM', text=str(round(bpm)))
                audiofile.save(caminho_audio)
                print(f"BPM atualizado para {bpm:.2f}")
            else:
                print("Os BPMs estão iguais. Nenhuma atualização necessária.")
        else:
            print(f"Não há informações de BPM para '{caminho_audio}'")
    except Exception as e:
        print(f"Erro ao processar '{caminho_audio}': {str(e)}")

# Iterar sobre os arquivos na pasta
for arquivo in os.listdir(pasta_musica):
    # Verifique se o arquivo tem uma extensão de áudio suportada
    if any(arquivo.endswith(ext) for ext in extensoes_audio):
        # Caminho completo para o arquivo de áudio
        caminho_audio = os.path.join(pasta_musica, arquivo)
        
        # Processar a música
        processar_musica(caminho_audio)
