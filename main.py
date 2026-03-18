#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Puff Lens/Bethune - Mini App Telegram
Serveur web + Bot Telegram combinés
"""

from flask import Flask, send_from_directory, request, jsonify
import os
import json
from datetime import datetime
import threading
import subprocess
import time

app = Flask(__name__, static_folder='frontend')

# ==========================================
# FICHIER DE DONNÉES
# ==========================================
import os
DATA_FILE = os.path.join(os.getcwd(), 'products.json')

def load_puffs():
    """Charger les puffs depuis le fichier JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Erreur chargement puffs: {e}")
            return []
    else:
        print(f"📁 Fichier {DATA_FILE} non trouvé, création vide")
        return []

def save_puffs(puffs):
    """Sauvegarder les puffs dans le fichier JSON"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(puffs, f, ensure_ascii=False, indent=2)
        print(f"✅ {len(puffs)} puffs sauvegardés dans {DATA_FILE}")
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde puffs: {e}")
        return False

# ==========================================
# ROUTES API
# ==========================================
@app.route('/api/products', methods=['GET'])
def get_products():
    """Récupérer tous les puffs personnalisés"""
    puffs = load_puffs()
    return jsonify({'success': True, 'products': puffs})

@app.route('/api/products', methods=['POST'])
def add_product():
    """Ajouter un nouveau puff"""
    try:
        product_data = request.get_json()
        
        # Validation des données
        required_fields = ['name', 'price', 'category']
        for field in required_fields:
            if not product_data.get(field):
                return jsonify({'success': False, 'error': f'Champ {field} requis'}), 400
        
        # Ajouter le puff
        puffs = load_puffs()
        new_puff = {
            'id': len(puffs) + 1,
            'name': product_data['name'],
            'category': product_data['category'],  # Nouveau champ catégorie
            'price': product_data['price'],  # Garder en texte pour "1G: 20€, 2G: 35€..."
            'puffs': product_data.get('puffs', 'Non spécifié'),
            'description': product_data.get('description', ''),
            'image': product_data.get('image', 'bg.jpg'),
            'mediaType': product_data.get('mediaType', 'image'),
            'custom': True,
            'created': datetime.now().isoformat()
        }
        
        puffs.append(new_puff)
        
        if save_puffs(puffs):
            return jsonify({'success': True, 'product': new_puff})
        else:
            return jsonify({'success': False, 'error': 'Erreur sauvegarde'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Supprimer un puff"""
    try:
        puffs = load_puffs()
        original_length = len(puffs)
        
        # Filtrer le puff à supprimer
        puffs = [p for p in puffs if p['id'] != product_id]
        
        if len(puffs) == original_length:
            return jsonify({'success': False, 'error': 'Puff non trouvé'}), 404
        
        if save_puffs(puffs):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Erreur sauvegarde'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==========================================
# ROUTES STATIQUES
# ==========================================
# Route principale - sert index.html
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

# Route pour servir tous les fichiers statiques
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

# ==========================================
# DÉMARRAGE BOT TELEGRAM
# ==========================================
def start_telegram_bot():
    """Démarrer le bot Telegram en Python dans un thread séparé"""
    try:
        # Importer et lancer le bot Python
        from bot import start_bot_thread
        start_bot_thread()
    except Exception as e:
        print(f"❌ Erreur démarrage bot: {e}")

# ==========================================
# DÉMARRAGE
# ==========================================
if __name__ == '__main__':
    # Créer le fichier JSON s'il n'existe pas
    if not os.path.exists(DATA_FILE):
        save_puffs([])
    
    # Démarrer le bot Telegram en arrière-plan léger
    try:
        import threading
        import time
        
        def run_bot_lightweight():
            """Bot ultra léger qui ne bloque pas Flask"""
            try:
                from bot import start_bot_thread
                start_bot_thread()
                print("🤖 Bot Telegram démarré en arrière-plan léger")
            except Exception as e:
                print(f"⚠️ Erreur bot (non critique): {e}")
        
        # Démarrer le bot dans un thread daemon
        bot_thread = threading.Thread(target=run_bot_lightweight, daemon=True)
        bot_thread.start()
        print("🚀 Thread bot démarré")
        
    except Exception as e:
        print(f"⚠️ Impossible de démarrer le bot: {e}")
    
    # Démarrer le serveur Flask (priorité absolue)
    port = int(os.environ.get('PORT', 8080))
    print(f"🌐 Démarrage du serveur web sur le port {port}")
    app.run(host='0.0.0.0', port=port, threaded=True)
