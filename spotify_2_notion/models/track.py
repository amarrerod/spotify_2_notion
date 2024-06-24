#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   track.py
@Time    :   2024/06/24 11:33:18
@Author  :   Alejandro Marrero
@Version :   1.0
@Contact :   amarrerd@ull.edu.es
@License :   (C)Copyright 2024, Alejandro Marrero
@Desc    :   None
"""

from dataclasses import dataclass


@dataclass
class Track:
    title: str
    artists: list[str]
    popularity: int
    url: str
    album: str
    duration: int
    danceability: float
    key: str
    mode: str
    tempo: float

    def to_page(self) -> dict:
        return {
            "Title": {
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {"content": self.title},
                    }
                ],
            },
            "Artist": {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": ",".join(self.artists)},
                    }
                ],
            },
            "Popularity": {"type": "number", "number": self.popularity},
            "External_URL": {"type": "url", "url": self.url},
            "Album": {
                "type": "rich_text",
                "rich_text": [{"type": "text", "text": {"content": self.album}}],
            },
            "Duration": {"type": "number", "number": self.duration},
            "Danceability": {"type": "number", "number": self.danceability},
            "Key": {
                "type": "rich_text",
                "rich_text": [{"type": "text", "text": {"content": self.key}}],
            },
            "Mode": {
                "type": "rich_text",
                "rich_text": [{"type": "text", "text": {"content": self.mode}}],
            },
            "Tempo": {"type": "number", "number": self.tempo},
        }

    @classmethod
    def from_query(cls, item, features):
        artists = list(item["artists"][i]["name"] for i in range(len(item["artists"])))
        duration = item["duration_ms"]
        minutes = (duration / (1000 * 60)) % 60
        return cls(
            title=item["name"],
            artists=artists,
            popularity=item["popularity"],
            url=item["preview_url"],
            album=item["album"]["name"],
            duration=minutes,
            danceability=features["danceability"],
            key=str(features["key"]),
            mode=str(features["mode"]),
            tempo=features["tempo"],
        )
