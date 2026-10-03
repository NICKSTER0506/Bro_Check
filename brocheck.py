#!/usr/bin/env python3
"""
BroCheck 🔥 — The Open-Source AI Roaster CLI
Build for a Friend | Hacktoberfest 2026 (HF26) DEV Challenge
"""

import sys
import os
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.table import Table
from rich import box

from engine.prompts import PERSONAS, HEAT_LEVELS, build_roast_prompt
from engine.playlist_parser import PlaylistParser
from engine.github_fetcher import GitHubFetcher
from engine.llm_client import OpenAIEngine

console = Console()

BANNER = r"""[bold red]
  ____  _____   ____   _____ _    _ ______ _____ _  __
 |  _ \|  __ \ / __ \ / ____| |  | |  ____/ ____| |/ /
 | |_) | |__) | |  | | |    | |__| | |__ | |    | ' / 
 |  _ <|  _  /| |  | | |    |  __  |  __|| |    |  <  
 | |_) | | \ \| |__| | |____| |  | | |___| |____| . \ 
 |____/|_|  \_\\____/ \_____|_|  |_|______\_____|_|\_\
                                   [bold yellow]🔥 Open-Source AI Edition 🔥[/bold yellow]
[/bold red]"""

def print_header():
    console.print(BANNER)
    console.print(
        "[bold cyan]🎯 HF26 Challenge 'Build for a Friend'[/bold cyan] | "
        "[bold green]🪶 0 MB RAM Overhead[/bold green] | "
        "[bold magenta]⚡ Open-Weight AI Core[/bold magenta]\n"
    )

def interactive_wizard():
    print_header()
    
    # 1. Mode Selection
    table = Table(title="Select What You Want to BroCheck 🔥", box=box.ROUNDED, header_style="bold magenta")
    table.add_column("Key", style="bold yellow", width=5)
    table.add_column("Category", style="bold white", width=22)
    table.add_column("Supported Inputs", style="dim cyan")
    
    table.add_row("1", "🎵 Music Playlist", "Spotify / Apple / YT link, .txt/.csv file, or artist list")
    table.add_row("2", "💻 Code File", "Path to any .py, .js, .ts, .cpp, or code snippet")
    table.add_row("3", "🐙 GitHub Profile", "GitHub username (fetches repos, stars & bio)")
    table.add_row("4", "📱 Bio / Status", "WhatsApp status, Instagram bio, LinkedIn buzzwords")
    table.add_row("5", "💬 Friend Excuse", "Texts from group chats, late arrival excuses")
    table.add_row("6", "🎮 Gaming / Steam", "List of games, 3,000 hrs in Bronze rank")
    table.add_row("7", "🔮 Custom Anything", "Paste literally any text or screenshot OCR")
    
    console.print(table)
    mode_choice = Prompt.ask("\nChoose category", choices=["1", "2", "3", "4", "5", "6", "7"], default="1")
    
    mode_map = {
        "1": "playlist",
        "2": "code",
        "3": "github",
        "4": "bio",
        "5": "excuse",
        "6": "games",
        "7": "custom"
    }
    selected_mode = mode_map[mode_choice]

    # 2. Input Retrieval
    content = ""
    if selected_mode == "playlist":
        raw_in = Prompt.ask("\n[bold yellow]🎵 Drop playlist URL, file path, or song list[/bold yellow]")
        parsed = PlaylistParser.parse(raw_in)
        content = parsed["tracks_text"]
        console.print(f"[green]✓ Ingested from: {parsed['source_type']} ({parsed['title']})[/green]")
        
    elif selected_mode == "code":
        file_path = Prompt.ask("\n[bold yellow]💻 Enter path to code file (e.g. sample.py)[/bold yellow]")
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            console.print(f"[green]✓ Read {len(content.splitlines())} lines from {os.path.basename(file_path)}[/green]")
        else:
            console.print("[red]File not found! Using raw text instead.[/red]")
            content = file_path
            
    elif selected_mode == "github":
        username = Prompt.ask("\n[bold yellow]🐙 Enter GitHub username (e.g. octocat)[/bold yellow]")
        with console.status("[cyan]Fetching public GitHub profile & repos...[/cyan]"):
            res = GitHubFetcher.fetch_profile(username)
        if res["success"]:
            content = res["summary"]
            console.print(f"[green]✓ Successfully fetched GitHub stats for @{res['username']}[/green]")
        else:
            console.print(f"[yellow]Warning: {res['error']}. Proceeding with handle name.[/yellow]")
            content = f"GitHub User: @{username}"
            
    elif selected_mode == "bio":
        content = Prompt.ask("\n[bold yellow]📱 Paste the social bio or status text[/bold yellow]")
    elif selected_mode == "excuse":
        content = Prompt.ask("\n[bold yellow]💬 Paste the friend's excuse or chat message[/bold yellow]")
    elif selected_mode == "games":
        content = Prompt.ask("\n[bold yellow]🎮 Paste game list or steam library stats[/bold yellow]")
    else:
        content = Prompt.ask("\n[bold yellow]🔮 Paste the text to roast[/bold yellow]")

    # 3. Persona Selection
    console.print("\n[bold cyan]Select Roaster Persona:[/bold cyan]")
    for k, v in PERSONAS.items():
        console.print(f" • [bold yellow]{k}[/bold yellow]: {v['name']} — [dim]{v['desc']}[/dim]")
    persona = Prompt.ask("\nChoose Persona", choices=list(PERSONAS.keys()), default="bestfriend")

    # 4. Heat Level Selection
    console.print("\n[bold cyan]Select Heat Level:[/bold cyan]")
    for k, v in HEAT_LEVELS.items():
        console.print(f" • [bold red]{k}[/bold red]: {v['name']} — [dim]{v['instruction']}[/dim]")
    heat = Prompt.ask("\nChoose Heat", choices=list(HEAT_LEVELS.keys()), default="spicy")

    # 5. Execute Roast
    execute_and_display_roast(selected_mode, content, heat, persona)

