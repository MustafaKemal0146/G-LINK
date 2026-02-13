import asyncio
import os
import sys
import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
import pyfiglet

# Configuration
API_KEY = "AIzaSyAunqM4G8lRgQRlQ1vMBk1E1B-wYWfkw8E"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro-latest')

console = Console()

class GLinkStandalone:
    """Standalone CLI for G-LINK - Direct Gemini Interface"""
    
    def __init__(self):
        self.history = []

    def print_banner(self):
        f = pyfiglet.Figlet(font='slant')
        banner = f.renderText('G-LINK')
        console.print(Panel(banner, border_style="bold red", subtitle="[bold yellow]Mustafa Kemal Cingil Edition[/bold yellow]"))

    async def run(self):
        self.print_banner()
        chat = model.start_chat(history=[])
        
        while True:
            user_input = Prompt.ask("[bold cyan]G-LINK[/bold cyan] >")
            if user_input.lower() in ['exit', 'q']: break
                
            with console.status("[bold green]Gemini is processing...[/bold green]"):
                response = chat.send_message(user_input)
                
            console.print(Panel(Markdown(response.text), title="[bold red]Gemini 1.5 Pro[/bold red]", border_style="red"))

if __name__ == "__main__":
    glink = GLinkStandalone()
    asyncio.run(glink.run())
