# 🚀 Premiers Pas — NovAI

Bienvenue ! Voici les étapes pour démarrer **NovAI** en 5 minutes.

## ⚙️ Étape 1 : Installer les dépendances

Ouvre un terminal et tape :

```bash
cd backend/
pip install -r requirements.txt
```

Cela installe FastAPI, Uvicorn et l'SDK Anthropic.

---

## 🔑 Étape 2 : Configurer ta clé API

Ouvre le fichier `backend/.env` et remplace :

```
ANTHROPIC_API_KEY=sk-ant-REMPLACE_MOI
```

par ta vraie clé API. Tu la trouves ici → https://console.anthropic.com/keys

**Exemple :**
```
ANTHROPIC_API_KEY=sk-ant-v7xz9aB4cD2eF1gH5jK8lM0nO3pQ6rS9tU
```

---

## 🚀 Étape 3 : Lancer le serveur

### Option A : Linux/Mac
```bash
cd backend/
bash start.sh
```

### Option B : Windows
```bash
cd backend/
start.bat
```

### Option C : Manuel (tous les OS)
```bash
cd backend/
uvicorn main:app --reload
```

Tu devrais voir :
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Laisse le terminal ouvert !** ✅

---

## 💻 Étape 4 : Ouvrir l'interface

1. Double-clic sur `index.html` dans le dossier principal, OU
2. Ouvre ton navigateur et va à `file:///...chemin.../index.html`

Tu devrais voir :
- ✅ Un chatbot avec 4 rôles
- ✅ Un historique vide
- ✅ Une zone de chat active

---

## 💬 Étape 5 : Commencer à chatter

1. Sélectionne un **rôle** (onglet Rôles à gauche)
2. Clique sur un rôle : **NovAI, Mentor, Créative, Analyste**
3. Tape un message dans la boîte en bas
4. Appuie sur **Entrée** ou **Envoyer**

---

## ❌ Ça ne marche pas ?

### "Chargement des rôles..." en boucle
→ **Le backend n'est pas démarré**
- Retour à l'Étape 3
- Vérifiez que le terminal affiche `http://127.0.0.1:8000`

### "⚠️ API non démarrée"
→ **Même problème**
- Redémarrez le serveur : `uvicorn main:app --reload`

### "Clé API invalide"
→ **La clé n'est pas bonne**
- Vérifiez `backend/.env`
- La clé doit commencer par `sk-ant-`
- Récupérez-la sur https://console.anthropic.com/keys

### Le message ne s'envoie pas
→ **Le serveur a crashé**
- Regardez le terminal (section Étape 3)
- Cherchez les erreurs rouges
- Relancez : `uvicorn main:app --reload`

---

## 🎉 Ça marche !

Félicitations ! Tu as un chatbot IA fully fonctionnel avec :
- 4 rôles différents
- Historique des conversations
- Interface moderne
- Backend propre et maintenable

**Prochaines étapes :**
- Ajoute un nouveau rôle (voir `CLAUDE.md`)
- Partage le projet avec des amis
- Explore les fonctionnalités avancées

---

## 📚 Besoin de plus d'infos ?

Consulte :
- `README.md` — Vue d'ensemble
- `CLAUDE.md` — Architecture complète
- Terminal — Logs du serveur

Enjoy ! 🚀
