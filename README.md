# App créateur d'exercices de mathématiques

Une application qui permet de généré des exercices de mathématiques à volonté.

## Contenu du dépôt

Ce dépôt contient le code source de l'application.
Elle est développée en Python et elle utilise une base de données d'exercices pour générer des exercices avec l'IA.

## Utilisation

1. Clonez le dépôt, renommer le, et placez vous dedans `cd votre-dossier`
2. Créer un environnement virtuel avec :
```bash
python -m venv env
```
3. Activer votre environnement virtuel :
 ```bash 
 windows : env\Script\activate
 linux : source env/bin/activate
 ```
4. Installez les dépendances en exécutant :
```bash
pip install -r requirements.txt
```
5. Créer un fichier `.env` à la racine du projet et ajouter les variables d'environnement suivantes :
```bash 
OPENAI_API_KEY="votre clé API"
FLASK_APP="app\\route.py" // sur windows
```

6. Lancez votre application Python.

## Contribution

Contributions, problèmes et demandes de fonctionnalités sont les bienvenus !

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.
