# VeganAI: Project Overview & Technical Report

## 1. Project Mission
VeganAI is a **Multimodal Precision Nutrition Assistant** designed to eliminate the guesswork from plant-based living. It leverages cutting-edge Artificial Intelligence to provide personalized, scientifically-backed nutritional insights, local ingredient analysis, and gourmet recipe generation tailored to specific health goals.

## 2. Core Technology Stack
*   **Backend**: 
    *   **FastAPI (Python)**: High-performance web framework for handling API requests and business logic.
    *   **Uvicorn**: ASGI server for running the FastAPI application.
*   **AI Engine (Multimodal Intelligence)**:
    *   **Google Gemini 2.0 Flash**: Handles complex text generation, nutritional calculations, and AI Vision (ingredient scanning).
    *   **Imagen 3.0**: Powers real-time professional food photography generation for recipes.
    *   **Groq (Llama-3.3-70b)**: High-speed inference for recipe analysis and dietitian personality.
*   **Database**: 
    *   **SQLite**: Lightweight, persistent storage for recipe history and user preferences.
*   **Frontend**:
    *   **HTML5/JavaScript**: Core structure and interactive logic.
    *   **Vanilla CSS**: Custom-built design system featuring **Glassmorphism**, botanical aesthetics, and responsive layouts.
    *   **Chart.js**: Dynamic visualization of macro and micro-nutrients.
    *   **jsPDF**: Client-side generation of nutritional reports.

## 3. Key Features
*   **Precision Recipe Generation**: Creates high-end vegan recipes with a full breakdown of protein, carbs, fats, fiber, and sodium.
*   **AI Vision Scanning**: Allows users to upload photos of raw ingredients to receive instant dish suggestions (powered by `DISHTAG` technology).
*   **Personalization Engine**: Tracks user-specific data including BMI, health focuses (e.g., Anemia, Diabetes), and activity levels to refine advice.
*   **Smart History Management**: Automatically saves and restores recent meal analyses from the local database.
*   **Multimodal Interaction**: Supports text-based craving entry, image uploads, and voice-to-text queries.
*   **Premium Landing Page**: A high-impact entry point featuring an interactive hero section and educational content regarding the benefits of veganism.

## 4. Design System & Aesthetics
The project follows a **Rich Botanical Aesthetic**, emphasizing its "Vegan" identity through visuals:
*   **4K High-Res Imagery**: Uses stunning, high-definition botanical and herbal backgrounds (2560px width) across the dashboard and landing page.
*   **Glassmorphism**: UI elements use advanced translucency (`backdrop-filter: blur(20px)`) and semi-transparent white borders to appear "floating" over the nature-themed wallpaper.
*   **Modern Typography**: Utilizes "Outfit", "Inter", and "Manrope" fonts for a clean, premium, and readable experience.
*   **Micro-animations**: Subtle hover transitions on cards and buttons enhance the "living" feel of the application.

## 5. Recent Upgrades
*   **Background Overhaul**: Transitioned from simple gradients to high-resolution floral wallpapers tailored to be "soothing and attractive."
*   **Resolution Optimization**: Upgraded all external assets to 4K resolution via Unsplash API integration.
*   **Compatibility Fixes**: Standardized CSS properties (like `background-clip`) for cross-browser stability.
*   **UI Polish**: Enhanced recommendation cards with glassmorphism for a more integrated and modern dashboard look.
