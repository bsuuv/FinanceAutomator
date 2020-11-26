"""Määrittelee luokan ReportWriter ja sen riippuvuudet"""
from datetime import datetime
from os.path import join
import json
from .report_reader import ReportReader

class ReportWriter:
    """Huolehtii talousraporttien kirjoittamisesta ja tulostamisesta. Raportti
    kirjoitetaan konstruktorin parametrina annettavan
    values_by_category-sanakirjan perusteella. Raporttien tallennussijainti
    määritellään sanakirjaparametrin locations kohdassa "save" """

    def __init__(self, values_by_category, save_dir):
        self.date_format = "%Y-%m-%d"
        self.values_by_category = values_by_category
        self.save_dir = save_dir
        self.timestamp = datetime.now().strftime(self.date_format)

    def write_human_readable_report(self, title=""):
        """Kirjoittaa raportin selkokielisenä käyttäjän määrittämään
        tallennuskansioon tiedostonimellä "fa_report.txt". Uudet raportit
        kirjoitetaan aina samaan tiedostoon. "fa_report.txt" on vakio nimi
        raporttitiedostolle, mutta vaihtoehtoisen tiedostonimen voi antaa
        summaraporttien (joita ei lueta ohjelmallisesti) tallentamista varten."""

        report = self._build_human_readable_report(title)
        filename = "fa_report.txt" if title in "" else title
        filepath = join(self.save_dir, filename)
        with open(filepath, "a", encoding="UTF-8") as human_readable_report:
            human_readable_report.write(report)

    def _build_human_readable_report(self, title):
        title = f"\nTalousraportti {self.timestamp}\n" if title in "" else title
        report = title

        for category, value in self.values_by_category.items():
            report += f"{category}: {value}\n"

        return report

    def print_human_readable_report(self, title=""):
        """Tulostaa raportin."""

        print(self._build_human_readable_report(title))

    def write_machine_readable_report(self):
        """Kirjoittaa raportin JSON-muodossa käyttäjän määrittämään
        tallennuskansioon tiedostonimellä "fa_report_mr.txt". Uudet raportit
        kirjoitetaan aina samaan tiedostoon."""

        filepath = join(self.save_dir, "fa_report_mr.txt")

        report_reader = ReportReader(self.save_dir)
        reports = report_reader.read_all_reports(filepath)

        new_report = self._build_machine_readable_report()
        reports.append(new_report)
        # default on funktio, joka ajetaan kaikille kohdattaville oliolle,
        # joita ei voida serialisoida!
        with open(filepath, "w", encoding="UTF-8") as report_file:
            json.dump(reports, report_file, ensure_ascii=False, indent=4, default=str)

    def _build_machine_readable_report(self):
        report_dict = self.values_by_category
        report_dict["timestamp"] = self.timestamp
        return report_dict
