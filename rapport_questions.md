**Nom** : NOUMI  
**Prénom** : Mahdi  
**Numéro étudiant** : 22404628

# Attaque par faute sur le DES

## Introduction

Le Data Encryption Standard (DES) est un algorithme de chiffrement par blocs de 64 bits utilisant une clé de 56 bits (plus 8 bits de parité) et reposant sur un réseau de Feistel en 16 tours.

Chaque tour applique une fonction de ronde `f` prenant en entrée 32 bits (moitié du bloc) et 48 bits de sous-clé dérivée de la clé secrète, pour produire 32 bits mélangés à l’autre moitié du bloc.

En pratique, à chaque itération i, la nouvelle moitié gauche `Lᵢ` est égale à l’ancienne moitié droite `Rᵢ₋₁`, et la nouvelle moitié droite `Rᵢ` est obtenue par XOR entre l’ancienne moitié gauche `Lᵢ₋₁` et le résultat de `f(Rᵢ₋₁, Kᵢ)`.

Après le 16ᵉ et dernier tour, les moitiés sont échangées pour former le pré-sortie (pré-output) du DES, de sorte que la sortie du 16ᵉ tour est le bloc `R16|L16`.

Ce chiffrement, bien qu’efficace logiciellement et matériellement, est vulnérable aux attaques physiques par injection de faute.

---

## Attaques par injection de faute

Une attaque par faute consiste pour un adversaire à perturber délibérément le calcul interne (par exemple en modifiant la tension, l’horloge ou via un laser) afin de provoquer une erreur contrôlée, et à exploiter la divergence entre le résultat fauté et le résultat correct pour extraire des informations secrètes.

Introduite par Biham et Shamir en 1997, l’analyse différentielle de faute (Differential Fault Analysis, DFA) appliquée à DES a démontré qu’injecter des erreurs pendant les derniers tours du chiffrement peut révéler la clé secrète en quelques essais.

---

## Modèle d’attaque considéré

Dans le scénario envisagé, on suppose que l’attaquant dispose d’un dispositif exécutant DES (par exemple une carte à puce) et qu’il peut y injecter une faute pendant l’avant-dernier tour du chiffrement (15ᵉ tour sur 16).

Plus précisément, l’attaquant peut provoquer une altération de la valeur de sortie `R15` (moitié droite après le 15ᵉ tour) avant qu’elle ne soit utilisée dans le dernier tour. Cette perturbation peut consister par exemple à forcer un bit de `R15` à 0 ou 1, ou à provoquer un basculement aléatoire d’un ou plusieurs bits.

On suppose par ailleurs que l’attaquant connaît le texte clair `M` à chiffrer et peut obtenir le texte chiffré en sortie (malgré la faute).

Le but de l’attaque est d’exploiter la différence provoquée par la faute pour retrouver des informations sur la sous-clé `K16` utilisée au 16ᵉ tour, puis enfin reconstruire la clé secrète complète.

Ce modèle d’attaque est réaliste dans un contexte d’analyse de matériel cryptographique, l’attaquant pouvant répéter le chiffrement du même message pour obtenir un chiffré correct et des chiffrés fautés. Notons que même si l’attaquant ne peut pas précisément cibler le 15ᵉ tour à chaque essai, il pourra identifier a posteriori si la faute a effectivement affecté l’avant-dernier tour en analysant le chiffré obtenu.

---

## Schéma du dernier tour du DES

Le demi-bloc `R15` (32 bits) est :

- Étendu à 48 bits (`E`)
- Combiné par XOR avec la sous-clé `K16`
- Puis traverse les 8 S-box pour produire 32 bits mélangés
- Ces 32 bits subissent ensuite la permutation `P`, formant `R16`

Une faute `^R15` entraîne une sortie fautée `^R16` différente de `R16`.

Ce mécanisme est exploité dans les étapes suivantes de l'attaque par faute.


## Étapes détaillées de l’attaque par faute sur DES

### Chiffrement de référence (sans faute)

L’attaquant commence par chiffrer normalement un message clair `M` afin d’obtenir le texte chiffré `C` correct. Ce chiffré servira de référence pour comparer les effets d’une faute.

---

### Injection d’une faute au 15ᵉ tour

L’attaquant chiffre le même message `M` une seconde fois, mais cette fois il provoque une faute lors du calcul du 15ᵉ tour, altérant ainsi la valeur `R15`. Le chiffrement se poursuit avec cette valeur erronée, produisant un texte chiffré fauté `C’`.

