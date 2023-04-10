import dataclasses
from typing import TYPE_CHECKING
from . import models
from django.conf import settings
import re

import pdfplumber

if TYPE_CHECKING:
    from .models import TaxFiling

@dataclasses.dataclass
class TaxFilingDataClass:
    identificador: str
    tax_filing: str
    wages: int
    total_deductions: int
    id: int = None

    @classmethod
    def from_instance(cls, tax_filing: "TaxFiling") -> "TaxFilingDataClass":
        return cls(
            identificador=tax_filing.identificador,
            tax_filing=tax_filing.tax_filing,
            wages=tax_filing.wages,
            total_deductions=tax_filing.total_deductions,
            id=tax_filing.id,
        )

def create_tax_filing(tax_filing_dc: "TaxFilingDataClass") -> "dict":
    instance = models.TaxFiling(
        identificador=tax_filing_dc.identificador,
        tax_filing=tax_filing_dc.tax_filing,
        wages=tax_filing_dc.wages,
        total_deductions=tax_filing_dc.total_deductions,
    )
    if tax_filing_dc.id is not None:
        instance.id = tax_filing_dc.id
    instance.save()

    return TaxFilingDataClass.from_instance(instance)



def extract_data_from_pdf(pdf_file) -> "TaxFiling":
    #abrir el pdf con pdfplumber
    pdf_reader = pdfplumber.open(pdf_file)
    #extraer la primera pagina
    page = pdf_reader.pages[0]
    #extraer la tabla
    table = page.extract_text()


    #extraer el identificador marcado
    patron_identificador =  r"Your first name and middle initial Last name Your social security number\s+(\S+)"
    #buscar el patron en todo el texto directamente
    match = re.search(patron_identificador, table)
    if match:
        identificador = match.group(1)
    else:
        print("No se encontró el identificador.")



    #extraer el filing marcado
    patron_filing = r"X\s+(Single|Married filing jointly|Married filing separately \(MFS\)|Head of household \(HOH\)|Qualifying widow\(er\) \(QW\))"
    #buscar el patron en todo el texto directamente
    match = re.search(patron_filing, table)
    if match:
        filing = match.group(1)
    else:
        print("No se encontró el filing.")


    patron_wages =  r"1 Wages, salaries, tips, etc\. Attach Form\(s\) W-2\. .+? ([\d,\.]+)\."
    
    #buscar el patron en todo el texto directamente
    match = re.search(patron_wages, table)
    if match:
        wages = match.group(1).replace(",", "")
    else:
        print("No se encontró el numero de wages.")

    page_third = pdf_reader.pages[2]
    table_third = page_third.extract_text()

    #extraer 17 add admount
    patron_add_amount = r"Itemized Form 1040 or 1040-SR, line 12a\.\. .+? ([\d,\.]+)\."

    #buscar el patron en todo el texto directamente
    match = re.search(patron_add_amount, table_third)
    if match:
        total_deductions = match.group(1).replace(",", "")
    else:
        print("No se encontró el numero de add amount.")

    print(identificador)
    print(filing)
    print(wages)
    print(total_deductions)

    objectExtract = {
        "identificador": identificador,
        "tax_filing": filing,
        "wages": int(wages),
        "total_deductions": int(total_deductions),

    } 

    return objectExtract

    