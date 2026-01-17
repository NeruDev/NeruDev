# MUSICA
Registro de música favorita - Sistema de gestión de base de datos musical en JSON

## 📁 Estructura del Proyecto

```
MUSICA/
├── data/
│   ├── raw/          # JSONs originales de yt-dlp
│   └── clean/        # JSONs procesados y limpios
├── src/
│   ├── models.py     # Schema de datos con dataclasses
│   └── cleaner.py    # Script de limpieza y procesamiento
└── README.md
```

## 🎯 Características

- **Schema de datos estructurado**: Utiliza dataclasses de Python para definir el modelo de datos musical
- **Limpieza automática**: Extrae nombres de artistas de títulos usando expresiones regulares
- **Compatibilidad con yt-dlp**: Procesa JSONs generados por yt-dlp
- **Formato de fecha**: Convierte fechas del formato YYYYMMDD a ISO (YYYY-MM-DD)

## 📋 Schema de Datos

El modelo `MusicTrack` incluye los siguientes campos:

- **id**: Identificador único del track
- **titulo**: Título completo de la canción
- **artista**: Nombre del artista (extraído automáticamente)
- **url**: URL del video/canción
- **fecha**: Fecha en formato ISO (YYYY-MM-DD)

## 🚀 Uso

### 1. Colocar archivos JSON de yt-dlp en `data/raw/`

```bash
# Ejemplo de cómo descargar metadata con yt-dlp
yt-dlp --write-info-json --skip-download "URL_DEL_VIDEO" -o "data/raw/%(id)s"
```

### 2. Ejecutar el script de limpieza

```bash
cd src
python cleaner.py
```

El script procesará todos los archivos `.json` en `data/raw/` y guardará las versiones limpias en `data/clean/`.

## 🎨 Patrones de Extracción de Artistas

El sistema reconoce automáticamente varios formatos de títulos:

- `[Artista] Título de la canción`
- `Artista - Título de la canción`
- `Artista『Título』`
- `Artista / Título`

### Ejemplos:

- `"Kikuo - 愛して愛して愛して"` → Artista: `"Kikuo"`
- `"[米津玄師] Lemon"` → Artista: `"米津玄師"`
- `"Artist Name『Song Title』"` → Artista: `"Artist Name"`

## 📊 Ejemplo de Transformación

**Entrada (data/raw/ABC123.json):**
```json
{
  "id": "ABC123XYZ",
  "title": "Kikuo - 愛して愛して愛して",
  "uploader": "Kikuo Official",
  "upload_date": "20231015",
  "webpage_url": "https://www.youtube.com/watch?v=ABC123XYZ"
}
```

**Salida (data/clean/ABC123.json):**
```json
{
  "id": "ABC123XYZ",
  "titulo": "Kikuo - 愛して愛して愛して",
  "artista": "Kikuo",
  "url": "https://www.youtube.com/watch?v=ABC123XYZ",
  "fecha": "2023-10-15"
}
```

## 🛠️ Requisitos

- Python 3.7+
- No se requieren dependencias externas (usa solo la biblioteca estándar de Python)

## 📝 Notas

- El script preserva los caracteres Unicode (japonés, chino, etc.)
- Si no se puede extraer el artista del título, se usa el valor del campo `uploader` o `channel`
- Los archivos JSON se guardan con codificación UTF-8 e indentación de 2 espacios