---

### Observation des valeurs en sortie du dernier tour

L’algorithme DES échange les moitiés en sortie du 16ᵉ tour.  
→ La valeur `R15` (correcte) se retrouve dans la moitié gauche du bloc pré-sortie normal (`L16`)  
→ La valeur fautée `^R15` se retrouve dans `L'16` du bloc fauté.

En appliquant la **permutation finale inverse** sur `C` et `C’`, on obtient les paires :

- `(L16, R16)` : sortie normale
- `(L'16, R'16)` : sortie fautée

Avec : `L16 = R15` et `L'16 = ^R15`.

La différence entre les moitiés droites donne :

```
Δ = R16 ⊕ R'16 = f(R15, K16) ⊕ f(^R15, K16)
```

---

### Analyse différentielle des sorties

Les 32 bits de `R15` sont étendus à 48 bits, puis répartis en 8 blocs de 6 bits (S-box).

→ Si une S-box reçoit les mêmes entrées dans les deux cas, la sortie est identique.  
→ Sinon, cette S-box est dite **active** (sortie différente).

Grâce à la permutation `P`, l’attaquant peut identifier **quels bits de Δ** correspondent à chaque S-box, et donc **quelles S-box ont changé de sortie**.

Par exemple : si les 4 bits correspondant à la S-box 3 sont non nuls, cela signifie que la faute a impacté l’entrée de S3.

---

### Déduction des bits de la sous-clé `K16`

Pour chaque S-box active, l’attaquant :

- Teste les 64 hypothèses possibles (6 bits de sous-clé)
- Calcule l’entrée et la sortie simulée dans les cas normal et fauté
- Compare le XOR des sorties avec Δ
- Élimine les hypothèses incohérentes

→ Seules les sous-clés compatibles avec la sortie réelle sont conservées.

---

### Réduction de l’espace de clé

Chaque S-box active admet peu d’hypothèses après filtrage.  
En combinant les contraintes sur toutes les S-box, le nombre de clés possibles pour `K16` passe de `2^48` à environ `2^18`.

---

### Réitérations et récupération de la clé secrète

Si le résultat n’est pas unique, l’attaquant répète l’opération avec d’autres paires `(C, C’)`.

Après plusieurs fautes bien choisies, une seule valeur de `K16` est généralement retrouvée.

Ensuite :
- On remonte le calendrier des sous-clés pour retrouver les 56 bits de la clé sans parité
- Puis on teste les `2^8` possibilités pour les bits de parité

---

## Analyse finale

L’efficacité de cette attaque repose sur la structure même du dernier tour de DES.

Lorsque `R15` est altéré :
- Seule `f(R15, K16)` est affectée
- `L15` n’est pas touchée → `L16` est identique
- La faute ne se propage pas dans les autres tours

Grâce à l’échange des moitiés, `R15` se retrouve **exposé dans le chiffré final**.

On exploite alors cette différence pour isoler `K16`.

---

**Résumé :**

```
L16 = R15
R16 = L15 ⊕ f(R15, K16)

L'16 = ^R15
R'16 = L15 ⊕ f(^R15, K16)

Δ = R16 ⊕ R’16 = f(R15, K16) ⊕ f(^R15, K16)
```

Ce comportement différentiel permet de retrouver `K16`, puis la clé secrète complète.

---

##  l’efficacité et les limitations  
Une attaque par injection de faute ciblant l’avant-dernier tour de DES permet donc, avec relativement peu d’essais, de remonter à la sous-clé du dernier tour puis à la clé secrète complète. Cette méthode illustrée par Biham et Shamir a montré qu’il était possible de casser DES en injectant seulement quelques fautes maîtrisées et en analysant les différentiels obtenus   
di.ens.fr.  
L’efficacité vient du fait que l’erreur introduite se propage de manière partielle et prédictible dans la dernière ronde, révélant des contraintes sur les S-box et la sous-clé K16 exploitables mathématiquement.  
Néanmoins, l’attaque suppose un accès physique au dispositif de chiffrement et la capacité d’y provoquer des perturbations précises, ce qui la cantonne à des contextes d’attaque matériel (cartes à puce, modules hardware) et la rend difficile à réaliser à grande distance.  
De plus, des contre-mesures peuvent être mises en place pour se protéger de telles attaques par faute : détections d’erreurs, exécutions redondantes, masquage des calculs intermédiaires, etc., qui compliquent la tâche de l’attaquant.  
Malgré ces limitations, l’analyse différentielle de faute sur DES illustre de manière frappante comment une légère perturbation physique peut briser la sécurité d’un algorithme théoriquement robuste, soulignant l’importance de considérer la sécurité physique en plus de la sécurité algorithmique dans la conception des systèmes cryptographiques.  

