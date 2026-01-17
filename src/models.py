"""
Musical data model definition using dataclasses.
"""
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class MusicTrack:
    """
    Schema for musical track data.
    
    Attributes:
        id: Unique identifier for the track
        titulo: Title of the track
        artista: Artist name
        url: URL to the track
        fecha: Date of the track (ISO format)
    """
    id: str
    titulo: str
    artista: str
    url: str
    fecha: str
    
    def to_dict(self) -> dict:
        """Convert dataclass to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MusicTrack':
        """Create MusicTrack instance from dictionary."""
        return cls(
            id=data.get('id', ''),
            titulo=data.get('titulo', ''),
            artista=data.get('artista', ''),
            url=data.get('url', ''),
            fecha=data.get('fecha', '')
        )
