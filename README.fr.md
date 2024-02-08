<h1 align="center">
  <a href="https://github.com/MadeInPierre/finalynx">
    <img src="https://raw.githubusercontent.com/MadeInPierre/finalynx/main/docs/_static/logo_assistant_transparent.png" width="400" />
  </a>
  <br>Finalynx Assistant<br>
</h1>

<div align="center">
  View in <a href="https://github.com/MadeInPierre/finalynx/blob/main/README.md">English 🇬🇧</a> / Lire en <a href="https://github.com/MadeInPierre/finalynx/blob/main/README.fr.md">Français 🇫🇷</a>

  <br>

  <h4>Outil de ligne de commande minimaliste pour vous aider à gérer vos investissements</h4>
  <a href="https://pypi.org/project/finalynx/"><img alt="PyPI" src="https://img.shields.io/pypi/v/finalynx?style=flat-square"></a>
  <a href="https://github.com/MadeInPierre/finalynx/actions/workflows/semantic-release.yml"><img alt="GitHub Workflow Status (main)" src="https://img.shields.io/github/actions/workflow/status/madeinpierre/finalynx/semantic-release.yml?branch=main&style=flat-square"></a>
  <a href="https://github.com/MadeInPierre/finalynx/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/madeinpierre/finalynx?style=flat-square"></a>
  <a href="https://github.com/sponsors/MadeInPierre"><img alt="GitHub Sponsors" src="https://img.shields.io/github/sponsors/MadeInPierre?style=flat-square"></a>
  <a href="https://github.com/finary-wealth/awesome"><img alt="Mentioned in Awesome Finary" src="https://awesome.re/mentioned-badge-flat.svg"></a>

  <sub>Construit avec ❤︎ par <a href="https://github.com/sponsors/MadeInPierre">Pierre Laclau</a> et <a href="https://github.com/MadeInPierre/finalynx/graphs/contributors">contributeurs</a>. Logo généré par <a href="https://midjourney.com">Midjourney</a>.</sub>

  <br>
</div>

Finalynx est votre "assistant financier", un outil en ligne de commande (et un tableau de bord web expérimental) pour organiser votre portefeuille d'investissements et obtenir des recommandations mensuelles automatisées basées sur vos objectifs de vie futurs.
Cet outil se synchronise avec votre compte Finary, un agrégateur de comptes d'investissement, pour afficher vos positions en temps réel.

Vous n'avez pas encore Finary ? Vous pouvez vous inscrire en utilisant mon [lien de parrainage](https://finary.com/referral/f8d349c922d1e1c8f0d2) 🌹 (ou via la page [par défaut](https://finary.com/signup)).

<p align="center">
  <img src="https://raw.githubusercontent.com/MadeInPierre/finalynx/main/docs/_static/screenshot_demo_frameless.png" width="600" />
</p>

<details>
<summary>
  <div align="center">
    <strong>[Cliquer]</strong> Captures d'écran supplémentaires 📸
  </div>
</summary>

| Recommendations                                                                                                                    | Tableau de bord web                                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| <img src="https://raw.githubusercontent.com/MadeInPierre/finalynx/main/docs/_static/screenshot_recommendations.png" width="600" /> | <img src="https://raw.githubusercontent.com/MadeInPierre/finalynx/main/docs/_static/screenshot_dashboard.png" width="600" /> |

Finalynx comprend également un gestionnaire de budget quotidien pour classer vos dépenses et afficher des statistiques mensuelles et annuelles :

<img src="https://raw.githubusercontent.com/MadeInPierre/finalynx/main/docs/_static/budget.png"/>

<img src="https://raw.githubusercontent.com/MadeInPierre/finalynx/main/docs/_static/budget_review.png"/>

Des statistiques et des visualisations seront bientôt ajoutées !

</details>

## ✨ Fonctionnalités

1. **✅ Portefeuille:** Organisez vos actifs, fixez des objectifs et synchronisez avec votre compte Finary.
2. **⏳ Tableau de bord web:** Générez des statistiques et graphiques pour comprendre chaque ligne ou dossier.
3. **⏳ Assistant:** Obtenez des recommandations mensuelles sur vos investissements pour atteindre vos objectifs.
4. **🔜 Simulateur:** Définissez vos objectifs et événements de vie, simulez l'avenir de votre portefeuille.
5. **🙏 Extensions:** Faire fonctionner cet outil pour les situations d'autres personnes, contributions nécessaires 👀.

