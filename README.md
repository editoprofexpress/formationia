# Formationia — Fondamentaux et usages de l'intelligence artificielle

**Plateforme éducative gratuite — Fondamentaux et usages de l'intelligence artificielle** — 15 micro-modules interactifs ludifiés pour comprendre, utiliser et questionner l'intelligence artificielle de manière citoyenne.

> Proposée par [Prof Express](https://www.profexpress.com)

---

## Démarrage rapide

```bash
git clone <url-du-repo>
cd formationia
open index.html        # macOS
xdg-open index.html    # Linux
```

Aucun serveur ni build requis. Tous les fichiers fonctionnent directement en local ou sur n'importe quel hébergeur statique.

---

## Vue d'ensemble

| | |
|---|---|
| Modules | 15 micro-modules (10–20 min chacun) |
| Domaines | 4 domaines de compétences |
| Durée totale | ~15 heures |
| Format | HTML/CSS/JS autonome — zéro backend, zéro tracking |
| Conformité | Compatible RGPD pour usage éducatif avec mineurs |
| Style | Cyberpunk / Néon immersif |

---

## Structure des fichiers

```
formationia/
├── index.html                              # Page d'accueil
├── modules.html                            # Catalogue des 15 modules
├── certification.html                      # Page de certification finale
│
├── module1.html                            # Module 01 – Démystifier l'IA
├── module-02-donnees-sous-influence.html   # Module 02
├── module-03-dans-la-tete-du-modele.html   # Module 03
├── module-04-generer-sans-comprendre.html  # Module 04
├── module-05-art-de-la-consigne.html       # Module 05
├── module-06-iteration-amelioration.html   # Module 06
├── module-07-co-creer-ia.html              # Module 07
├── module-08-choisir-bon-usage.html        # Module 08
├── module-09-hallucinations.html           # Module 09
├── module-10-biais-algorithmiques.html     # Module 10
├── module-11-signal-falsifie.html          # Module 11
├── module-12-impact-environnemental.html   # Module 12
├── module-13-vie-privee-donnees.html       # Module 13
├── module-14-ia-et-emploi.html             # Module 14
├── module15-le-tribunal-de-l-ia.html       # Module 15
│
├── images/                                 # Ressources graphiques (fonds, logos, icônes)
│
├── fix_badge_merge.py                      # Script maintenance : fusion badge + n° module
└── fix_all.py                              # Script maintenance : couleurs, barres, footer
```

---

## Catalogue des modules

### Domaine 1 — Fondations IA `#ff6b6b`

| # | Fichier | Titre | Univers / Mission | Activité | Leçons |
|---|---------|-------|-------------------|----------|--------|
| 01 | `module1.html` | 🕵️‍♂️ Démystifier l'IA | DOSSIER ZÉRO · VERIT-IA | Mission d'enquête | 8 |
| 02 | `module-02-donnees-sous-influence.html` | 🧬 Données sous influence | LABORATOIRES SYNAPTIK | Jeu de simulation | 8 |
| 03 | `module-03-dans-la-tete-du-modele.html` | 🧠 Dans la tête du modèle | NEURONAUTE | Exploration interactive | 5 |
| 04 | `module-04-generer-sans-comprendre.html` | 🧠 Générer sans comprendre | SYNTHÈSE | Simulation | — |

### Domaine 2 — Interaction Raisonnée `#4ecdc4`

| # | Fichier | Titre | Univers / Mission | Activité | Leçons |
|---|---------|-------|-------------------|----------|--------|
| 05 | `module-05-art-de-la-consigne.html` | 🤖 L'art de la consigne | ARIA-7 LAB | Escape Room | 5 |
| 06 | `module-06-iteration-amelioration.html` | 🎯 Itération et amélioration | STUDIO ITERATEK | Défi progressif | 8 |
| 07 | `module-07-co-creer-ia.html` | 🎨 Co-créer avec l'IA | SYNAPSE STUDIO | Ateliers créatifs | — |
| 08 | `module-08-choisir-bon-usage.html` | 🧭 Choisir le bon usage | NEXUS DÉCISION | Triage de cas | — |

### Domaine 3 — Limites & Esprit Critique `#ffe66d`

| # | Fichier | Titre | Univers / Mission | Activité | Leçons |
|---|---------|-------|-------------------|----------|--------|
| 09 | `module-09-hallucinations.html` | 🔍 L'erreur qui sonne juste | RÉDACTION VERITAS NEWS | Enquête d'investigation | 9 |
| 10 | `module-10-biais-algorithmiques.html` | ⚖️ Biais invisibles | AGENCE EQUITYWATCH | Simulation d'audit | — |
| 11 | `module-11-signal-falsifie.html` | 🎭 Signal Falsifié | UNITÉ VERITAS | Investigation forensique | 7 |

### Domaine 4 — Enjeux Citoyens `#95e1d3`

| # | Fichier | Titre | Univers / Mission | Activité | Leçons |
|---|---------|-------|-------------------|----------|--------|
| 12 | `module-12-impact-environnemental.html` | 🔐 Impact environnemental de l'IA | INFILTRATION VERTE | Escape Game | — |
| 13 | `module-13-vie-privee-donnees.html` | 🛡️ Vie privée & données | AGENCE SHIELD DATA | Jeu de rôle | — |
| 14 | `module-14-ia-et-emploi.html` | ⚙️ IA et Emploi | AGENCE ARIA | Simulation de carrière | 8 |
| 15 | `module15-le-tribunal-de-l-ia.html` | ⚖️ Le Tribunal de l'IA | LE TRIBUNAL | Tribunal simulé | — |

---

## Architecture d'un module

Chaque fichier HTML est structuré en 4 écrans navigués par JavaScript, sans rechargement de page :

```
1. Écran titre
   └── Contexte narratif, personnage du module, badge domaine, CTA "Commencer"

2. Briefing / Cours
   ├── Sidebar gauche : liste des leçons + accès Mission + Attestation (verrouillée)
   ├── Zone contenu : leçons 1…N (chargées dynamiquement)
   └── Footer : boutons "← Précédent" / "Suivant →"
        (dernière leçon → "Ouvrir [mission] →")

3. Mission / Jeu
   └── Activité gamifiée adaptée au thème
       (escape room, simulation, tribunal, triage…)

4. Quiz + Attestation
   └── QCM de validation (score minimum : 70 %)
   └── Attestation HTML téléchargeable (nom, date, score, compétences)
```

---

## Design system

### Typographies

| Rôle | Police |
|------|--------|
| Titres, interface | Space Mono (monospace) |
| Corps de texte | Exo 2 / Inter |

### Palette de base

```css
:root {
  --neon-green:  #00ff88;          /* Accent principal */
  --neon-blue:   #00d4ff;          /* Accent secondaire */
  --neon-pink:   #ff0080;          /* Alertes */
  --dark-bg:     #0a0e17;          /* Fond principal */
  --panel-bg:    rgba(10,20,40,.95);
  --text:        #e0f0ff;
  --muted:       #8899aa;
}
```

### Couleurs par domaine

Chaque module expose une variable `--domain-color` dans son `:root` :

| Domaine | `--domain-color` | Usages |
|---------|-----------------|--------|
| Fondations IA | `#ff6b6b` | Badge, `briefing-title`, titres `h3` |
| Interaction Raisonnée | `#4ecdc4` | Badge, `briefing-title`, titres `h3` |
| Limites & Esprit Critique | `#ffe66d` | Badge, `briefing-title`, titres `h3` |
| Enjeux Citoyens | `#95e1d3` | Badge, `briefing-title`, titres `h3` |

### Badge de domaine (format standardisé)

Tous les modules affichent en haut de l'écran titre un badge unique au format :

```
[Nom du domaine - Module n°NN]
```

Exemple : `Enjeux Citoyens - Module n°12`

---

## Hébergement statique

| Plateforme | Config |
|------------|--------|
| GitHub Pages | Pages sur `main`, dossier racine |
| Netlify | Glisser-déposer ou `netlify deploy` |
| Vercel | `vercel --prod` |
| Apache / Nginx | Copier dans `www/` ou `public_html/` |

---

## Conventions de nommage

```
module-{NN}-{slug}.html    →  modules 02–14  (format principal)
module{N}.html             →  module 01      (format historique)
module{NN}-{slug}.html     →  module 15      (format alternatif)
```

---

## Scripts de maintenance

| Script | Rôle |
|--------|------|
| `fix_badge_merge.py` | Fusionne le numéro de module dans le badge de domaine sur tous les modules |
| `fix_all.py` | Harmonisation couleurs titres, suppression barres de progression, ajout footer module 14 |

---

## Statut du projet

- [x] 15 modules HTML autonomes et complets
- [x] 4 domaines avec code couleur harmonisé (`--domain-color`)
- [x] Badge domaine unifié sur tous les modules (`Domaine - Module n°NN`)
- [x] Couleurs des titres (`briefing-title`, `h3`) alignées sur la couleur du domaine
- [x] Barres de progression dossier/section supprimées
- [x] Footer de navigation (Précédent / Suivant) présent sur tous les modules
- [x] Attestations téléchargeables par module
- [ ] Page de certification inter-modules (`certification.html`) — en cours

---

## Licence et crédits

**Éditeur** : [Prof Express](https://www.profexpress.com)
**Usage** : Éducatif, gratuit, sans tracking ni collecte de données
