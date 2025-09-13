import random
from global_variables import GLOBAL

MALE_ANIMALS = [
    "Rato",
    "Hamster",
    "Esquilo",
    "Camundongo",
    "Castor",
    "Gabiru",
    "Porquinho-da-índia",
    "Tatu",
    "Coelho",
    "Furão",
    "Porco-espinho",
    "Ouriço",
    "Lêmure",
    "Morcego",
    "Esquilo-voador",
    "Arminho",
]

FEMALE_ANIMALS = [
    "Marmota",
    "Capivara",
    "Chinchila",
    "Topeira",
    "Ratazana",
    "Lontra",
    "Lebre",
    "Doninha",
    "Rata",
    "Fuinha",
    "Camundonga",
    "Equidna",
]

NEUTRAL_ADJECTIVES = [
    "Serelepe",
    "Tchola",
    "Sapeca",
    "Mequetrefe",
    "Besta",
    "Triste",
    "Infeliz",
    "Inteligente",
    "Vidente",
    "Banguela",
    "Cegueta",
    "Nerdola",
    "Carente",
    "de iPhone",
    "Grande",
    "Paia",
    "Ciclista",
    "Motorista",
    "Captalista",
    "Comunista",
    "Socialista",
    "Anarquista",
    "Terraplanista",
    "Conspiracionista",
    "Capacitista",
    "Cientista",
    "Monarquista",
    "Futurista",
    "Carioca",
    "Paulista",
    "Taxista",
    "Petista",
    "Jovem",
    "de Schrödinger",
    "do BTS",
    "da Twitch",
    "Youtuber",
]

MALE_ADJECTIVES = [
    "Deprimido",
    "Bobão",
    "Espertinho",
    "Emburrado",
    "Estranho",
    "Preguiçoso",
    "Inchado",
    "Transtornado",
    "Cabuloso",
    "Parrudo",
    "Maluco",
    "Doidão",
    "Burro",
    "Pidão",
    "Barato",
    "Fedido",
    "Curioso",
    "Fofoqueiro",
    "Capacho",
    "Matemático",
    "Viciado",
    "Mesquinho",
    "Voador",
    "Anão",
    "Armado",
    "Motoqueiro",
    "Piloto",
    "Vascaíno",
    "Místico",
    "Quântico",
    "Túlio",
    "Twitteiro",
]

FEMALE_ADJECTIVES = [
    "Deprimida",
    "Bobona",
    "Espertinha",
    "Emburrada",
    "Estranha",
    "Preguiçosa",
    "Inchada",
    "Transtornada",
    "Cabulosa",
    "Parruda",
    "Maluca",
    "Doidona",
    "Burra",
    "Barata",
    "Curiosa",
    "Fofoqueira",
    "Matemática",
    "Viciada",
    "Mesquinha",
    "Pidona",
    "Anã",
    "Voadora",
    "Armada",
    "Motoqueira",
    "Pilota",
    "Mística",
    "Quântica",
    "Twitteira",
]


def generate_player_name() -> str:
    all_animals = MALE_ANIMALS + FEMALE_ANIMALS
    animal = random.choice(all_animals)

    if animal in MALE_ANIMALS:
        adjective_pool = NEUTRAL_ADJECTIVES + MALE_ADJECTIVES
    else:
        adjective_pool = NEUTRAL_ADJECTIVES + FEMALE_ADJECTIVES

    adjective = random.choice(adjective_pool)

    name = f"{animal} {adjective}"

    player_names = [client["player"].name for client in GLOBAL["clients"]]

    if name in player_names:
        return generate_player_name()

    return name
