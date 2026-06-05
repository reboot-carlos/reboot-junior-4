# 🤖 NovAI — Assistant IA avec Gestion des Rôles

## 📋 Vue d'ensemble

**NovAI** est un chatbot conversationnel moderne et focalisé, avec une architecture propre séparant frontend et backend. Le système supporte **plusieurs rôles/personnalités** d'IA, permettant aux utilisateurs de basculer entre différents modes de conversation.

### Principes de Conception

1. **Focalisé** : Chat conversationnel pur, sans APIs externes
2. **Modulaire** : Rôles/personnalités facilement extensibles
3. **Maintenable** : Code structuré avec séparation des responsabilités
4. **Performant** : Utilisation de la mise en cache Claude pour les prompts système

---

## 🏗️ Architecture

```
chatbot-new/
├── index.html              # Frontend (UI interactive)
├── CLAUDE.md              # Cette doc
└── backend/
    ├── main.py            # API FastAPI (routage + logique)
    ├── requirements.txt    # Dépendances Python
    └── .env              # Variables d'environnement
```

### Flux de Données

```
[Client HTML]
    ↓ (fetch POST/GET)
[FastAPI Backend]
    ↓ (historique + système prompt du rôle)
[Claude API]
    ↓ (réponse générée)
[Client HTML] ← affichage du message
```

---

## 🎯 Fonctionnalités Principales

### 1. **Chat Conversationnel**
- Zone de chat centrale avec scroll automatique
- Messages utilisateur (gradients colorés) et IA (gradient violet)
- Rendu Markdown pour les réponses IA
- Suppression individuelle de messages
- Indicateur de réflexion en cours

### 2. **Gestion des Conversations**
- **Historique persistant** : localStorage (client)
- **Onglet Historique** : voir et charger les conversations passées
- **Nouvelle conversation** : bouton + dans la zone chat
- **Titre auto-généré** : extrait du premier message utilisateur
- **Suppression** : par conversation

### 3. **Gestion des Rôles**
- **Onglet Rôles** : bascule entre 4 rôles pré-définis
- **Rôles disponibles** :
  - 🤖 **NovAI** : Assistant conversationnel général
  - 👨‍🏫 **Mentor IA** : Professeur pédagogue structuré
  - 🎨 **Muse Créative** : Stimulation créatif et brainstorming
  - 🔬 **Analyste Logique** : Raisonnement logique et structuré

- **Par rôle** :
  - Système prompt unique (détermine le comportement)
  - Badges descriptifs (tags)
  - Avatar emoji personnalisé
  - Description et greeting

### 4. **Interface Moderne**
- **Sidebar** : historique + rôles (collapsible sur mobile)
- **Header** : avatar, badges, nom, statut (online)
- **Fond dégradé animé** : 4 couleurs en mouvement
- **Bulles décoratives** : animation float-up
- **Responsive** : adaptée desktop et mobile

---

## 🛠️ Installation & Démarrage

### Prérequis
- Python 3.10+
- Clé API Anthropic (gratuit avec crédit)

### 1. Installer les dépendances
```bash
cd backend/
pip install -r requirements.txt
```

### 2. Configurer la clé API
```bash
# Éditer backend/.env
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

### 3. Démarrer le serveur API
```bash
cd backend/
uvicorn main:app --reload
```

L'API sera disponible à `http://127.0.0.1:8000`

### 4. Ouvrir le frontend
Ouvrir `index.html` dans un navigateur (double-clic ou `python -m http.server`)

---

## 📡 API Endpoints

### **POST /chat**
Envoie un message au chatbot.

**Requête :**
```json
{
  "texte": "Comment apprendre Python ?",
  "role_id": "mentor"
}
```

**Réponse :**
```json
{
  "reponse": "Python est un excellent langage...",
  "nb_messages": 42
}
```

---

### **GET /roles**
Récupère tous les rôles disponibles.

**Réponse :**
```json
{
  "roles": [
    {
      "id": "assistant",
      "name": "NovAI",
      "emoji": "🤖",
      "description": "Assistant Conversationnel",
      "tags": ["✨ IA", "🧠 Intelligent", "🚀 Rapide"],
      "greeting": "Comment puis-je t'aider aujourd'hui ?"
    },
    ...
  ]
}
```

---

### **POST /roles**
Crée un rôle personnalisé (optionnel, pour future extension).

