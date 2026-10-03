"""
Universal Playlist Ingestion & Parser for BroCheck
Supports:
1. Spotify Links (via public oEmbed / meta scraper)
2. Apple Music Links (via public meta tags)
3. YouTube / YouTube Music Links (via oEmbed API)
4. Local files (.txt, .csv, .m3u, .json)
5. Raw text copy-paste
"""

import os
import re
import json
import requests
from typing import Optional, Dict, Any

class PlaylistParser:
    @staticmethod
    def is_url(text: str) -> bool:
        return bool(re.match(r"^https?://", text.strip(), re.IGNORECASE))

    @staticmethod
    def parse(input_data: str) -> Dict[str, Any]:
        """
        Main entry point to parse any playlist input (URL, file path, or raw text).
        """
        cleaned = input_data.strip()
        
        # 1. Check if it's a file path
        if os.path.isfile(cleaned):
            return PlaylistParser._parse_file(cleaned)
            
        # 2. Check if it's a URL
        if PlaylistParser.is_url(cleaned):
            return PlaylistParser._parse_url(cleaned)
            
        # 3. Fallback to raw text
        return {
            "source_type": "raw_text",
            "title": "Custom Tracklist",
            "tracks_text": cleaned,
            "raw_input": cleaned
        }

    @staticmethod
    def _parse_file(file_path: str) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        filename = os.path.basename(file_path)
        return {
            "source_type": "file",
            "title": filename,
            "tracks_text": content.strip(),
            "raw_input": file_path
        }

    @staticmethod
    def _parse_url(url: str) -> Dict[str, Any]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        # 1. Spotify URL
        if "spotify.com" in url:
            try:
                oembed_url = f"https://open.spotify.com/oembed?url={url}"
                resp = requests.get(oembed_url, headers=headers, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    title = data.get("title", "Spotify Playlist")
                    html_resp = requests.get(url, headers=headers, timeout=5)
                    meta_desc = ""
                    if html_resp.status_code == 200:
                        desc_match = re.search(r'<meta\s+property="og:description"\s+content="([^"]+)"', html_resp.text)
                        if desc_match:
                            meta_desc = desc_match.group(1)
                    
                    return {
                        "source_type": "spotify",
                        "title": title,
                        "tracks_text": f"Playlist: {title}\nPreview/Artists: {meta_desc}\nURL: {url}",
                        "raw_input": url
                    }
            except Exception:
                pass
            return {
                "source_type": "spotify",
                "title": "Spotify Playlist",
                "tracks_text": f"Spotify Playlist Link: {url}",
                "raw_input": url
            }

        # 2. YouTube / YouTube Music URL
        if "youtube.com" in url or "youtu.be" in url:
            try:
                oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
                resp = requests.get(oembed_url, headers=headers, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    title = data.get("title", "YouTube Playlist")
                    author = data.get("author_name", "Unknown Channel")
                    return {
                        "source_type": "youtube",
                        "title": title,
                        "tracks_text": f"YouTube Playlist: {title} by {author}\nURL: {url}",
                        "raw_input": url
                    }
            except Exception:
                pass
            return {
                "source_type": "youtube",
                "title": "YouTube Music Playlist",
                "tracks_text": f"YouTube Playlist Link: {url}",
                "raw_input": url
            }

        # 3. Apple Music
        if "music.apple.com" in url:
            try:
                resp = requests.get(url, headers=headers, timeout=5)
                title = "Apple Music Playlist"
                desc = ""
                if resp.status_code == 200:
                    title_match = re.search(r'<title>([^<]+)</title>', resp.text)
                    if title_match:
                        title = title_match.group(1).replace(" on Apple Music", "")
                    desc_match = re.search(r'<meta\s+property="og:description"\s+content="([^"]+)"', resp.text)
                    if desc_match:
                        desc = desc_match.group(1)
                return {
                    "source_type": "apple_music",
                    "title": title,
                    "tracks_text": f"Apple Music Playlist: {title}\nDetails: {desc}\nURL: {url}",
                    "raw_input": url
                }
            except Exception:
                pass

        # 4. Generic / SoundCloud / Other URLs
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            title = "Web Playlist"
            if resp.status_code == 200:
                title_match = re.search(r'<title>([^<]+)</title>', resp.text)
                if title_match:
                    title = title_match.group(1)
            return {
                "source_type": "web_url",
                "title": title,
                "tracks_text": f"Web Playlist: {title}\nURL: {url}",
                "raw_input": url
            }
        except Exception:
            return {
                "source_type": "url",
                "title": "Online Playlist",
                "tracks_text": f"Playlist Link: {url}",
                "raw_input": url
            }
