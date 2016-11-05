class OsebaDna():

    def __init__(self, ime, barva_las, oblika_obraza, barva_oci, spol, rasa):
        self.ime = ime
        self.barva_las = barva_las
        self.oblika_obraza = oblika_obraza
        self.barva_oci = barva_oci
        self.spol = spol
        self.rasa = rasa

    def preveri_dna(self, dna):
        if self.barva_las in dna and\
           self.oblika_obraza in dna and\
           self.barva_oci in dna and\
           self.spol in dna and\
           self.rasa in dna:
            return True
        else:
            return False

class GlavnaMesta():

    def __init__(self, drzava, gl_mesto, url_slike):
        self.drzava = drzava
        self.gl_mesto = gl_mesto
        self.url_slike = url_slike
