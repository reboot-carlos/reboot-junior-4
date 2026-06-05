import os
import pathlib
import anthropic
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional
import uuid

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
load_dotenv()

_api_key = os.getenv("ANTHROPIC_API_KEY")
_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    """Lazy client init — raises HTTP 503 with a helpful message if the key is missing."""
    global _client
    if _client is None:
        if not _api_key or _api_key == "sk-ant-REMPLACE_MOI":
            raise HTTPException(
                status_code=503,
                detail="ANTHROPIC_API_KEY non configurée. Ajoute-la dans Railway → Variables.",
            )
        _client = anthropic.Anthropic(api_key=_api_key)
    return _client

# ─────────────────────────────────────────────
# RÔLES DISPONIBLES
# ─────────────────────────────────────────────
ROLES = {
    "assistant": {
        "id": "assistant",
        "name": "NovAI",
        "emoji": "🤖",
        "description": "Assistant Conversationnel",
        "tags": ["✨ IA", "🧠 Intelligent", "🚀 Rapide"],
        "greeting": "Comment puis-je t'aider aujourd'hui ?",
        "system_prompt": """Tu es NovAI, un assistant IA intelligent, sympa et pédagogique.
Tu réponds toujours en français, de façon claire et concise.
Tu es enthousiaste, bienveillant, et tu expliques les choses simplement.
Tu gardes tes réponses courtes (2-3 phrases) sauf si on te demande plus de détails.
Tu utilises des emojis avec modération pour rester sympathique. 🤖"""
    },
    "mentor": {
        "id": "mentor",
        "name": "Mentor IA",
        "emoji": "👨‍🏫",
        "description": "Professeur Particulier",
        "tags": ["📚 Pédagogue", "🎯 Structuré", "✏️ Patient"],
        "greeting": "Je suis là pour t'aider à apprendre. Qu'aimerais-tu étudier ?",
        "system_prompt": """Tu es un mentor pédagogique patient et structuré.
Tu expliques les concepts de manière progressive et logique.
Tu poses des questions pour vérifier la compréhension.
Tu fournis des exemples concrets et accessibles.
Tu encourages l'apprenant et célèbres ses progrès."""
    },
    "creative": {
        "id": "creative",
        "name": "Muse Créative",
        "emoji": "🎨",
        "description": "Brainstorming & Créativité",
        "tags": ["💡 Innovant", "🎭 Imaginatif", "✨ Inspirant"],
        "greeting": "Libérons ta créativité ! De quoi veux-tu parler ?",
        "system_prompt": """Tu es une muse créative qui inspire et stimule l'imagination.
Tu encourages l'exploration d'idées nouvelles et audacieuses.
Tu fournis des perspectives innovantes et originales.
Tu utilises des métaphores et des analogies pour enrichir les échanges.
Tu célèbres la créativité et les idées non-conventionnelles."""
    },
    "analyst": {
        "id": "analyst",
        "name": "Analyste Logique",
        "emoji": "🔬",
        "description": "Analyse & Raisonnement",
        "tags": ["🧮 Logique", "📊 Analytique", "🎯 Précis"],
        "greeting": "Analysons cela ensemble. Quel problème dois-je examiner ?",
        "system_prompt": """Tu es un analyste logique et précis.
Tu décomposes les problèmes complexes en éléments simples.
Tu fournis des analyses structurées et basées sur la logique.
Tu identifies les causes racines et les implications.
Tu exprimes tes conclusions avec rigueur et clarté."""
    },
    "senior_dev": {
        "id": "senior_dev",
        "name": "Dev Senior",
        "emoji": "👨‍💼",
        "description": "Expert en Architecture & Code",
        "tags": ["💻 Code", "🏗️ Architecture", "🎯 Expert"],
        "greeting": "Bienvenue ! Je suis un développeur senior. Comment puis-je t'aider avec ton projet ou architecture ?",
        "system_prompt": """Tu es un développeur senior expérimenté avec 10+ ans d'expérience.
Tu es spécialisé en architecture logicielle, patterns de design, et best practices.
Tu aides les développeurs à écrire du code propre, maintenable et performant.
Tu expliques les concepts complexes de manière pédagogique avec des exemples concrets.
Tu donnes des conseils pragmatiques, pas juste théoriques.
Tu reviewes du code avec rigueur en cherchant bugs, performance, sécurité et maintenabilité.
Tu proposes des refactorisations intelligentes et expliques pourquoi.
Tu fais attention aux détails : erreurs de typage, gestion d'erreurs, edge cases.
Tu dis "je ne sais pas" plutôt que de inventer une réponse.
Tu adaptes ton niveau d'explication au contexte (junior/senior/expert).
Ton ton est direct mais bienveillant. Tu encourages l'apprentissage."""
    }
}

# ─────────────────────────────────────────────
# Intégrations externes : Steam & GameBanana
# ─────────────────────────────────────────────

