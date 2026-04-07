from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from pydantic import BaseModel
import brain

class UserInput(BaseModel):
    name: str
    goal: str
    allergies: str
    craving: str

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en" id="htmlTag">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VeganAI | Precision Nutrition</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
        
        <style>
            :root {
                --bg-gradient: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                --card-bg: rgba(255, 255, 255, 0.9);
                --text-main: #0f172a;
                --input-bg: #ffffff;
                --border-color: #cbd5e1;
                --accent: #16a34a;
            }

            [data-theme='dark'] {
                --bg-gradient: linear-gradient(135deg, #020617 0%, #0f172a 100%);
                --card-bg: rgba(30, 41, 59, 0.7);
                --text-main: #f8fafc;
                --input-bg: #1e293b;
                --border-color: #334155;
                --accent: #22c55e;
            }

            body { 
                font-family: 'Plus Jakarta Sans', sans-serif; 
                background: var(--bg-gradient); color: var(--text-main);
                min-height: 100vh; display: flex; flex-direction: column; align-items: center; transition: 0.4s;
            }

            .glass-card { background: var(--card-bg); backdrop-filter: blur(12px); border: 1px solid var(--border-color); }
            
            .input-field { 
                background: var(--input-bg); border: 1px solid var(--border-color); 
                color: var(--text-main); width: 100%; border-radius: 0.75rem; padding: 0.8rem;
            }

            .theme-btn { position: fixed; top: 20px; right: 20px; padding: 12px; cursor: pointer; }
            
            .error-box { 
                color: #ef4444; background: rgba(239, 68, 68, 0.1); 
                padding: 1rem; border-radius: 0.75rem; border: 1px solid rgba(239, 68, 68, 0.2);
            }
        </style>
    </head>
    <body class="p-6">
        <button class="theme-btn glass-card rounded-full" onclick="toggleTheme()">🌓</button>
        
        <div class="max-w-3xl w-full mt-10">
            <div class="glass-card rounded-[2.5rem] p-10 shadow-2xl">
                
                <div class="flex items-center gap-4 mb-10">
                    <div id="iconContainer" class="bg-green-600 w-16 h-16 rounded-2xl flex items-center justify-center shadow-lg">
                        <span id="staticEmoji" class="text-3xl">🌿</span>
                        <dotlottie-player id="lottieAnim" 
                            src="https://lottie.host/7864758b-306b-432a-949e-f082e6d6232d/6pS3Y1XvLg.json" 
                            speed="1" style="width: 50px; height: 50px; display: none;" loop autoplay>
                        </dotlottie-player>
                    </div>
                    <div>
                        <h1 class="text-3xl font-extrabold tracking-tight">VeganAI</h1>
                        <p class="text-green-600 font-bold text-xs uppercase tracking-widest">Precision Nutrition Assistant</p>
                    </div>
                </div>

                <div class="space-y-4 mb-8">
                    <div class="grid grid-cols-2 gap-4">
                        <input type="text" id="userName" placeholder="Your Name" class="input-field">
                        <select id="healthIssue" class="input-field">
                            <option value="General">General Health</option>
                            <option value="Anemia">Anemia</option>
                            <option value="Diabetes">Diabetes</option>
                            <option value="Hypertension">Hypertension</option>
                        </select>
                    </div>
                    <textarea id="notes" placeholder="Any allergies?" class="input-field h-20 resize-none"></textarea>
                    <div class="flex gap-3">
                        <input type="text" id="craving" placeholder="What are you craving?" class="input-field text-lg">
                        <button onclick="getAdvice()" id="btn" class="bg-green-600 text-white px-8 py-4 rounded-xl font-bold hover:bg-green-700 transition-all">
                            Get Advice
                        </button>
                    </div>
                </div>

                <div id="result" class="hidden">
                    <div class="p-6 rounded-2xl border-2 border-dashed border-slate-300 dark:border-slate-600 mb-8">
                        <div id="aiText" class="whitespace-pre-wrap leading-relaxed text-lg"></div>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                        <canvas id="nutrientChart"></canvas>
                        <button onclick="exportPDF()" class="w-full bg-slate-900 dark:bg-white dark:text-slate-900 text-white py-4 rounded-xl font-black">
                            📥 Download Report
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let myChart = null;

            function toggleTheme() {
                const html = document.getElementById('htmlTag');
                html.hasAttribute('data-theme') ? html.removeAttribute('data-theme') : html.setAttribute('data-theme', 'dark');
                if (myChart) updateChart();
            }

            async function getAdvice() {
                const craving = document.getElementById('craving').value;
                const btn = document.getElementById('btn');
                const aiText = document.getElementById('aiText');
                const emoji = document.getElementById('staticEmoji');
                const anim = document.getElementById('lottieAnim');

                if (!craving) return;

                // UI Loading State
                emoji.style.display = 'none'; anim.style.display = 'block';
                btn.innerText = "Analyzing..."; btn.disabled = true;

                try {
                    const response = await fetch('/generate-recipe/', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            current_craving: craving,
                            health_context: document.getElementById('healthIssue').value 
                        })
                    });

                    const data = await response.json();
                    
                    // FIX: Check for the exact key returned by brain.py
                    if (data.ai_recommendation) {
                        if (data.ai_recommendation.includes("Busy") || data.ai_recommendation.includes("Quota")) {
                            aiText.innerHTML = `<div class="error-box">${data.ai_recommendation}</div>`;
                        } else {
                            aiText.innerText = data.ai_recommendation;
                        }
                    } else {
                        aiText.innerText = "Error: Backend returned undefined data.";
                    }
                    
                    document.getElementById('result').classList.remove('hidden');
                    updateChart();

                } catch (e) {
                    aiText.innerText = "Server connection lost. Please check your terminal.";
                } finally {
                    emoji.style.display = 'block'; anim.style.display = 'none';
                    btn.innerText = "Get Advice"; btn.disabled = false;
                }
            }

            function updateChart() {
                const isDark = document.getElementById('htmlTag').hasAttribute('data-theme');
                const ctx = document.getElementById('nutrientChart').getContext('2d');
                if (myChart) myChart.destroy();
                myChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Iron', 'B12', 'Protein'],
                        datasets: [{ data: [15, 10, 25], backgroundColor: ['#3b82f6', '#8b5cf6', '#22c55e'] }]
                    },
                    options: { plugins: { legend: { labels: { color: isDark ? '#fff' : '#000' } } } }
                });
            }

            function exportPDF() {
                const { jsPDF } = window.jspdf;
                const doc = new jsPDF();
                doc.text(document.getElementById('aiText').innerText, 20, 20);
                doc.save("VeganAI_Report.pdf");
            }
        </script>
    </body>
    </html>
    """

@app.post("/generate-recipe/")
async def generate_recipe(user_input: UserInput):
    # 🛑 BACKEND VALIDATION
    if not user_input.name or not user_input.craving:
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    try:
        # Your existing code to call brain.py
        recipe = brain.get_recipe_from_ai(user_input)
        return {"ai_recommendation": recipe}
    except Exception as e:
        return {"ai_recommendation": "Sorry, I encountered an error. Please try again."}

@app.get("/dashboard")
async def read_dashboard():
    # This is your actual AI Dietitian page
    return FileResponse("templates/index.html")

@app.get("/generate-image/")
async def get_meal_image(meal_name: str):
    # This calls the new function in brain.py
    image_data = brain.generate_meal_image(meal_name)
    return image_data

@app.post("/login")
async def login_user(username: str, password: str):
    # This is where we check the database
    # For now, we can 'mock' it for your demo:
    if username == "admin" and password == "1234":
        return {"status": "success", "message": "Welcome, Tripti!"}
    else:
        raise HTTPException(status_code=401, detail="Invalid Credentials")