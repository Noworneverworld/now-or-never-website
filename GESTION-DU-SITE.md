# Now or Never — gestion du site

Cette V9 ajoute la couche d’administration du blog sans changer le design validé.

## Ce que Charlotte pourra faire sans coder

Dans Pages CMS :

1. Créer un guide ou un article.
2. Modifier le titre, le pays, le type de contenu, la photo, le résumé et le texte.
3. Ajouter ou remplacer des photos avec le gestionnaire de médias.
4. Renseigner le titre et la description Google.
5. Garder un article en brouillon puis le publier en décochant « Brouillon ».

Les contenus sont enregistrés dans `content/guides/`. Le script `build.py` transforme automatiquement les contenus publiés en pages HTML statiques dans `dist/guides/` et génère aussi `sitemap.xml` et `robots.txt`.

## Mise en ligne prévue

- Dépôt : GitHub
- Interface d’édition : Pages CMS
- Hébergement : Cloudflare Pages
- Commande de build : `python build.py`
- Dossier publié : `dist`

Les 3 guides présents (Vietnam, Nouvelle-Zélande, Japon) sont volontairement en brouillon et ne contiennent aucun itinéraire ou budget inventé. Ils servent de modèles à compléter avec l’expérience réelle de Charlotte.
