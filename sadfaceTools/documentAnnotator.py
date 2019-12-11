import sadface.sadface as sadf


class DocumentAnnotator:

    def annotate_claims(self, claims):

        sadf.config.set_location(r"C:\Users\ROSSA\PycharmProjects\pickaxe\etc\pickaxe.cfg")
        sadf.config.load()
        sadf.sd = sadf.init()

        sadf.set_title("Pickaxe")
        sadf.add_notes("Claim detection")
        sadf.set_description("Pickaxe essay_corpus_results")

        for claim in claims:
            con = str(claim)
            sadf.add_atom(con)
            #sadf.add_atom_metadata()

        print(sadf.prettyprint())
        jsonData = sadf.export_json()
        with open(r"C:\Users\ROSSA\PycharmProjects\pickaxe\output\sadface.json", "w") as jsonFile:
            jsonFile.write(jsonData)


if __name__ == '__main__':
    main = DocumentAnnotator()
    main.annotate_claims(['above all', 'accordingly', 'actually', 'admittedly', 'after', 'after all', 'after that',
                               'afterwards', 'again',
                               'all in all', 'all the same', 'also', 'alternatively', 'although',
                               'always assuming that', 'anyway', 'as', 'as a consequence', 'as a corollary',
                               'as a result', 'as long as', 'as soon as', 'as well', 'at any rate', 'at first',
                               'at first blush', 'at first sight', 'at first view',
                               'at the moment when', 'at the outset', 'at the same time', 'because', 'before', 'but',
                               'by comparison', 'by contrast'])
