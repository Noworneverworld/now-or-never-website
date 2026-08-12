# Gérer Now or Never sans coder

## Le template V11
Dans Pages CMS > Guides & articles, tu peux gérer sans code : la photo principale, l’introduction, autant d’étapes que nécessaire, jusqu’à 3 photos par étape, ton avis, les activités à retenir, le budget détaillé, les transports, les infos pratiques, la conclusion et le SEO.

## Synchronisation
Quand tu sauvegardes dans Pages CMS, le JSON est mis à jour dans GitHub. GitHub Actions lance ensuite `build.py`. Le build génère l’article, met à jour automatiquement les cartes de la page Conseils & destinations, régénère le sitemap et publie le dossier `dist`.

## Photos
Une seule photo sur une étape : mise en page paysage. Deux ou trois photos : mosaïque. Tu peux les remplacer à tout moment dans Pages CMS.

## Brouillon
Brouillon activé : pas de page publique et la carte affiche “Bientôt disponible”. Brouillon désactivé : page générée et carte cliquable.