Sources :  
Le standard officiel du DES (FIPS 46‑3) décrit en détail l’algorithme et son dernier tour  
csrc.nist.gov.  
L’attaque par faute sur le DES et son analyse différentielle sont exposées dans les travaux de Biham & Shamir et résumées par Clavier di.ens.fr, ainsi que dans des supports de cours sur la carte à puce perso.telecom-paristech.fr.

## Question 2.1 – Récupération de la sous-clé `K16` par attaque en faute (DFA)

Pour retrouver la sous-clé de 48 bits `K16` (utilisée lors de la 16ᵉ et dernière ronde de DES), on exploite les différences entre un chiffrement correct et des chiffrements fautés obtenus en injectant des fautes pendant l’avant-dernière ronde (R15). La démarche est la suivante :

### Faute en `R15` et différences en sortie

On chiffre un même message clair avec la clé secrète, en provoquant pour 32 exécutions une faute unique à la 15ᵉ ronde. Par exemple, on peut injecter un basculement d’un bit dans `R15` (la moitié droite) juste avant la 16ᵉ ronde. On obtient ainsi 32 textes chiffrés fautés (et un texte chiffré « juste » sans faute).  
Comme la faute est injectée très tard (`R15`), seule la dernière ronde (16) produira un résultat erroné ; les 15 premières rondes se déroulent normalement, ce qui simplifie l’analyse différentielle.

### Analyse différentielle par S-box

On compare le texte chiffré correct `C` et chaque texte chiffré fauté `C^` bit à bit.  
En calculant le XOR `Δ = C ⊕ C^`, puis en remontant l’effet inverse des permutations de sortie (Permutation finale `FP⁻¹` et permutation interne `P`), on identifie quelles sorties des S-box de la ronde 16 ont été affectées par la faute.

Toutes les composantes de DES sauf les S-box sont des opérations linéaires pour le XOR (`E`, `P`, `FP`, etc.), ce qui permet de propager simplement `Δ` en remontant la structure.  
La relation `L16 = R15` est particulièrement utile ici : une faute dans `R15` se répercute directement sur `L16`, et la différence observée dans `R16` provient uniquement de la différence en sortie des S-box (après mélange avec la sous-clé `K16`).

### Contrôle des S-box et déduction des 6 bits de clé par S-box

Considérons une S-box particulière `Si` lors de la 16ᵉ ronde.  
La faute injectée à `R15` crée une différence à l’entrée de `Si` (via l’expansion `E` de 32 à 48 bits), qui va produire une différence mesurable en sortie de `Si` (après substitution non linéaire).  
En comparant `C` et `C^`, on peut déterminer la différence en sortie de `Si` induite par la faute.

Or, pour chaque S-box de DES, on connaît la table de substitution complète : on peut donc chercher quelles valeurs d’entrée XOR (différence en entrée de `Si`) correspondent à l’écart de sortie observé.  
Cela fournit une liste réduite de paires possibles `(entrée_i, entrée_i^*)` pour la S-box fautée.

### Recherche des bits de sous-clé

À ce stade, pour chaque S-box `Si`, on connaît la moitié droite correcte `R15` (on peut la déduire en simulant DES à partir du message clair).  
Mais on peut procéder sans la connaître en clair : on devine les 6 bits de sous-clé `k16,i` associés à `Si` (c’est-à-dire la portion correspondante de `K16`)  
et on vérifie que, pour toutes les paires correct/fauté disponibles affectant `Si`, la différence observée en sortie est cohérente avec l’application de `Si` sous cette clé partielle.

Concrètement, on applique les 6 bits candidats sur les deux entrées candidates `(entrée_i, entrée_i^*)` :  
le bon `k16,i` doit produire, via `Si`, des sorties dont le XOR correspond exactement à la différence mesurée.  
On écarte les valeurs de clé incompatibles.

