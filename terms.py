
search_terms = [
    "Rose", "Tulip", "Daffodil", "Sunflower", "Lily", "Orchid", "Marigold", "Daisy", "Peony", "Chrysanthemum",
    "Lavender", "Carnation", "Hibiscus", "Iris", "Jasmine", "Lilac", "Magnolia", "Poppy", "Violet", "Zinnia",
    "Begonia", "Camellia", "Cosmos", "Dahlia", "Freesia", "Gardenia", "Geranium", "Gladiolus", "Hyacinth", "Hydrangea",
    "Impatiens", "Larkspur", "Lotus", "Morning Glory", "Narcissus", "Oleander", "Petunia", "Primrose", "Ranunculus", "Snapdragon",
    "Sweet Pea", "Tuberose", "Verbena", "Wisteria", "Yarrow", "Aster", "Anemone", "Bluebell", "Buttercup", "Calendula",
    "Clematis", "Columbine", "Coreopsis", "Crocus", "Delphinium", "Foxglove", "Fuchsia", "Gaillardia", "Gazania", "Hellebore",
    "Hollyhock", "Jonquil", "Kalanchoe", "Lantana", "Lisianthus", "Lupine", "Monarda", "Nasturtium", "Pansy", "Phlox",
    "Plumeria", "Protea", "Rhododendron", "Salvia", "Scabiosa", "Stock", "Trillium", "Verbascum", "Wallflower", "Weigela",
    "Achillea", "Agapanthus", "Allium", "Alstroemeria", "Amaryllis", "Aquilegia", "Armeria", "Astilbe", "Balsam", "Bellflower",
    "Bird of Paradise", "Black-eyed Susan", "Blanket Flower", "Borage", "Candytuft", "Canna", "Clarkia", "Coneflower", "Cornflower", "Cyclamen"
    "Aloe Vera", "Aloe Aristata", "Aloe Polyphylla", "Agave Americana", "Agave Attenuata",
    "Echeveria Elegans", "Echeveria Lola", "Echeveria Perle von Nurnberg", "Echeveria Black Prince", "Echeveria Agavoides",
    "Haworthia Fasciata", "Haworthia Cooperi", "Haworthia Attenuata", "Haworthiopsis Limifolia", "Gasteria Verrucosa",
    "Crassula Ovata", "Crassula Perforata", "Crassula Capitella", "Crassula Tetragona", "Crassula Muscosa",
    "Sedum Morganianum", "Sedum Rubrotinctum", "Sedum Acre", "Sedum Spurium", "Sedum Clavatum",
    "Kalanchoe Tomentosa", "Kalanchoe Blossfeldiana", "Kalanchoe Thyrsiflora", "Kalanchoe Daigremontiana", "Kalanchoe Luciae",
    "Sempervivum Tectorum", "Sempervivum Arachnoideum", "Graptopetalum Paraguayense", "Graptosedum Vera Higgins", "Graptoveria Fred Ives",
    "Pachyphytum Oviferum", "Pachyphytum Compactum", "Aeonium Arboreum", "Aeonium Zwartkop", "Aeonium Kiwi",
    "Senecio Rowleyanus", "Senecio Radicans", "Curio Ficoides", "Curio Herreanus", "Portulacaria Afra",
    "Adromischus Cristatus", "Adromischus Maculatus", "Cotyledon Orbiculata", "Cotyledon Tomentosa", "Dudleya Brittonii",
    "Dudleya Pulverulenta", "Graptopetalum Superbum", "Fenestraria Rhopalophylla", "Lithops Karasmontana", "Lithops Lesliei",
    "Conophytum Bilobum", "Pleiospilos Nelii", "Titanopsis Calcarea", "Faucaria Tigrina", "Delosperma Cooperi",
    "Carpobrotus Edulis", "Lampranthus Spectabilis", "Anacampseros Rufescens", "Anacampseros Telephiastrum", "Euphorbia Tirucalli",
    "Euphorbia Milii", "Euphorbia Obesa", "Euphorbia Lactea", "Huernia Zebrina", "Stapelia Gigantea",
    "Orbea Variegata", "Aptenia Cordifolia", "Ceropegia Woodii", "Ceropegia Sandersonii", "Sansevieria Trifasciata",
    "Sansevieria Cylindrica", "Dracaena Fragrans", "Dracaena Marginata", "Zamioculcas Zamiifolia", "Peperomia Graveolens",
    "Peperomia Ferreyrae", "Peperomia Obtusifolia", "Rhipsalis Baccifera", "Schlumbergera Truncata", "Hatiora Salicornioides",
    "Epiphyllum Oxypetalum", "Opuntia Microdasys", "Opuntia Ficus-Indica", "Mammillaria Elongata", "Mammillaria Spinosissima",
    "Gymnocalycium Mihanovichii", "Astrophytum Myriostigma", "Echinocactus Grusonii", "Ferocactus Latispinus", "Rebutia Minuscula"]

def populate_terms():
    #function to populate search terms from file, returns list of search terms
    with open("terms.txt", "r") as f:
        terms = f.read().splitlines()
    return terms

def populate_template(list_terms):

    for t in list_terms:

        with  open("terms.txt", "a") as f:
            f.write(t + "\n")

def compare(list1, list2):
    #function to compare two lists and return a list of items that are in list1 but not in list2
    #return [item for item in list1 if item not in list2]

    return list(set(list1) - set(list2))


def compare_lists():
    list1 = []

    with open("terms.txt", "r") as f:
        for line in f:
            list1.append(line.strip())

    with open("failed.txt", "r") as f2:
        list2 = []
        for line in f2:
            list2.append(line.strip())

        diff = compare(list1, list2)
        print("Items in terms.txt but not in failed.txt:")
        for item in diff:
            print(item)
