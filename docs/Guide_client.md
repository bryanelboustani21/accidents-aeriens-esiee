# Démonstration à un client simulé

Le client est un responsable qualité/sécurité qui souhaite explorer une base
historique, comprendre les anomalies et comparer différents périmètres.

Application : https://accidents-aeriens-esiee-berqbs6auc7f4txjtyjxip.streamlit.app/

| Demande | Commande | Résultat à commenter |
|---|---|---|
| Comparer les périodes | Scénarios / Comparer deux périodes | 1 184 lignes sur 1980–1999, 743 sur 2000–2019. Survie pondérée de 35,02 à 30,32 %. |
| Comprendre le nettoyage | Scénarios / Traitement des données manquantes | Populations différentes selon que le pays est renseigné ou réellement résolu. |
| Examiner une hypothèse | Scénarios / Hypothèse sur la gravité | Une réduction relative de 10 % donne 101 167,2 décès théoriques sur les lignes valides. |
| Voir une variabilité | Scénarios / Monte-Carlo | 50 lignes, 1 000 répétitions, graine 42 : médiane 1 089 décès fictifs, Q05 758,95 et Q95 1 550,10. |

## Recommandations

Vérifier la couverture avant les comparaisons géographiques. Revoir manuellement
les libellés non résolus. Ajouter un dénominateur harmonisé de trafic et une
classification des opérations avant d'étudier un taux d'accident par vol.
Consolider les événements avant de compter des victimes au sol uniques.

Le dashboard ne démontre pas qu'un pays, une compagnie ou un constructeur est
plus dangereux. Les scénarios imposent des hypothèses. Les simulations ne
prévoient pas de futurs accidents.