def trouver_app_id_steam(nom_jeu: str) -> str:
    """Cherche l'App ID d'un jeu Steam en fonction de son nom."""
    try:
        import json
        import re
        url = "https://steamcommunity.com/actions/SearchGames/"
        params = {"term": nom_jeu.lower()}
        reponse = requests.get(url, params=params, timeout=5)
        reponse.raise_for_status()
        results = reponse.json()
        if results and len(results) > 0:
            return str(results[0].get("appid"))
        return None
    except:
        return None


def recuperer_avis_utilisateurs(app_id: str) -> str:
    """Récupère les statistiques d'avis des utilisateurs."""
    try:
        url = f"https://steamcommunity.com/gloo/ratings/app/{app_id}/json/"
        reponse = requests.get(url, timeout=3)
        data = reponse.json()
        if "recommendations" in data:
            rec = data["recommendations"]
            total = rec.get("total", 0)
            positive = rec.get("positive", 0)
            negative = rec.get("negative", 0)
            if total > 0:
                pct_positif = (positive / total) * 100
                resultats = f"\n📊 **Avis des utilisateurs:**\n"
                resultats += f"• **Avis positifs:** {positive:,} ({pct_positif:.1f}%)\n"
                resultats += f"• **Avis négatifs:** {negative:,} ({100-pct_positif:.1f}%)\n"
                resultats += f"• **Total avis:** {total:,}"
                return resultats
        return ""
    except:
        return ""


def chercher_jeu_steam(nom_jeu: str) -> str:
    """Récupère les détails d'un jeu Steam par son nom."""
    try:
        app_id = trouver_app_id_steam(nom_jeu)
        if not app_id:
            return f"❌ Aucun jeu trouvé pour '{nom_jeu}' sur Steam"
        url = "https://store.steampowered.com/api/appdetails"
        params = {"appids": app_id}
        reponse = requests.get(url, params=params, timeout=5)
        reponse.raise_for_status()
        data = reponse.json()
        if app_id not in data or not data[app_id].get("success"):
            return f"❌ Détails non disponibles pour '{nom_jeu}'"
        game_data = data[app_id].get("data", {})
        nom = game_data.get("name", "N/A")
        prix = game_data.get("price_overview", {}).get("final_formatted", "Gratuit")
        score = game_data.get("metacritic", {}).get("score", "N/A")
        avis_positifs = game_data.get("total_positive_reviews", 0)
        avis_negatifs = game_data.get("total_negative_reviews", 0)
        description = game_data.get("short_description", "")[:100]
        resultats = f"🎮 **{nom}**\n"
        resultats += f"• **Prix:** {prix}\n"
        resultats += f"• **Score Metacritic:** {score}\n"
        if avis_positifs > 0 or avis_negatifs > 0:
            total_avis = avis_positifs + avis_negatifs
            pct_positif = (avis_positifs / total_avis) * 100 if total_avis > 0 else 0
            resultats += f"• **Avis positifs:** {avis_positifs:,}\n"
            resultats += f"• **Avis négatifs:** {avis_negatifs:,}\n"
            resultats += f"• **Pourcentage positif:** {pct_positif:.1f}%\n"
            resultats += f"• **Total avis:** {total_avis:,}\n"
        avis_supps = recuperer_avis_utilisateurs(app_id)
        if avis_supps:
            resultats += avis_supps + "\n"
        if description:
            resultats += f"• **Description:** {description}...\n"
        return resultats
    except Exception as e:
        return f"⚠️ Erreur en cherchant le jeu: {str(e)[:50]}"


def chercher_mods_gamebanana(query: str) -> str:
    """Cherche des mods sur GameBanana et retourne les résultats."""
    try:
        url = "https://api.gamebanana.com/Game/25/Mods/LatestModifications"
        reponse = requests.get(url, timeout=5)
        reponse.raise_for_status()
        mods = reponse.json()
        if not mods:
            return "Aucun mod trouvé pour cette recherche."
        resultats = f"📦 **Mods GameBanana (recherche: {query}):**\n"
        for mod in mods[:3]:
            if isinstance(mod, (list, tuple)) and len(mod) > 0:
                nom = mod[1] if len(mod) > 1 else "N/A"
                resultats += f"\n• {nom}"
            elif isinstance(mod, dict):
                nom = mod.get("name") or mod.get("_sName", "N/A")
                resultats += f"\n• {nom}"
        return resultats
    except Exception:
        return "📦 **Mods GameBanana (exemple):**\n• Skyrim Mod 1\n• Minecraft Mod 2\n• GTA V Mod 3\n\n(Remarque: L'API GameBanana a des limitations)"


# /app in Docker, chatbot-new/ locally — parent of backend/
STATIC_DIR = pathlib.Path(__file__).parent.parent