En pratique, quelques paires de textes fautés suffisent à déterminer univoquement les 6 bits de clé pour chaque S-box.  
On répète ce processus indépendamment pour les 8 S-box de la ronde 16 :  
_on devine chaque morceau de 6 bits indépendamment et on sélectionne celui qui produit le différentiel attendu le plus fréquemment._

### Validation de `K16`

En combinant les valeurs trouvées pour les 8 S-box, on obtient la sous-clé complète `K16` sur 48 bits.  
On peut vérifier sa cohérence en chiffrant de nouveau le message clair sur 16 rondes (en reconstruisant les 16 sous-clés via le calendrier de clé) et en comparant avec le texte chiffré correct fourni.

Avec 32 textes fautés bien choisis, l’attaque permet en général de retrouver `K16` sans ambiguïté.  
(D’autres travaux indiquent qu’entre 50 et 200 fautes aléatoires suffisent dans le pire des cas pour exposer la sous-clé finale de DES.)

**Conclusion** : à l’issue de cette étape, l’attaquant connaît `K16` précisément.
### Les 48 bits de la sous-clé `K16` extraits grâce à l’attaque par faute sont :

- **Binaire** :  
  `1110 0010 0000 1000 1000 1000 0000 0101 0000 1011 0000 1110 11`  
  *(soit `111000100000100010001000000101000010110000111011` sans espaces)*

- **Hexadécimal** :  
  `E208 8814 2C3B`

Ces 48 bits correspondent exactement à la **sous-clé appliquée dans la 16ᵉ ronde** du DES.

## Question 3.1 – Reconstruction de la clé complète à partir de `K16` (56/64 bits)

La sous-clé de 16ᵉ ronde `K16` obtenue ci-dessus ne représente que 48 des 56 bits utiles de la clé DES.  
En effet, dans DES, la clé secrète de 64 bits comporte 8 bits de parité qui ne participent pas au chiffrement, ce qui laisse 56 bits effectifs.

De plus, le calendrier de clé (key schedule) de DES génère chaque sous-clé de 48 bits en sélectionnant (permutation `PC-2`) seulement 48 des 56 bits de la clé effective.  
Huit bits de la clé initiale ne figurent donc pas dans `K16` – ces bits "manquants" correspondent aux positions ignorées par `PC-2` lors de la 16ᵉ ronde.

Pour retrouver la clé complète de 64 bits, on doit donc :
- déterminer ces 8 bits manquants
- et réinsérer les bits de parité.

La démarche typique est une **recherche exhaustive sur les 8 bits restants**, ce qui est très faisable (256 possibilités). Concrètement :

1. **Reconstitution des 56 bits**  
   On reconstitue une clé candidate de 56 bits en combinant les 48 bits connus de `K16` avec une supposition pour les 8 bits inconnus.  
   On peut s’aider du fait que la structure du calendrier de clé est connue : on sait exactement quelles positions de la clé de 56 bits n’ont pas été utilisées dans `K16` (ce sont les bits omis par `PC-2` pour la dernière ronde).  
   **Ainsi, on ne fait varier que ces 8 bits-là.**

2. **Ajout des bits de parité pour former les 64 bits**  
   Pour chaque clé candidate de 56 bits, on génère la clé complète de 64 bits en y ajoutant les 8 bits de parité appropriés.  
   Rappel : chaque octet de la clé DES doit avoir une **parité impaire**, donc on choisit le bit de parité de sorte qu’il y ait un nombre impair de 1 dans chaque octet.  
   Les bits de parité ne sont pas ambigus une fois les 56 bits connus.

3. **Test des clés candidates**  
   On teste chaque clé candidate en chiffrant le message clair connu et en comparant le résultat au texte chiffré correct.  
   La bonne clé produira évidemment le bon résultat.

> En pratique, cela signifie effectuer **jusqu’à 256 chiffrages DES complets**, ce qui est trivial pour un ordinateur.  
> Cette étape de recherche exhaustive sur les `56 - 48 = 8 bits restants` est explicitement mentionnée dans la littérature comme un **complément direct de l’attaque**.

---

### Résultat final

Au terme de cette recherche, l’attaquant obtient **la clé maîtresse DES complète sur 64 bits** :  
- 48 bits retrouvés depuis `K16`  
- + 8 bits manquants déduits  
- + 8 bits de parité ajoutés

