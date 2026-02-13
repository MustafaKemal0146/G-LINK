import os
import json
import httpx
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import google.generativeai as genai
from rich.console import Console

app = FastAPI()
console = Console()

# Configuration
GEMINI_API_KEY = "AIzaSyAunqM4G8lRgQRlQ1vMBk1E1B-wYWfkw8E"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro-latest')

@app.post("/v1/messages")
@app.post("/v1/v1/messages")
async def messages_proxy(request: Request):
    """Bridge between Anthropic Schema and Gemini AI Studio"""
    try:
        anthropic_data = await request.json()
        requested_model = anthropic_data.get("model", "claude-3-5-sonnet-20241022")
        console.log(f"[bold cyan]G-LINK:[/bold cyan] Incoming request for {requested_model}")
        
        # 1. Translate Anthropic to Gemini
        messages = anthropic_data.get("messages", [])
        
        gemini_messages = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            content = msg["content"]
            if isinstance(content, list):
                text_parts = [item["text"] for item in content if item["type"] == "text"]
                content = " ".join(text_parts)
            
            gemini_messages.append({"role": role, "parts": [content]})
            
        # 2. Call Gemini
        chat = model.start_chat(history=gemini_messages[:-1])
        response = chat.send_message(gemini_messages[-1]["parts"][0])
        
        # 3. Translate Gemini back to Anthropic
        anthropic_response = {
            "id": f"msg_{os.urandom(8).hex()}",
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": response.text}],
            "model": requested_model,
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 100, 
                "output_tokens": 100
            }
        }
        
        console.log(f"[bold green]G-LINK:[/bold green] Successfully bridged to Gemini")
        return JSONResponse(content=anthropic_response)

    except Exception as e:
        console.log(f"[bold red]Error in G-LINK Bridge:[/bold red] {str(e)}")
        return JSONResponse(content={"error": {"type": "api_error", "message": str(e)}}, status_code=500)

@app.post("/v1/messages/count_tokens")
@app.post("/v1/v1/messages/count_tokens")
async def count_tokens_proxy(request: Request):
    """Mock token counting for the CLI"""
    return JSONResponse(content={"input_tokens": 100})

@app.get("/v1/models")
async def list_models():
    return {
        "data": [
            {"id": "claude-sonnet-4-5-20250929", "type": "model"},
            {"id": "claude-3-5-sonnet-20241022", "type": "model"},
            {"id": "claude-3-5-opus-20240229", "type": "model"}
        ]
    }

if __name__ == "__main__":
    console.print("[bold red]G-LINK BRIDGE ACTIVE[/bold red]")
    console.print("[yellow]Redirecting Claude Code to Google Gemini AI Studio...[/yellow]")
    uvicorn.run(app, host="127.0.0.1", port=11435)