**Requête :**
```json
{
  "name": "Débateur",
  "emoji": "🎤",
  "description": "Expert en débat",
  "tags": ["🎯 Argumenté", "💬 Éloquent"],
  "greeting": "Débattons !",
  "system_prompt": "Tu es un débateur convaincant..."
}
```

---

### **DELETE /roles/{role_id}**
Supprime un rôle personnalisé.

⚠️ Les rôles pré-définis ne peuvent pas être supprimés.

---

### **GET /historique**
Récupère l'historique de conversation.

---

### **DELETE /historique**
Efface tout l'historique.

---

## 💡 Comment Ajouter un Nouveau Rôle

### Backend (main.py)
Ajouter une entrée dans le dictionnaire `ROLES` :

```python
ROLES = {
    ...
    "debater": {
        "id": "debater",
        "name": "Débateur",
        "emoji": "🎤",
        "description": "Expert en débat argumenté",
        "tags": ["🎯 Argumenté", "💬 Éloquent", "🔥 Convaincant"],
        "greeting": "Débattons ensemble !",
        "system_prompt": """Tu es un débateur expert qui...
        (instructions détaillées ici)"""
    }
}
```

Le frontend chargera automatiquement le nouveau rôle via `GET /roles`.

---

## 🔐 Sécurité

- ✅ Clé API stockée en `.env` (jamais committer)
- ✅ CORS ouvert pour développement (limiter en production)
- ✅ Validation Pydantic sur tous les inputs
- ✅ Pas d'accès à des APIs externes (surface d'attaque réduite)

---

## 📊 Caching Claude

Le système utilise **prompt caching** pour les system prompts :

```python
"cache_control": {"type": "ephemeral"}
```

Cela améliore la performance et réduit les coûts pour les rôles volumineux.

---

## 🎨 Styling

- **Palette** : Violet (#a855f7), Bleu (#3a86ff), Cyan (#06b6d4)
- **Typography** : Poppins (normal), Pacifico (boutons)
- **Animations** : Gradient flow, slide-in, bounce, pulse
- **Z-index** : Bulles (0) < contenu (1) < sidebar (50)

---

## 🐛 Dépannage

### "⚠️ API non démarrée"
```bash
# Redémarrer le backend
cd backend/
uvicorn main:app --reload
```

### Clé API invalide
```bash
# Vérifier backend/.env
cat backend/.env
```

### Historique non sauvegardé
Les conversations sont stockées en `localStorage` du navigateur. Effacer le cache supprime l'historique.

---

## 🚀 Évolutions Futures

- [ ] Persistance cloud (base de données)
- [ ] Authentification utilisateur
- [ ] Partage de conversations
- [ ] Export PDF/JSON
- [ ] Paramètres avancés (température, max_tokens)
- [ ] Intégration vision (images)
- [ ] Mode sombre/clair

---

## 📝 Notes de Développement

### Architecture Backend

Le backend est volontairement **simple** et **maintenable** :
- Pas de patterns complexes (Factory, Strategy, etc.)
- Historique en mémoire (acceptable pour 1 utilisateur / dev)
- Configuration centralisée dans `ROLES`
- Prompts système avec cache ephemeral

### Code Formatting

- Python : PEP 8, docstrings court
- JavaScript : ES6+, camelCase, commentaires rares
- HTML : BEM-like classes, emojis dans l'UI

### Performance

- Messages limités à 20 derniers (contexte window)
- Scrolling auto pour messages
- Debounce sur recherche (futur)

---

## 👤 Développeur Senior Notes

**Principes appliqués :**
1. ✅ Séparation Frontend/Backend claire
2. ✅ Une responsabilité par fonction
3. ✅ Configuration centralisée (ROLES)
4. ✅ DRY : pas de code dupliqué
5. ✅ Documentation complète
6. ✅ Pas d'over-engineering (une fonctionnalité = une implémentation simple)

**Décisions justifiées :**
- localStorage pour historique : acceptable dev, pas de backend lourd
- Rôles immuables pré-définis : cohérence garantie
- Pas d'APIs externes : focalisé et maintenable
- Prompt caching : améliore perf & réduit coûts

---

## 📄 Licence & Auteur

Chatbot créé en 2026 — Architecture senior, focalisée sur la clarté et la maintenabilité.
