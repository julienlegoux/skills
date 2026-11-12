# Exercise loop

Paste everything below the line after `/loop`, in an empty folder, in a local session
signed in to `gh` as a maintainer of the skills repo.

---

Tu fais tourner les skills lx sur des projets pour voir où leurs instructions posent problème. À chaque tour :

1. Lis journal.md (crée-le s'il n'existe pas) et invente trois projets qui n'y figurent pas encore, de genres différents. Pas des jouets : chacun doit obliger à de vrais choix (plusieurs composants, des données à modéliser, des compromis à trancher), tout en restant faisable en local, sans compte, clé ni déploiement, et en quelques heures de build au plus. Inscris-les dans journal.md.

2. Pour chacun, crée un dossier vide et lance dedans un agent sur le modèle Sonnet, les trois en parallèle. Donne-lui seulement la demande, écrite comme je l'écrirais, et dis-lui de la traiter avec le skill lx:plan. Il ne doit pas savoir que c'est un essai.

3. Le demandeur, c'est moi, et tu réponds à ma place. Quand l'agent revient avec des questions ou avec son plan, réponds au même agent comme je le ferais. Valide le plan quand c'est celui que j'aurais validé. Ensuite laisse-le aller jusqu'au bout.

4. Quand un agent a terminé, porte un second regard sur ce qu'il a fait : son compte rendu, le déroulé de sa session, son dossier, et le produit lui-même, que tu essaies. Si les instructions d'un skill l'ont bloqué, ralenti ou envoyé dans une mauvaise direction, même s'il s'en est sorti, et qu'il ne l'a pas déjà signalé lui-même, signale-le avec le skill lx:feedback.

5. Complète journal.md pour chaque projet : s'il marche, et ce qui a été signalé, par l'agent et par toi.

Ne modifie jamais les skills et n'aide pas un agent à contourner une difficulté : le but est de voir où il bute. Si rien ne cloche, ne signale rien.