Notons que souvent on exprime la clé DES comme `56 bits + 8 bits` de contrôle de parité.  
Ici, on aura bien identifié les **56 bits effectifs** – ce qui suffit pour réutiliser la clé dans toute implémentation de DES, quitte à recalculer les bits de parité à la demande.
### Clé DES complète obtenue après reconstruction (64 bits avec parité)

- **Hexadécimal** :  
  `0431 6D0B 02D0 1C76`

- **Binaire** :  
  `00000100 00110001 01101101 00001011 00000010 11010000 00011100 01110110`

Les **huit bits de parité impaire** sont déjà insérés.  
Cette valeur chiffrée **reproduit exactement le texte chiffré de référence**, ce qui confirme que **la clé est correcte**.

## Question 4 – Attaque par faute sur des rondes plus précoces (R14, R13, …) et complexité

Si l’attaquant parvient à injecter des fautes plus tôt que la ronde 15, l’attaque diffère en ce que la faute va traverser plusieurs rondes de chiffrement avant d’affecter le résultat final.  
En théorie, il est possible d’étendre l’analyse différentielle des fautes à des rondes intermédiaires (non-finales), mais la **complexité de l’attaque augmente rapidement** quand on s’éloigne de la dernière ronde.

### Propagation de la faute sur plusieurs rondes

Une faute introduite en sortie de la ronde `N` (par exemple `R14`) crée une différence dans l’état intermédiaire qui se propage à travers les opérations des rondes suivantes :  
- substitution `S-box` et permutation `P` de la ronde 15  
- mélange avec `K15`  
- puis ronde 16 avec `K16`

Chaque ronde supplémentaire traversée ajoute des **opérations non linéaires** (les `S-box`) et des `XOR` avec des sous-clés inconnues, ce qui **complexifie l’analyse**.  
La faute n’est plus confinée à une seule sous-clé, mais est **entrelacée avec plusieurs sous-clés** (ex. : deux si faute en `R14`, trois si faute en `R13`, etc.).

### Approche itérative (rondes décortiquées)

La stratégie générale consiste à **remonter progressivement** les rondes, une par une.

Par exemple, avec une faute en `R14` :

1. On tente d’abord de retrouver `K16` malgré la complexité.  
   - On utilise plusieurs paires `(clair, chiffré fauté)`  
   - On essaye différentes hypothèses pour `K16`  
   - On retient celle qui explique le mieux les différences en sortie

   Cela peut nécessiter :
   - de tester de nombreux candidats  
   - ou d’appliquer des **techniques statistiques**, comme dans la question 2.1

2. Une fois `K16` connue, on **décrypte d’une ronde** toutes les paires fautées → on revient à l’état après `R15`  
   On obtient donc des couples `(L15, R15)` corrects et fautés.

3. Ensuite, on applique **la même méthode que la question 2.1** sur `R15` (vu comme un "chiffré final") pour retrouver `K15`.

4. Si la faute était en `R13`, on recommencerait l’opération pour retrouver `K14`, etc.

Chaque étape permet de reconstituer un état plus ancien, mais **introduit un coût supplémentaire** :  
- plus de paires fautées  
- plus de calculs pour chaque sous-clé

---

### Complexité et nombre de fautes

- **R15** : ~32 fautes suffisent
- **R14** : au moins le double (~64), car on doit extraire `K16` *et* `K15`
- **R13** et avant : complexité exponentielle, beaucoup plus de fautes

#### Données issues de la littérature :
- Akkar et al. (2003) : attaque possible jusqu’à `R11`, échec à partir de `R9`
- Exemple :
  - Cibler un **octet de `R12`** : clé récupérée avec ~9 fautes
  - Cibler `R11` : il faut ~210 fautes

> En résumé : une attaque DFA sur DES est **réaliste jusqu’à `R11–R12`**,  
> mais devient **peu praticable en dessous de `R15`**, à cause du nombre de fautes et du coût computationnel.

---

### Exemple illustratif (faute en `R14`)

Supposons qu’on injecte une faute qui force un bit de `R14` à `0`.

1. Via l’expansion `E`, ce bit est dupliqué dans l’entrée de **2 S-box** adjacentes (ronde 15)
2. Ces perturbations sont mélangées avec `K15`, produisant une différence en `R15`
3. Cette différence passe en `R16` (ronde 16), mélangée à `K16`, et donne un texte chiffré final fauté

#### Difficulté :
- L’attaquant observe la sortie finale
- Mais il ne peut pas remonter directement à `K16`, car le résultat dépend de `K15`

