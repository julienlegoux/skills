# Exercise loop

Paste everything below the line after `/loop`, in an empty folder, in a local session
signed in to `gh` as a maintainer of the skills repo.

---

Tu fais tourner les skills lx sur des projets pour voir où leurs instructions posent problème. À chaque tour :

1. Lis journal.md (crée-le s'il n'existe pas) et invente trois projets qui n'y figurent pas encore, de genres différents. Pas des jouets : chacun doit obliger à de vrais choix (plusieurs composants, des données à modéliser, des compromis à trancher), tout en restant faisable en local, sans compte, clé ni déploiement, et en quelques heures de build au plus. Inscris-les dans journal.md.

2. Pour chacun, crée un dossier vide et lance dedans une session Claude Code séparée sur le modèle Sonnet, les trois en parallèle. Pas un sous-agent : il ne pourrait pas lancer ses propres relecteurs. Par exemple `claude -p "<la demande>" --model sonnet --output-format json --permission-mode auto`, en gardant la sortie dans un fichier du dossier. Donne-lui seulement la demande, écrite comme je l'écrirais, et dis-lui de la traiter avec le skill lx:plan. Elle ne doit pas savoir que c'est un essai.

3. Le demandeur, c'est moi, et tu réponds à ma place. Quand la session revient avec des questions ou avec son plan, réponds dans cette même session (`--resume <session_id>`) comme je le ferais. Valide le plan quand c'est celui que j'aurais validé. Ensuite laisse-la aller jusqu'au bout.

4. Quand une session a terminé, porte un second regard sur ce qu'elle a fait : son compte rendu, son déroulé, son dossier, et le produit lui-même, que tu essaies. Compare-le à la demande de départ et au plan validé : ce qui a été abandonné ou remis à plus tard en route compte. Si les instructions d'un skill l'ont bloquée, ralentie ou envoyée dans une mauvaise direction, même si elle s'en est sortie, et qu'elle ne l'a pas déjà signalé elle-même, signale-le avec le skill lx:feedback.

5. Complète journal.md pour chaque projet : s'il marche, et ce qui a été signalé, par la session et par toi.

Ne modifie jamais les skills et n'aide pas une session à contourner une difficulté : le but est de voir où elle bute. Si rien ne cloche, ne signale rien.
