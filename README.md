# Formation IA - Formation Interactive

**Plateforme éducative gratuite sur l'IA responsable** - 15 micro-modules interactifs ludifiés pour comprendre l'intelligence artificielle de manière citoyenne.

> Proposée par [Prof Express](https://www.profexpress.com)

---

## Vue d'ensemble

### Objectif
Former le grand public (notamment les jeunes et enseignants) aux enjeux de l'IA de manière ludique et immersive, sans collecte de données personnelles (conforme RGPD pour usage éducatif avec mineurs).

### Structure
- **15 micro-modules** organisés en **4 domaines**
- Chaque module : 10-20 minutes
- Format : HTML/CSS/JS autonome (pas de backend, pas de dépendances)
- Style : **Cyberpunk/Néon** immersif

---

## Les 4 Domaines

| Domaine | Couleur | Modules | Thème |
|---------|---------|---------|-------|
| **Fondations IA** | Rouge `#ff6b6b` | 1-4 | Comprendre l'IA |
| **Interaction Raisonnée** | Cyan `#4ecdc4` | 5-8 | Utiliser l'IA efficacement |
| **Limites et Esprit Critique** | Jaune `#ffe66d` | 9-11 | Détecter les failles |
| **Enjeux Citoyens** | Vert menthe `#95e1d3` | 12-15 | Impacts sociétaux |

---

## Liste des 15 Modules

### Fondations IA (1-4)
1. **Démystifier l'IA** *(Dossier Zéro)* - Mission d'enquête ✅ *Disponible*
2. **Données sous influence** - Apprentissage & biais, jeu de simulation ✅ *Disponible*
3. **Dans la tête d'un modèle** *(NEURONAUT)* - Tokenisation, embeddings, attention, prédiction ✅ *Disponible*
4. **Générer sans comprendre** - Simulation d'un modèle génératif ⏳ *Bientôt*

### Interaction Raisonnée (5-8)
5. **L'art de la consigne** - Escape room de prompts, rédiger des consignes efficaces ⏳ *Bientôt*
6. **Itération et amélioration** - Prompt engineering, défi progressif ✅ *Disponible*
7. **Co-créer avec l'IA** - Usages créatifs ⏳ *Bientôt*
8. **Savoir quand s'arrêter** - Limites d'utilisation ⏳ *Bientôt*

### Limites et Esprit Critique (9-11)
9. **Hallucinations** *(L'Erreur qui Sonne Juste)* - Quand l'IA invente ✅ *Disponible*
10. **Biais algorithmiques** - Discrimination et équité ⏳ *Bientôt*
11. **Deepfakes** - Détection de contenus manipulés ⏳ *Bientôt*

### Enjeux Citoyens (12-15)
12. **Impact environnemental** *(Green Infiltration)* - Empreinte carbone de l'IA, escape game ✅ *Disponible*
13. **Vie privée et données** *(Data Shadow)* - Protection des informations personnelles, jeu de rôle ✅ *Disponible*
14. **IA et emploi** - Transformation du travail ⏳ *Bientôt*
15. **Le Tribunal de l'IA** - Responsabilité humaine et régulation ✅ *Disponible*

---

## Architecture Technique

### Structure des fichiers
```
formationia/
├── index.html                              # Page d'accueil
├── modules.html                            # Catalogue des modules
├── certification.html                      # Page certification (future)
├── module-01-demystifier-ia.html           # Module 1 - Mission d'enquête
├── module-02-donnees-sous-influence.html   # Module 2 - Jeu de simulation
├── module-03-dans-la-tete-du-modele.html   # Module 3 - NEURONAUT (tokenisation, embeddings…)
├── module-06-iteration-amelioration.html   # Module 6 - Prompt engineering
├── module-09-hallucinations.html           # Module 9 - Hallucinations IA
├── module-12-impact-environnemental.html   # Module 12 - Escape game environnement
├── module-13-vie-privee-donnees.html       # Module 13 - Jeu de rôle vie privée
├── module15-le-tribunal-de-l-ia.html      # Module 15 - Régulation et éthique
├── images/
│   ├── logo-profexpress.png
│   ├── hero-banner.png
│   ├── domain-*.png                        # Icônes des domaines
│   ├── room-*.png                          # Arrière-plans escape game
│   └── ...
└── README.md
```

### Stack Technique
- **HTML5** - Structure sémantique
- **CSS3** - Animations, variables CSS, flexbox/grid
- **JavaScript Vanilla** - Aucune dépendance externe
- **Fonts** : Google Fonts (Space Mono, Exo 2)

### Pas de backend
- Aucune base de données
- Aucun tracking utilisateur
- Tout fonctionne en local/statique
- Compatible hébergement GitHub Pages, Netlify, etc.

---

## Charte Graphique - ADN Visuel

### Palette de couleurs
```css
:root {
    --neon-green: #00ff88;      /* Accent principal */
    --neon-blue: #00d4ff;       /* Accent secondaire */
    --neon-cyan: #00d4ff;       /* Liens, interactions */
    --neon-pink: #ff0080;       /* Alertes, erreurs */
    --dark-bg: #0a0e17;         /* Fond principal */
    --panel-bg: rgba(10, 20, 40, 0.95);  /* Panneaux */
    --text: #e0f0ff;            /* Texte principal */
    --text-muted: #8899aa;      /* Texte secondaire */
}
```

### Typographies
- **Titres** : `'Space Mono', monospace` - Style terminal/hacker
- **Corps** : `'Exo 2', sans-serif` - Lisibilité futuriste

### Effets visuels signature
- **Glow néon** : `box-shadow: 0 0 20px rgba(0, 255, 136, 0.5)`
- **Bordures luminescentes** : `border: 1px solid rgba(0, 212, 255, 0.5)`
- **Dégradés** : `linear-gradient(135deg, var(--neon-green), var(--neon-blue))`
- **Backdrop blur** : `backdrop-filter: blur(10px)`
- **Grilles de fond** : Pattern de lignes cyberpunk

### Animations
- Transitions fluides : `transition: all 0.3s ease`
- Hover avec scale : `transform: scale(1.02)`
- Effets de scan/pulse pour éléments interactifs
- Float animation pour éléments décoratifs

---

## Structure d'un Module (Template)

### Flux utilisateur
```
1. ÉCRAN TITRE
   └── Contexte narratif + bouton "Commencer"

2. BRIEFING / COURS (si applicable)
   └── 5-8 sections de contenu pédagogique
   └── Navigation latérale
   └── Boutons Précédent/Suivant

3. PHASE DE JEU
   └── Mécanique interactive adaptée au thème
   └── Objectifs clairs + feedback visuel
   └── Progression trackée visuellement

4. QUIZ DE VALIDATION
   └── 5-10 questions sur le contenu
   └── Score minimum pour valider

5. ATTESTATION
   └── Certificat téléchargeable (HTML généré)
   └── Nom du participant
   └── Date + score
```

### Mécaniques de jeu possibles
| Type | Description | Adapté pour |
|------|-------------|-------------|
| **Escape Game** | Explorer, collecter indices, résoudre énigmes | Modules complexes, investigation |
| **Simulation** | Prendre des décisions, voir conséquences | Éthique, choix sociétaux |
| **Enquête** | Analyser documents, détecter anomalies | Deepfakes, fact-checking |
| **Jeu de rôle** | Incarner un personnage, dialogues | Biais, interactions humaines |
| **Puzzle** | Assembler, trier, catégoriser | Concepts techniques |
| **Quiz interactif** | Questions avec feedback immédiat | Tous modules |

---

## Module 12 - Référence Technique

### Spécifications
- **Fichier** : `module-12-impact-environnemental.html`
- **Lignes** : ~4400 (HTML + CSS + JS intégré)
- **Type** : Escape Game immersif
- **Durée** : 15-20 minutes

### Structure interne
```javascript
// État du jeu
const gameState = {
    currentRoom: 'corridor',
    inventory: [],
    evidence: { energy: false, water: false, models: false, manufacturing: false, co2: false },
    suspicion: 0,
    timeRemaining: 900, // 15 minutes
    // ...
};
```

### Fonctionnalités implémentées
- [x] Écran titre avec contexte narratif
- [x] 7 sections de briefing éducatif
- [x] 5 salles explorables (corridor, serveurs, contrôle, refroidissement, bureau)
- [x] Système d'inventaire (5 slots)
- [x] Collecte de 5 types de preuves
- [x] Jauge de suspicion
- [x] Timer de 15 minutes
- [x] Mini-map de navigation
- [x] Système de dialogues/SMS
- [x] Puzzles interactifs (calculs, associations)
- [x] Quiz final de certification
- [x] Génération d'attestation téléchargeable
- [x] Bouton retour vers liste des modules

---

## Attestation - Format Standard

Chaque module génère une attestation HTML téléchargeable avec :

```html
<!-- Structure de l'attestation -->
- En-tête avec logo Prof Express
- Titre "ATTESTATION DE RÉUSSITE"
- Nom du module complété
- Nom du participant (saisi à la fin)
- Date de complétion
- Score obtenu
- Liste des compétences validées
- Design cohérent avec la charte graphique
```

---

## Workflow de Développement

### Pour créer un nouveau module

1. **Dupliquer** `module-12-impact-environnemental.html` comme template
2. **Adapter** le contenu pédagogique (briefing)
3. **Choisir** la mécanique de jeu appropriée
4. **Implémenter** les interactions spécifiques
5. **Créer** les images de fond si nécessaire
6. **Ajouter** le lien dans `modules.html`
7. **Tester** le parcours complet

### Conventions de nommage
- Fichiers : `module-XX-nom-court.html`
- Images : `room-nom.png`, `icon-nom.png`
- IDs CSS : kebab-case (`#game-container`)
- Classes CSS : kebab-case (`.module-card`)
- Variables JS : camelCase (`gameState`)

---

## Versioning

### V1.0.0
- Page d'accueil (`index.html`)
- Catalogue des modules (`modules.html`)
- Module 12 complet (escape game environnement)
- Charte graphique établie
- Infrastructure de base

### V1.1.0
- Module 01 : Dossier Zéro — Mission d'enquête (Démystifier l'IA)
- Module 02 : Données sous Influence — Jeu de simulation (Apprentissage & Biais)
- Module 06 : Itération & Amélioration — Défi progressif (Prompt Engineering)
- Module 09 : L'Erreur qui Sonne Juste — Hallucinations de l'IA
- Module 13 : Data Shadow — Jeu de rôle (Vie Privée & Données)
- Module 15 : Le Tribunal de l'IA — Responsabilité humaine

### V1.2.0 (actuelle)
- Module 03 : NEURONAUT — Voyage au Cœur du Modèle (Tokenisation, Embeddings, Attention, Prédiction)

### Roadmap
- Module 4 (Fondations IA — suite)
- Modules 5, 7-8 (Interaction Raisonnée — suite)
- Modules 10-11 (Limites et Esprit Critique — suite)
- Module 14 (Enjeux Citoyens — IA et emploi)
- Page certification globale

---

## Licence et Crédits

**Projet** : Formation IA - Formation Interactive
**Éditeur** : [Prof Express](https://www.profexpress.com)
**Usage** : Éducatif, gratuit, sans tracking

---

## Contact

Pour toute question sur ce projet, contacter l'équipe Prof Express.
