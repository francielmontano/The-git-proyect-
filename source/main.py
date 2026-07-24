from bcoding import bdecode

# 1. Abrir y decodificar el archivo torrent
with open('music.torrent', 'rb') as f:
    metadata = bdecode(f)

# 2. Extraer el tracker de forma segura
announce_bytes = metadata.get(b'announce')

if announce_bytes is not None:
    tracker = announce_bytes.decode('utf-8')
    print(f"Tracker Principal: {tracker}")
else:
    print("Tracker Principal: No disponible (Este torrent podría usar DHT o enlaces Magnet)")

# 3. Extraer una lista alternativa de trackers (si existe)
if b'announce-list' in metadata:
    print("\nLista de Trackers alternativos:")
    for grupo_trackers in metadata[b'announce-list']:
        for t in grupo_trackers:
            print(f" - {t.decode('utf-8')}")