def execute_and_display_roast(mode: str, content: str, heat: str, persona: str):
    system_prompt, user_prompt = build_roast_prompt(mode, content, heat, persona)
    
    with console.status("[bold red]🔥 Running BroCheck with Open-Weight AI...[/bold red]", spinner="bouncingBall"):
        engine = OpenAIEngine()
        roast_text = engine.generate_roast(system_prompt, user_prompt)
        
    p_name = PERSONAS.get(persona, {}).get("name", persona)
    h_name = HEAT_LEVELS.get(heat, {}).get("name", heat)
    
    console.print("\n")
    panel_title = f"[bold red]🔥 BROCHECK RESULTS: {p_name} ({h_name}) 🔥[/bold red]"
    
    console.print(
        Panel(
            Markdown(roast_text),
            title=panel_title,
            border_style="bold red",
            padding=(1, 2)
        )
    )
    console.print("\n[bold yellow]💡 Tip:[/bold yellow] Copy-paste this roast to your friend, or screenshot for group chats! 😈\n")

def main():
    parser = argparse.ArgumentParser(description="BroCheck 🔥 — Open-Source AI Roaster CLI")
    parser.add_argument("--mode", "-m", choices=["playlist", "code", "github", "bio", "excuse", "games", "custom"], help="Roast mode")
    parser.add_argument("--input", "-i", type=str, help="Input string (text, URL, or GitHub username)")
    parser.add_argument("--file", "-f", type=str, help="Path to file to roast (playlist file or code file)")
    parser.add_argument("--heat", choices=["mild", "spicy", "nuclear"], default="spicy", help="Heat level")
    parser.add_argument("--persona", "-p", choices=list(PERSONAS.keys()), default="bestfriend", help="Roaster persona")
    
    args = parser.parse_args()
    
    # If no flags passed, launch interactive wizard
    if not args.mode:
        interactive_wizard()
        return

    # Direct CLI flag mode
    content = ""
    if args.file and os.path.isfile(args.file):
        if args.mode == "playlist":
            parsed = PlaylistParser.parse(args.file)
            content = parsed["tracks_text"]
        else:
            with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
    elif args.input:
        if args.mode == "playlist":
            parsed = PlaylistParser.parse(args.input)
            content = parsed["tracks_text"]
        elif args.mode == "github":
            res = GitHubFetcher.fetch_profile(args.input)
            content = res["summary"] if res["success"] else f"GitHub User: @{args.input}"
        else:
            content = args.input
    else:
        console.print("[red]Error: You must provide either --input or --file when using CLI flags.[/red]")
        sys.exit(1)

    print_header()
    execute_and_display_roast(args.mode, content, args.heat, args.persona)

if __name__ == "__main__":
    main()
