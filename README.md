# API de création d'exercices de mathématiques

Ce logiciel construit des exercices de mathématiques. Il est utilisable via son API.

## Contenu du dépôt

Ce dépôt contient le code source de l'application. Elle est développée en Python et utilise une base de données d'exercices modifiés par l'IA.

## Utilisation

1. Clonez le dépôt, renommez-le, puis vous placer dans son répertoire: `cd votre-dossier`
2. Créez un environnement virtuel avec :
```bash
python -m venv env
```
3. Activez votre environnement virtuel :
 ```bash 
 Windows : env\Script\activate
 Linux : source env/bin/activate
 ```
4. Installez les dépendances:
```bash
pip install -r requirements.txt
```
5. Créez un fichier `.env` à la racine du projet et étalissez les variables d'environnement nécessaires:
```bash 
OPENAI_API_KEY="votre clé API"
FLASK_APP="app\\route.py" // sur Windows
```
6. Lancez l'application Python. Ses points d'entrée sont :
    - `flask run` pour lancer le serveur Flask
    - `app/main.py` pour lancer en Python

## Contribution

Contribution, description de problème et demande de fonctionnalité sont les bienvenus !

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.
