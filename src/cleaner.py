"""
Script to clean and process musical data from raw JSON files.

Reads JSON files from data/raw, extracts artist names from titles using regex,
maps data to MusicTrack schema, and saves cleaned data to data/clean.
"""
import json
import re
import os
from pathlib import Path
from typing import List, Dict, Any
from models import MusicTrack

# Regular expression pattern for valid artist name characters (alphanumeric + Japanese)
VALID_ARTIST_CHARS = r'\w\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF'


def extract_artist_from_title(title: str) -> str:
    """
    Extract artist name from title using regex patterns.
    
    Common patterns:
    - "[Artist] Song Title"
    - "Artist - Song Title"
    - "Artist『Song Title』"
    - "Artist / Song Title"
    
    Args:
        title: The full title string
        
    Returns:
        Extracted artist name or empty string if not found
    """
    # Pattern 1: [Artist] format at the start (must be checked before dash)
    match = re.search(r'^\[([^\]]+)\]', title)
    if match:
        return match.group(1).strip()
    
    # Pattern 2: 【Artist】 format at the start
    match = re.search(r'^【([^】]+)】', title)
    if match:
        return match.group(1).strip()
    
    # Pattern 3: Artist - Song Title
    match = re.search(r'^([^-]+)\s*-', title)
    if match:
        return match.group(1).strip()
    
    # Pattern 4: Artist『Song Title』or similar brackets
    match = re.search(r'^([^『【\[]+)[\s]*[『【\[]', title)
    if match:
        return match.group(1).strip()
    
    # Pattern 5: Artist / Song Title
    match = re.search(r'^([^/]+)\s*/', title)
    if match:
        return match.group(1).strip()
    
    # Pattern 6: Extract anything before common separators
    match = re.search(r'^([^\(\)\[\]【】『』]+?)(?:\s*[\(\[\{【『]|$)', title)
    if match:
        artist = match.group(1).strip()
        if artist and len(artist) > 0:
            return artist
    
    return ""


def clean_artist_name(artist: str) -> str:
    """
    Clean artist name by removing extra whitespace and special characters.
    
    Args:
        artist: Raw artist name
        
    Returns:
        Cleaned artist name
    """
    # Remove extra whitespace
    artist = re.sub(r'\s+', ' ', artist).strip()
    
    # Remove trailing/leading special characters using the constant pattern
    pattern = f'^[^{VALID_ARTIST_CHARS}]+|[^{VALID_ARTIST_CHARS}]+$'
    artist = re.sub(pattern, '', artist)
    
    return artist


def process_raw_json(raw_data: Dict[str, Any]) -> MusicTrack:
    """
    Process raw JSON data and map it to MusicTrack schema.
    
    Args:
        raw_data: Raw JSON data from yt-dlp
        
    Returns:
        MusicTrack instance with cleaned data
    """
    # Extract basic fields
    track_id = raw_data.get('id', '')
    title = raw_data.get('title', '')
    url = raw_data.get('webpage_url', raw_data.get('url', ''))
    upload_date = raw_data.get('upload_date', '')
    
    # Extract artist from title or use uploader as fallback
    artist = extract_artist_from_title(title)
    if not artist:
        artist = raw_data.get('uploader', raw_data.get('channel', ''))
    
    # Clean artist name
    artist = clean_artist_name(artist)
    
    # Format date if needed (yt-dlp format: YYYYMMDD)
    if upload_date and len(upload_date) == 8:
        try:
            fecha = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
        except (ValueError, IndexError):
            fecha = upload_date
    else:
        fecha = upload_date
    
    return MusicTrack(
        id=track_id,
        titulo=title,
        artista=artist,
        url=url,
        fecha=fecha
    )


def clean_all_raw_files(raw_dir: Path, clean_dir: Path) -> List[MusicTrack]:
    """
    Process all JSON files in raw directory and save cleaned versions.
    
    Args:
        raw_dir: Path to directory with raw JSON files
        clean_dir: Path to directory for cleaned JSON files
        
    Returns:
        List of processed MusicTrack instances
    """
    if not raw_dir.exists():
        print(f"Raw directory does not exist: {raw_dir}")
        return []
    
    # Create clean directory if it doesn't exist
    clean_dir.mkdir(parents=True, exist_ok=True)
    
    cleaned_tracks = []
    
    # Process each JSON file in raw directory
    for json_file in raw_dir.glob('*.json'):
        print(f"Processing: {json_file.name}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            # Process the data
            track = process_raw_json(raw_data)
            cleaned_tracks.append(track)
            
            # Save cleaned data
            output_file = clean_dir / json_file.name
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(track.to_dict(), f, ensure_ascii=False, indent=2)
            
            print(f"  ✓ Cleaned and saved to: {output_file.name}")
            print(f"    Artist: {track.artista}")
            
        except Exception as e:
            print(f"  ✗ Error processing {json_file.name}: {e}")
    
    return cleaned_tracks


def main():
    """Main execution function."""
    # Set up paths
    base_dir = Path(__file__).parent.parent
    raw_dir = base_dir / 'data' / 'raw'
    clean_dir = base_dir / 'data' / 'clean'
    
    print("=" * 60)
    print("Musical Data Cleaner")
    print("=" * 60)
    print(f"Raw directory: {raw_dir}")
    print(f"Clean directory: {clean_dir}")
    print("=" * 60)
    
    # Process all files
    cleaned_tracks = clean_all_raw_files(raw_dir, clean_dir)
    
    print("=" * 60)
    print(f"Processing complete! Cleaned {len(cleaned_tracks)} tracks.")
    print("=" * 60)


if __name__ == '__main__':
    main()
