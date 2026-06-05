# 🤖 NovAI — Chatbot IA avec Gestion des Rôles

Un assistant IA conversationnel moderne avec **4 rôles personnalisés**, interface belle et architecture propre.

## ⚡ Démarrage Rapide

### 1. Installer les dépendances
```bash
cd backend/
pip install -r requirements.txt
```

### 2. Configurer la clé API
```bash
# Éditer backend/.env et remplacer :
ANTHROPIC_API_KEY=sk-ant-YOUR_API_KEY
```

### 3. Lancer le serveur API
```bash
cd backend/
uvicorn main:app --reload
```

L'API démarre à `http://127.0.0.1:8000` ✅

### 4. Ouvrir le chatbot
- Double-clic sur `index.html` OU
- Serveur local : `python -m http.server 5000` puis ouvrir `http://localhost:5000`

## 🎭 Les 4 Rôles

| Rôle | Emoji | Usage |
|------|-------|-------|
| **NovAI** | 🤖 | Chat général intelligent |
| **Mentor IA** | 👨‍🏫 | Apprendre et étudier |
| **Muse Créative** | 🎨 | Brainstorming & créativité |
| **Analyste Logique** | 🔬 | Raisonnement & problèmes |

## 📋 Fonctionnalités

✅ Chat conversationnel fluide  
✅ Historique persistant (localStorage)  
✅ 4 rôles pré-configurés  
✅ Basculer entre rôles en un clic  
✅ Interface moderne et responsive  
✅ Suppression de messages/conversations  
✅ Markdown support dans les réponses  

## 📁 Structure

```
chatbot-new/
├── index.html           # Frontend (UI)
├── README.md           # Ce fichier
├── CLAUDE.md           # Documentation complète
└── backend/
    ├── main.py         # API FastAPI
    ├── requirements.txt
    └── .env           # Variables d'env (à configurer)
```

## 🚀 API Rapide

```bash
# Envoyer un message
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"texte": "Bonjour", "role_id": "mentor"}'

# Voir les rôles
curl http://127.0.0.1:8000/roles

# Voir l'historique
curl http://127.0.0.1:8000/historique
```

## ⚙️ Configuration

Pour les détails complets : voir `CLAUDE.md`

---

**Questions ?** Voir la documentation complète dans `CLAUDE.md` 📚