# ─────────────────────────────────────────────
# Initialisation FastAPI
# ─────────────────────────────────────────────
app = FastAPI(
    title="NovAI API",
    description="L'API de NovAI — Chatbot avec gestion des rôles",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Modèles de données
# ─────────────────────────────────────────────
class Message(BaseModel):
    texte: str
    role_id: Optional[str] = "assistant"

class Reponse(BaseModel):
    reponse: str
    nb_messages: int

class RoleResponse(BaseModel):
    id: str
    name: str
    emoji: str
    description: str
    tags: list[str]
    greeting: str

# ─────────────────────────────────────────────
# État de l'application
# ─────────────────────────────────────────────
historique: list[dict] = []
roles_custom: dict = {}

# ─────────────────────────────────────────────
# Fonctions utilitaires
# ─────────────────────────────────────────────
def obtenir_role(role_id: str) -> dict:
    """Récupère un rôle (custom ou pré-défini)"""
    if role_id in roles_custom:
        return roles_custom[role_id]
    return ROLES.get(role_id, ROLES["assistant"])

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.get("/health")
def health():
    """Vérifie que l'API fonctionne."""
    return {"message": "NovAI API est en ligne 🤖", "version": "3.0.0", "model": "claude-opus-4-8"}

@app.get("/")
def serve_index():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/home")
def serve_home():
    return FileResponse(STATIC_DIR / "home.html")

@app.post("/chat", response_model=Reponse)
def chat(message: Message):
    """Envoie un message à Claude avec le rôle actif."""
    if not message.texte.strip():
        return Reponse(reponse="Envoie-moi un message !", nb_messages=len(historique))

    # Obtenir le rôle actif
    role = obtenir_role(message.role_id or "assistant")

    # Détection de mots-clés et enrichissement avec données externes
    texte_lower = message.texte.lower()
    donnees_externes = ""

    if any(w in texte_lower for w in ["steam", "jeu", "prix", "game", "détails", "combien", "coûte"]):
        nom_jeu = message.texte
        for w in ["steam", "sur steam", "coûte", "prix", "détails", "parle-moi", "montre-moi", "cherche"]:
            nom_jeu = nom_jeu.lower().replace(w, "").strip()
        if nom_jeu and len(nom_jeu) > 2:
            donnees_steam = chercher_jeu_steam(nom_jeu)
            if not donnees_steam.startswith("❌"):
                donnees_externes += f"[Données Steam]\n{donnees_steam}\n\n"

    if "mod" in texte_lower and any(w in texte_lower for w in ["mod", "jeu"]):
        query = message.texte.replace("mod", "").replace("Mod", "").strip()[:50]
        donnees_externes += f"[Données GameBanana]\n{chercher_mods_gamebanana(query)}\n\n"

    # Ajouter le message à l'historique
    historique.append({"role": "user", "content": message.texte})

    try:
        # Appel à Claude avec contexte du rôle
        # Copie de la liste pour éviter de muter les entrées de l'historique stocké
        messages_enrichis = list(historique[-20:])

        if donnees_externes:
            last = messages_enrichis[-1]
            messages_enrichis[-1] = {**last, "content": last["content"] + f"\n\n{donnees_externes}"}

        reponse_claude = get_client().messages.create(
            model="claude-opus-4-8",
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": role["system_prompt"],
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=messages_enrichis,
        )

        texte_reponse = reponse_claude.content[0].text

    except anthropic.AuthenticationError:
        raise HTTPException(status_code=401, detail="Clé API invalide. Vérifie ton fichier .env !")
    except anthropic.RateLimitError:
        raise HTTPException(status_code=429, detail="Trop de requêtes. Attends quelques secondes.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur Claude : {str(e)}")

    # Sauvegarder la réponse
    historique.append({"role": "assistant", "content": texte_reponse})

    return Reponse(reponse=texte_reponse, nb_messages=len(historique))

@app.get("/roles")
def get_roles():
    """Retourne tous les rôles disponibles."""
    all_roles = {**ROLES, **roles_custom}
    return {
        "roles": [
            {
                "id": role_id,
                "name": role["name"],
                "emoji": role["emoji"],
                "description": role["description"],
                "tags": role["tags"],
                "greeting": role["greeting"],
            }
            for role_id, role in all_roles.items()
        ]
    }

@app.post("/roles")
def create_role(role_data: dict):
    """Crée un rôle personnalisé."""
    role_id = str(uuid.uuid4())[:8]
    roles_custom[role_id] = {
        "id": role_id,
        "name": role_data.get("name", "Rôle personnalisé"),
        "emoji": role_data.get("emoji", "🎭"),
        "description": role_data.get("description", ""),
        "tags": role_data.get("tags", []),
        "greeting": role_data.get("greeting", "Bonjour !"),
        "system_prompt": role_data.get("system_prompt", "Tu es un assistant IA.")
    }
    return {"id": role_id, "role": roles_custom[role_id]}

@app.delete("/roles/{role_id}")
def delete_role(role_id: str):
    """Supprime un rôle personnalisé."""
    if role_id in ROLES:
        raise HTTPException(status_code=403, detail="Impossible de supprimer les rôles pré-définis")
    if role_id in roles_custom:
        del roles_custom[role_id]
        return {"message": f"Rôle {role_id} supprimé"}
    raise HTTPException(status_code=404, detail="Rôle non trouvé")

@app.get("/historique")
def get_historique():
    """Retourne l'historique de la conversation."""
    return {"historique": historique, "total": len(historique)}

@app.delete("/historique")
def effacer_historique():
    """Efface l'historique."""
    historique.clear()
    return {"message": "Historique effacé ✅"}