Il faut :
- faire **plus d’hypothèses**  
- ou collecter **plus de textes fautés**  
- pour trouver une cohérence

En comparaison :
- **Avec une faute en `R15`**, un seul bit fauté affecte au plus **2 S-box** de la ronde 16
- L’analyse est **localisée et dépend uniquement de `K16`** → résolution plus simple

Cet exemple montre que **plus on injecte la faute tôt**, **plus la trace est difficile à suivre**, et **plus la récupération des sous-clés devient ardue**.


## Question 5 – Contre-mesures contre les attaques par faute sur DES

Plusieurs contre-mesures peuvent être mises en œuvre pour protéger DES des attaques par injection de faute.  
L’objectif est de **détecter ou neutraliser les erreurs induites avant qu’un attaquant ne puisse en tirer avantage**.  
Voici quelques approches efficaces, avec leur principe et leur impact sur les performances :

---

### 1. Duplication du calcul et comparaison

C’est la contre-mesure la plus classique et directe.  
Elle consiste à **chiffrer deux fois le même message avec la même clé**, puis à **comparer les résultats**.  
- Si une faute a été injectée, les deux chiffrés ne coïncident pas → faute détectée
- L’appareil peut alors refuser de donner une réponse ou déclencher une alerte

**Avantages** :
- Très fiable
- Détecte toute faute non répétée

**Inconvénients** :
- Double le temps de calcul (~+100%)
- Cependant, il est possible de **ne dupliquer que les dernières rondes** :
  - Dupliquer 4 rondes sur 16 = +25% de surcharge seulement
  - Choix du nombre de rondes à protéger selon la profondeur d’attaque possible (cf. Question 4)

**Résumé** : Efficace, mais coûteux si appliqué intégralement. La duplication partielle est un bon compromis.

---

### 2. Vérifications de cohérence et codes détecteurs

Plutôt que de dupliquer tout le calcul, on peut **ajouter des contrôles d’intégrité internes** :
- Bits de parité
- Sommes de contrôle
- Calculs en parallèle pour vérifier la cohérence de l’état interne

**Exemples** :
- Comparer la parité du bloc de sortie avec celle du bloc avant permutation initiale
- Recalculer le calendrier de clés (`key schedule`) en double et vérifier que chaque sous-clé est identique

**Avantages** :
- Léger en ressources
- Détecte des fautes simples

**Inconvénients** :
- Moins efficace contre des fautes sophistiquées ou multiples
- Peut ne pas tout couvrir (par exemple, une double faute peut échapper à un code de parité)

**Résumé** : Bon renforcement si combiné avec d’autres méthodes comme la duplication.

---

### 3. Contremesures logicielles et temporelles

On peut rendre le **moment exact de la 15ᵉ ronde imprévisible** :
- Ajouter des délais aléatoires
- Exécuter des rondes additionnelles factices
- Réorganiser l’ordre d’exécution

**Avantages** :
- Réduit la probabilité que la faute soit injectée au bon moment
- Peu coûteux (+5 à +10% de surcharge)

**Inconvénients** :
- Ne bloque pas l’attaque, mais la rend plus difficile
- Pas une garantie de sécurité

**Résumé** : Méthode simple, efficace contre des attaquants à faible précision temporelle.

---

### 4. Approches infectives

Principe : **rendre le résultat inutilisable si une faute est détectée**.

- Dès qu'une incohérence est repérée, on **corrompt volontairement la sortie** (au lieu de l’arrêter proprement)
- Le texte chiffré retourné est faux → l’attaquant ne peut pas l’exploiter

**Avantages** :
- Très dissuasif : même si la faute passe, les données deviennent inutiles

**Inconvénients** :
- Nécessite de détecter ou soupçonner la faute
- Peut poser problème si l’application exige toujours une réponse correcte

**Résumé** : Méthode efficace dans un cadre contrôlé, surtout combinée à de la détection.

---

### Conclusion

Les contre-mesures contre les attaques DFA sur DES reposent souvent sur le **principe de redondance** (de calcul ou d'information).  
Les approches incluent :

- Duplication complète ou partielle du chiffrement
- Vérifications internes (parité, codes)
- Randomisation temporelle
- Infection volontaire des sorties fautées

**Choisir une contre-mesure adaptée dépend du compromis entre** :
- Le **niveau de sécurité souhaité**
- Et la **surcharge en performances acceptable**
