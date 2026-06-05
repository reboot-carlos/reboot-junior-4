#!/usr/bin/env python3
"""
Test rapide de l'API NovAI
Lance ce script pour vérifier que le serveur fonctionne
"""

import requests
import json
import sys
import time

API_URL = "http://127.0.0.1:8000"

def test_connection():
    """Test la connexion à l'API"""
    try:
        print("🔌 Test de connexion...", end=" ", flush=True)
        response = requests.get(f"{API_URL}/", timeout=2)
        if response.status_code == 200:
            print("✅")
            data = response.json()
            print(f"   Version: {data.get('version')}")
            print(f"   Modèle: {data.get('model')}")
            return True
        else:
            print(f"❌ Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌")
        print("   ⚠️  Le serveur n'est pas démarré")
        print("   Lance: uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"❌ {str(e)}")
        return False

def test_roles():
    """Test le endpoint des rôles"""
    try:
        print("🎭 Test des rôles...", end=" ", flush=True)
        response = requests.get(f"{API_URL}/roles", timeout=2)
        if response.status_code == 200:
            data = response.json()
            roles = data.get('roles', [])
            print(f"✅ ({len(roles)} rôles)")
            for role in roles:
                print(f"   • {role['emoji']} {role['name']}")
            return True
        else:
            print(f"❌ Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {str(e)}")
        return False

def test_chat():
    """Test le endpoint de chat"""
    try:
        print("💬 Test du chat...", end=" ", flush=True)
        payload = {
            "texte": "Bonjour, dis-moi un fait intéressant en une phrase.",
            "role_id": "assistant"
        }
        response = requests.post(
            f"{API_URL}/chat",
            json=payload,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            reponse = data.get('reponse', '')
            nb_messages = data.get('nb_messages', 0)
            print(f"✅")
            print(f"   Réponse: {reponse[:80]}...")
            print(f"   Historique: {nb_messages} messages")
            return True
        else:
            print(f"❌ Status {response.status_code}")
            if response.status_code == 401:
                print("   ⚠️  Clé API invalide (vérifiez .env)")
            return False
    except requests.exceptions.Timeout:
        print("❌")
        print("   ⚠️  Timeout - la réponse a pris trop longtemps")
        print("   Vérifiez votre clé API et votre connexion Internet")
        return False
    except Exception as e:
        print(f"❌ {str(e)}")
        return False

def main():
    print("=" * 50)
    print("🤖 TEST DE L'API NOVAI")
    print("=" * 50)
    print()

    results = {
        "Connexion": test_connection(),
        "Rôles": test_roles(),
        "Chat": test_chat()
    }

    print()
    print("=" * 50)
    passed = sum(1 for v in results.values() if v)
    total = len(results)

    if passed == total:
        print(f"✅ TOUS LES TESTS PASSÉS ({passed}/{total})")
        print()
        print("L'API fonctionne correctement !")
        print("Ouvre index.html pour commencer à chatter.")
        return 0
    else:
        print(f"⚠️  {total - passed} TEST(S) ÉCHOUÉ(S)")
        print()
        print("Dépannage:")
        if not results["Connexion"]:
            print("1. Démarre le serveur: uvicorn main:app --reload")
        if not results["Rôles"]:
            print("2. Vérifiez les logs du serveur")
        if not results["Chat"]:
            print("3. Vérifiez votre clé API dans .env")
        return 1

if __name__ == "__main__":
    sys.exit(main())
