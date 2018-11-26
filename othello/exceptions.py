"""4.2  Créer la classe d’exception
ErreurPositionCoup
Nous vous demandons d’utiliser la gestion des exceptions pour gérer l’invalidité de la po-
sition d’un coup. Vous devez donc créer une nouvelle classe d’exception dans un fichier
exceptions.py
, puis modifier votre gestion des coups pour qu’un exception
ErreurPositionCoup
soit levée lorsque le coup tenté est invalide. Vous pourrez ajouter un message personnalisé à
l’exception lors de sa création pour vous permettre de savoir si l’invalidité du coup est dûe
à la présence d’une autre pièce ou encore à l’absence de pièces ”mangées”.
3
IFT-1004 — Introduction à la programmation
TP # 4
De cette manière, le code de votre interface n’aura pas à valider la position du coup soumise
par l’usager (avec un clic de souris) : si le coup demandé était invalide, aucun coup ne sera
joué et l’interface attrapera l’exception et affichera un message d’avertissement correspon-
dant."""
