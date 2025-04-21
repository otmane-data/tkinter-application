# 🏋️‍♂️ FitTracker - Application de Suivi de Fitness et Santé

<div align="center"> <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/dumbbell.svg" width="100" height="100" alt="FitTracker Logo" /> </div>

## 📋 Table des Matières
- [📝 Description](#-description)
- [✨ Fonctionnalités](#-fonctionnalités)
- [📸 Captures d'écran](#-captures-décran)
- [🔧 Prérequis](#-prérequis)
- [📥 Installation](#-installation)
- [🗄️ Configuration de la Base de Données](#️-configuration-de-la-base-de-données)
- [📁 Structure du Projet](#-structure-du-projet)
- [🚀 Utilisation](#-utilisation)
- [👥 Contributeurs](#-contributeurs)
- [📄 Licence](#-licence)

## 📝 Description
FitTracker est une application de bureau développée en Python avec Tkinter, permettant aux utilisateurs de suivre leur activité physique, leur alimentation et leur état de santé général. Elle offre une interface intuitive pour enregistrer, consulter et analyser les données liées au bien-être.

## ✨ Fonctionnalités

### 👤 Gestion des Utilisateurs
- ✅ Création de compte & connexion sécurisée
- ✅ Profil utilisateur personnalisé
- ✅ Récupération de mot de passe

### 🍎 Suivi de la Nutrition
- ✅ Enregistrement des repas (petit-déjeuner, déjeuner, dîner)
- ✅ Calcul automatique des calories
- ✅ Différents plans alimentaires (athlètes / non-athlètes)
- ✅ Visualisation graphique de la consommation

### 💪 Suivi de l'Activité Physique
- ✅ Enregistrement des exercices (push-ups, squats, cardio...)
- ✅ Classification par intensité
- ✅ Chronomètre intégré
- ✅ Visualisation de la progression

### ❤️ Suivi de Santé
- ✅ Calcul de l'IMC
- ✅ Suivi du sommeil
- ✅ Définition d'objectifs
- ✅ Tendances et graphiques santé

## 📸 Captures d'écran
<div align="center"> <p><i>Des captures d'écran de l'application seront bientôt disponibles.</i></p> </div>

## 🔧 Prérequis
- Python 3.x
- Tkinter (déjà inclus)
- Dépendances :
```bash
pip install pymysql matplotlib pillow tkcalendar
```
- Serveur MySQL local

## 📥 Installation
1. Clonez le dépôt :
```bash
git clone https://github.com/votre-nom/tkinter-fit-tracker.git
```

2. Installez les bibliothèques nécessaires :
```bash
pip install pymysql matplotlib pillow tkcalendar
```

3. Configurez la base de données (voir section suivante).

4. Lancez l'application :
```bash
python login.py
```

## 🗄️ Configuration de la Base de Données
L'application utilise une base MySQL appelée `ensah` avec les tables suivantes :

| Table | Description |
|-------|-------------|
| info | Stocke les informations utilisateurs (id, prénom, nom, âge, genre, email, mot_de_passe) |
| fitness | Stocke les données physiques (id, poids, taille, objectif, IMC, interpretation) |

## 📁 Structure du Projet
```
📦 tkinter-fit-tracker/
 ┣ 📜 login.py          → Authentification & lancement de l'app
 ┣ 📜 formulaire.py     → Création de compte
 ┣ 📜 fitness.py        → Interface principale (poids, taille, objectifs...)
 ┣ 📜 nutrition.py      → Gestion des repas & calories
 ┣ 📜 Physic.py         → Activités sportives (push-ups, cardio...)
 ┣ 📜 Sante.py          → Suivi santé & sommeil
 ┗ 📜 README.md         → Documentation
```

## 🚀 Utilisation
1. Lancez `login.py`
2. Connectez-vous ou créez un compte
3. Naviguez entre :
   - 🧑‍💼 Profil
   - 🍎 Nutrition
   - 💪 Activité physique
   - ❤️ Santé

## 👥 Contributeurs
Bourabaa

## 📄 Licence
Ce projet est sous licence MIT.
Consultez le fichier LICENSE pour plus d'informations.
