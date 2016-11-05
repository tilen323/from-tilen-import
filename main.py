#!/usr/bin/env python
import os
import jinja2
import webapp2
import random
from time import gmtime, strftime
from NarediObjekt import *


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("home.html")

class KontaktHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template("kontakt.html", params=params)

class BlogHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template("blog.html", params=params)

class NalogeHandler(BaseHandler):
    def get(self):

        loto_stevila = []                                           ## - Loto
        while len(loto_stevila) < 8:
            rng_stevilo = random.randint(1, 39)
            if rng_stevilo not in loto_stevila:
                loto_stevila.append(rng_stevilo)

        datum_cas = strftime("%a, %d %b %Y %H:%M:%S", gmtime())     ## - Cas

        params = {"cas": datum_cas, "loto": sorted(loto_stevila)}
        return self.render_template("naloge.html", params=params)


class KalkulatorHandler(BaseHandler):                               ## - Kalkulator
    def post(self):
        vnos_enacbe = self.request.get("vnos-enacbe")
        if "*" in vnos_enacbe:
            rezultat_enacbe = float(vnos_enacbe.split("*")[0]) * float(vnos_enacbe.split("*")[1])
        elif "+" in vnos_enacbe:
            rezultat_enacbe = float(vnos_enacbe.split("+")[0]) + float(vnos_enacbe.split("+")[1])
        elif "-" in vnos_enacbe:
            rezultat_enacbe = float(vnos_enacbe.split("-")[0]) - float(vnos_enacbe.split("-")[1])
        else:
            rezultat_enacbe = "Nisi vnesel veljavne operacije!"

        params = {"rezultat_enacbe": rezultat_enacbe, "vnos_enacbe": vnos_enacbe}
        return self.render_template("kalkulator.html", params=params)


class Ugani_steviloHandler(BaseHandler):                            ## - Ugani stevilo
    def post(self):
        vnos_ugani_stevilo = self.request.get("vnos-ugani-stevilo")
        if len(vnos_ugani_stevilo) == 0 or len(vnos_ugani_stevilo) > 1:
            poskus = "Prosim vnesi stevilo med 1 in 10!"
        elif int(vnos_ugani_stevilo) < 7:
            poskus = "Stevilo, ki si ga vpisal je prenizko!"
        elif int(vnos_ugani_stevilo) > 7:
            poskus = "Stevilo, ki si ga vpisal je previsoko!"
        else:
            poskus = "Bravo! Za nagrado dobis keks!"

        params = {"poskus": poskus}
        return self.render_template("ugani_stevilo.html", params=params)


class PretvornikHandler(BaseHandler):                               ## - Pretvornik enot
    def post(self):
        milja = 0.62
        usd = 1.105
        lbs = 2.204
        enota = self.request.get("izberi-enoto")
        vnos_pretvornik = self.request.get("vnos-pretvornik")
        if len(vnos_pretvornik) == 0:
            rezultat_pretvorbe = "Za izracun moras vnesti stevilo!"
        elif "Km" in enota:
            sum_pretvorbe = float(vnos_pretvornik) * float(milja)
            rezultat_pretvorbe = str(vnos_pretvornik) +"km = " + str(sum_pretvorbe) + "mi"
        elif "Eur" in enota:
            sum_pretvorbe = float(vnos_pretvornik) * float(usd)
            rezultat_pretvorbe = str(vnos_pretvornik) +" Eur = " + str(sum_pretvorbe) + " Usd"
        elif "Kg" in enota:
            sum_pretvorbe = float(vnos_pretvornik) * float(lbs)
            rezultat_pretvorbe = str(vnos_pretvornik) +"kg = " + str(sum_pretvorbe) + " lbs(pound)"
        params = {"rezultat_pretvorbe": rezultat_pretvorbe}
        return self.render_template("pretvornik.html", params=params)