Vous pouvez consulter le [statut de développement actuel](https://github.com/users/MadeInPierre/projects/4). Les contributions sont les bienvenues !

## 🚀 Installation

Si vous n'avez pas l'intention de toucher au code, exécutez simplement (avec python >=3.10 et pip installé) :

```sh
pip install finalynx  # exécuter à nouveau avec --upgrade pour mettre à jour
```

Et c'est tout ! Maintenant, créez votre propre copie de l'exemple [`demo.py`](https://github.com/MadeInPierre/finalynx/blob/main/examples/demo.py) n'importe où et exécutez-le pour vous assurer que tout fonctionne. Vous pouvez maintenant le personnaliser pour vos propres besoins 🚀

**Débutants:** Voici des [étapes détaillées](https://finalynx.readthedocs.io/en/latest/quickstart/installation.html#detailed-instructions) et une [vidéo](https://www.terminalizer.com/view/5fcce8cb5875). N'hésitez pas à [ouvrir une discussion](https://github.com/MadeInPierre/finalynx/discussions), avec plaisir pour aider !

**Pro Tip 💡:** _Pourquoi pas créer un script pour lancer le projet dans un terminal à chaque démarrage ? Jolie vue_ 🤭

## ⚙️ Utilisation et documentation

L'objectif est de déclarer une arborescence de l'ensemble de votre portefeuille indépendamment de leurs enveloppes (e.g. PEA, AV, CTO, etc). Une fois que la stratégie de l'ensemble de votre portefeuille est définie dans Finalynx, trouvez la meilleure enveloppe pour chaque ligne et ajoutez-les à votre compte Finary (synchronisation manuelle ou automatique). Finalynx récupérera chaque ligne et affichera votre portefeuille complet avec les montants en temps réel.

Voici le code minimal accepté :

```python
from finalynx import Portfolio, Assistant
portfolio = Portfolio()     # <- votre configuration personnalisée ici
Assistant(portfolio).run()  # <- voir les tutoriels pour plus d'options
```

Vous pouvez maintenant remplir la classe `Portfolio` avec votre propre hiérarchie personnalisée en vous inspirant de l'exemple [`demo.py`](https://github.com/MadeInPierre/finalynx/blob/main/examples/demo.py) ou en lisant le guide [Getting Started](https://finalynx.readthedocs.io/en/latest/quickstart/getting_started.html) dans la documentation et les [Tutoriels](https://github.com/MadeInPierre/finalynx/tree/main/examples/tutorials) étape par étape. Pour plus de détails, consultez la [Référence API](https://finalynx.readthedocs.io/en/latest/apidocs/index.html) ou [posez une question](https://github.com/MadeInPierre/finalynx/discussions/new?category=q-a).

Une fois que vous avez défini un arbre de portefeuille complet avec des objectifs raisonnables, vous pouvez afficher le montant que vous devez investir dans chaque ligne à l'aide de :

```sh
python your_config.py delta  # tapez --help pour d'autres options, comme le lancement d'un tableau de bord web !
```

## 👨‍💻 Feedback & Contributions

Ce projet en est encore à ses débuts. Malheureusement, je n'aurai pas le temps de faire fonctionner cet outil par défaut pour tout le monde, mais vous êtes les bienvenus d'étendre ce projet (ou [m'embaucher](https://github.com/sponsors/MadeInPierre/commissions) si vous ne pouvez pas le développer vous-même). Les pull requests, [issues](https://github.com/MadeInPierre/finalynx/issues/new) (🇬🇧 de préférence) et [discussions ouvertes](https://github.com/MadeInPierre/finalynx/discussions/new) (🇬🇧/🇫🇷) sont les bienvenues !

Si vous souhaitez contribuer à ce projet, bienvenue à bord et merci de votre intérêt ! 🎉 Veuillez lire le [guide de contribution](https://github.com/MadeInPierre/finalynx/blob/main/CONTRIBUTING.md) pour configurer le projet sur votre machine et accepter les conventions communes. Le reste de la documentation est en anglais.

## 📄 License

Ce projet est sous la [License GPLv3](https://github.com/MadeInPierre/finalynx/blob/main/LICENSE), ce qui signifie que tout le monde peut utiliser, partager, étendre et contribuer à ce projet tant que leurs changements sont intégrés à ce repo ou également publiés sous GPLv3. Contactez-moi pour toute demande de licence spécifique.

## 💌 Donations

[<img align="right" src="https://raw.githubusercontent.com/MadeInPierre/finalynx/main/docs/_static/buymeacoffee.png" width="161" />](https://github.com/sponsors/MadeInPierre)
Ceci est un projet personnel sur lequel je m'amuse pendant mon temps libre. Si vous l'avez trouvé utile et souhaitez soutenir mon travail, vous pouvez [m'offrir un café](https://github.com/sponsors/MadeInPierre) ! Cela me donnerait la motivation nécessaire pour continuer à l'améliorer 😄 Merci !

Un grand merci également à tous les contributeurs 🌹 n'oubliez pas d'aller les voir :

<a href="https://github.com/MadeInPierre/finalynx/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MadeInPierre/finalynx" />
</a>

<!-- ![Alt](https://repobeats.axiom.co/api/embed/44fc99b8a4a89962a0e1a7170f8d44cd3e9ea2e0.svg "Repobeats analytics image") -->

<!-- Breaking: :boom:

Minor: :sparkles::children_crossing::lipstick::iphone::egg::chart_with_upwards_trend:

Patch: :ambulance::lock::bug::zap::goal_net::alien::wheelchair::speech_balloon::mag::apple::penguin::checkered_flag::robot::green_apple: -->
