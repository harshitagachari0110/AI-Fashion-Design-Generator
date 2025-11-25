# AI-Fashion-Design-Generator

An interactive web application that generates AI-powered fashion design descriptions and recommends affordable products based on the user’s text prompt.

This project uses:

FastAPI (Python) → Backend API
HTML + JavaScript → Frontend
Mock product search → Display sample product suggestions
AI-based description generation → Generates fashion text output

🚀 Features
🔹 1. AI Fashion Description Generator

Users can enter any fashion prompt, such as:
pastel floral summer dress, fitted waist, midi
The backend processes the prompt and returns a structured fashion description (text or SVG in future updates).

🔹 2. Mock Product Recommendations

Based on the prompt, the backend returns a set of affordable fashion items, including:
Product name
Price
Thumbnail image
External link
This simulates a real e-commerce recommendation engine.

🔹 3. Simple & Clean Frontend

The HTML frontend:

Accepts user prompt
Sends API request to FastAPI
Shows AI-generated design output
Displays recommended products with thumbnails
No frameworks required — works in any browser.

🛠️ Tech Stack
Layer	Technology
Backend	FastAPI (Python)
Server	Uvicorn
Frontend	HTML, CSS, JavaScript
Data	Mock JSON API
Framework	Standard Web APIs (Fetch API)
📂 Project Structure
project/
│── app.py             # FastAPI backend
│── index.html         # Frontend UI
│── .venv/             # Virtual environment
└── README.md          # Project documentation

▶️ How to Run the Project
1. Install dependencies
pip install fastapi uvicorn

2. Start the FastAPI server
uvicorn app:app --reload --port 8000


Your backend will run at:

📌 http://localhost:8000

3. Open the frontend

Right-click index.html → Open with Live Server
(or double-click to open in browser)
Frontend will send requests to:
POST /generate
GET /mock-products

🧪 API Endpoints
POST /generate

Generates a fashion description.

Request:

{
  "prompt": "pastel floral dress"
}


Response:

Here is your generated fashion description...
GET /mock-products?q=...
Returns a list of affordable product suggestions.

Response:

{
  "results": [
    {
      "title": "Floral Dress – Budget Edition",
      "price": "₹499",
      "image": "https://placehold.co/80x100?text=Dress",
      "link": "https://example.com/item1"
    }
  ]
}

🎯 Future Improvements (Optional)

Add AI image generation (DALL·E / Flux / Stability)
Add real product search using Amazon Flipkart API
Add style transfer for outfits
Save and download generated fashion concepts