class Preveri_dnaHandler(BaseHandler):                              ## - Forenzicna aplikacija
    def post(self):
        barva_las = {"crna": "CCAGCAATCGC", "rjava": "GCCAGTGCCG", "blond": "TTAGCTATCGC"}
        oblika_obraza = {"pravokotna": "GCCACGG", "okrogla": "ACCACAA", "ovalna": "AGGCCTCA"}
        barva_oci = {"modra": "TTGTGGTGGC", "zelena": "GGGAGGTGGC", "o_rjava": "AAGTAGTGAC"}
        spol = {"zenska": "TGAAGGACCTTC", "moski": "TGCAGGAACTTC"}
        rasa = {"belci": "AAAACCTCA", "crnci": "CGACTACAG", "azijci": "CGCGGGCCG"}

        seznam_oseb = []

        seznam_oseb.append(OsebaDna("Eva", barva_las["blond"], oblika_obraza["ovalna"], barva_oci["modra"], spol["zenska"], rasa["belci"]))
        seznam_oseb.append(OsebaDna("Miha", barva_las["rjava"], oblika_obraza["pravokotna"], barva_oci["zelena"], spol["moski"], rasa["belci"]))

        dna_txt = self.request.get("vnos-dna")

        for a in seznam_oseb:
            if a.preveri_dna(dna_txt) == True:
                ime = "Krivec je: " + a.ime
            else:
                ime = "V nasi bazi ni osebe, ki jo iscete"

        params = {"ime": ime}
        return self.render_template("preveri_dna.html", params=params)

class KvizHandler(BaseHandler):
    def get(self):
        rng_st = random.randint(0, (len(seznam_drzav) - 1))
        rng_drzava = seznam_drzav[rng_st].drzava
        rng_slika = seznam_drzav[rng_st].url_slike
        rng_mesto = seznam_drzav[rng_st].gl_mesto
        rezultat = "Pozdravljeni v nasem kvizu!"

        params = {"drzava": rng_drzava, "slika": rng_slika, "rezultat": rezultat, "mesto": rng_mesto}
        return self.render_template("kviz.html", params=params)

    def post(self):
        vnos_kviz = self.request.get("vnos-kviz")
        pravilen_odg = self.request.get("pravilen-odg")
        pravilen_drz = self.request.get("drzava-odg")
        if vnos_kviz.lower() == pravilen_odg.lower():
            rezultat = "Odgovor je pravilen! Glavno mesto " + pravilen_drz + " je res " + pravilen_odg + "."
        else:
            rezultat = "Odgovor je napacen! Glavno mesto " + pravilen_drz + " je " + pravilen_odg + "."

        rng_st = random.randint(0, (len(seznam_drzav) - 1))
        rng_drzava = seznam_drzav[rng_st].drzava
        rng_slika = seznam_drzav[rng_st].url_slike
        rng_mesto = seznam_drzav[rng_st].gl_mesto

        params = {"drzava": rng_drzava, "slika": rng_slika, "rezultat": rezultat, "mesto": rng_mesto}
        return self.render_template("kviz.html", params=params)

seznam_drzav = []
seznam_drzav.append(GlavnaMesta("Slovenije", "Ljubljana", "https://unaprojektiranje.files.wordpress.com/2013/01/l_176_7_8enhancer.jpg"))
seznam_drzav.append(GlavnaMesta("Hrvaske", "Zagreb", "http://loveit.hr/media/uploads/public/destination/p85-zagreb_3.jpg"))
seznam_drzav.append(GlavnaMesta("Avstrije", "Dunaj", "http://7wallpapers.net/wp-content/uploads/5_Vienna.jpg"))
seznam_drzav.append(GlavnaMesta("Nemcije", "Berlin", "https://images8.alphacoders.com/710/thumb-1920-710914.jpg"))
seznam_drzav.append(GlavnaMesta("Italije", "Rim", "http://www.worldfortravel.com/wp-content/uploads/2015/07/Rome-Italy-Travel.jpg"))


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/kontakt', KontaktHandler),
    webapp2.Route('/blog', BlogHandler),
    webapp2.Route('/naloge', NalogeHandler),
    webapp2.Route('/kalkulator', KalkulatorHandler),
    webapp2.Route('/ugani_stevilo', Ugani_steviloHandler),
    webapp2.Route('/pretvornik', PretvornikHandler),
    webapp2.Route('/preveri_dna', Preveri_dnaHandler),
    webapp2.Route('/kviz', KvizHandler),
], debug=True)
