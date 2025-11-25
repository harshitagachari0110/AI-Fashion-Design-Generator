# backend/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import random
import html

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptReq(BaseModel):
    prompt: str

def prompt_to_style(prompt: str):
    """Very simple parser mapping words to colors, patterns, silhouettes."""
    p = prompt.lower()
    color = "lightblue"
    if "red" in p: color = "salmon"
    if "black" in p: color = "black"
    if "pastel" in p: color = "#ffdbe6"
    if "green" in p: color = "#8fd694"

    silhouette = "a-line"
    if "fitted" in p or "bodycon" in p: silhouette = "fitted"
    if "maxi" in p: silhouette = "maxi"
    if "jacket" in p or "coat" in p: silhouette = "jacket"

    pattern = "plain"
    if "floral" in p: pattern = "floral"
    if "stripes" in p: pattern = "stripes"
    if "polka" in p: pattern = "polka"

    return color, silhouette, pattern

def make_svg(prompt: str) -> str:
    color, silhouette, pattern = prompt_to_style(prompt)
    # sanitize
    prompt_safe = html.escape(prompt)[:200]
    width, height = 600, 900

    # Basic body & dress shapes based on silhouette
    dress_path = ""
    if silhouette == "a-line":
        dress_path = f"<path d='M200 200 C250 350, 350 350, 400 200 L420 760 Q300 840,180 760 Z' fill='{color}' stroke='black' stroke-width='2'/>"
    elif silhouette == "fitted":
        dress_path = f"<path d='M240 200 C260 300, 340 300,360 200 L360 760 Q300 800,240 760 Z' fill='{color}' stroke='black' stroke-width='2'/>"
    elif silhouette == "maxi":
        dress_path = f"<path d='M180 200 C250 340, 350 340,420 200 L460 780 Q300 860,140 780 Z' fill='{color}' stroke='black' stroke-width='2'/>"
    elif silhouette == "jacket":
        dress_path = f"<rect x='190' y='200' width='220' height='200' rx='20' fill='{color}' stroke='black' stroke-width='2'/>"

    # Add simple pattern overlays
    pattern_svg = ""
    if pattern == "stripes":
        for y in range(230, 760, 20):
            pattern_svg += f"<rect x='200' y='{y}' width='200' height='8' fill='rgba(0,0,0,0.07)' />"
    elif pattern == "polka":
        for y in range(260, 740, 40):
            for x in range(230, 430, 40):
                pattern_svg += f"<circle cx='{x}' cy='{y}' r='6' fill='rgba(0,0,0,0.08)'/>"
    elif pattern == "floral":
        # tiny stylized flowers
        for y in range(260, 740, 60):
            for x in range(230, 430, 60):
                pattern_svg += f"<circle cx='{x}' cy='{y}' r='6' fill='white'/>" \
                               f"<circle cx='{x+6}' cy='{y+6}' r='3' fill='rgba(0,0,0,0.08)'/>"

    # small "neck" and arms to look like a garment
    head = "<circle cx='300' cy='120' r='40' fill='#ffdfc4' stroke='black' stroke-width='1'/>"
    arms = "<rect x='120' y='300' width='60' height='16' rx='8' transform='rotate(-12 120 300)' fill='rgba(0,0,0,0.04)'/>" \
           "<rect x='420' y='300' width='60' height='16' rx='8' transform='rotate(12 420 300)' fill='rgba(0,0,0,0.04)'/>"

    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
    <rect width='100%' height='100%' fill='white'/>
    {head}
    {arms}
    {dress_path}
    {pattern_svg}
    <text x='20' y='880' font-family='Arial' font-size='14'>Prompt: {prompt_safe}</text>
    </svg>"""
    return svg

@app.post("/generate")
async def generate(req: PromptReq):
    svg = make_svg(req.prompt)
    # Return raw svg text (frontend can embed it)
    return PlainTextResponse(content=svg, media_type="image/svg+xml")

@app.get("/mock-products")
async def mock_products(q: str):
    """Return mocked product suggestions (in real version you'd integrate a product search API)."""
    # create 5 mock affordable product entries
    items = []
    colors = ["black", "white", "blue", "green", "red", "pastel"]
    for i in range(5):
        items.append({
            "title": f"{q.title()} — affordable option #{i+1}",
            "price": f"₹{499 + 200*i}",
            "link": f"https://example.com/search?q={q.replace(' ','+')}&r={i}",
            "image": f"https://placehold.co/200x250/{random.choice(colors)}/fff?text=Item+{i+1}"
        })
    return {"query": q, "results": items}
@app.get("/")
def home():
    return {"message": "AI Fashion Design Generator API is running!"}
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Home route
@app.get("/")
def home():
    return {"message": "AI Fashion Design Generator API is running!"}

# Input model
class Prompt(BaseModel):
    text: str

# AI generator route
@app.post("/generate")
def generate_design(prompt: Prompt):
    # Dummy output for now (later we add real AI)
    svg_design = f"""
    <svg width="200" height="300" xmlns="http://www.w3.org/2000/svg">
        <rect width="200" height="300" fill="lightpink"/>
        <text x="10" y="150" font-size="14">Design: {prompt.text}</text>
    </svg>
    """
    return {"svg": svg_design}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Fashion Design Generator API is running!"}

@app.post("/generate")
async def generate_design(data: dict):
    prompt = data.get("prompt", "")

    svg = f"""
    <svg width="300" height="500" xmlns="http://www.w3.org/2000/svg">
      <rect width="300" height="500" fill="#f8f8f8" />
      <text x="20" y="50" font-size="20" fill="black">
        Design based on: {prompt}
      </text>
      <rect x="60" y="100" width="180" height="300" fill="pink" stroke="black" />
    </svg>
    """
    return svg

@app.get("/mock-products")
async def mock_products(q: str):
    return {
        "results": [
            {
                "title": "Floral Dress – Budget Edition",
                "price": "₹499",
                "image": "https://placehold.co/80x100?text=Dress",
                "link": "https://example.com/item1"
            },
            {
                "title": "Pastel Summer Dress",
                "price": "₹699",
                "image": "https://placehold.co/80x100?text=Pastel",
                "link": "https://example.com/item2"
            },
            {
                "title": "Cute Midi Dress",
                "price": "₹599",
                "image": "https://placehold.co/80x100?text=Midi",
                "link": "https://example.com/item3"
            }
        ]
    }
