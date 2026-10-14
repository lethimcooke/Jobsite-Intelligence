"""Metro definitions shared by the Jobsite Intelligence pull scripts.

TCEQ Central Registry files use county names. The Comptroller sales-tax file uses
three-digit county codes (alphabetical county number), checked against outlet cities
on 2026-10-14.
"""

# The five regional TCEQ Central Registry files on data.texas.gov. A county can
# appear in any of them, so every pull queries all five.
TCEQ_FILES = {
    "msah-s2rv": "Central Texas (regions 9, 11, 13)",
    "5eqq-7nad": "North Texas",
    "t34q-qzi3": "Dallas / Fort Worth",
    "tzyg-j7q4": "Coastal & East Texas",
    "9iad-hrn8": "Border & Permian Basin",
}

METROS = {
    "Austin": {
        "counties": {"TRAVIS": "227", "WILLIAMSON": "246", "HAYS": "105", "BASTROP": "011", "CALDWELL": "028"},
    },
    "Houston": {
        "counties": {"HARRIS": "101", "FORT BEND": "079", "MONTGOMERY": "170", "BRAZORIA": "020", "GALVESTON": "084"},
    },
    "DFW": {
        "counties": {"DALLAS": "057", "TARRANT": "220", "COLLIN": "043", "DENTON": "061"},
    },
    "San Antonio": {
        "counties": {"BEXAR": "015", "COMAL": "046", "GUADALUPE": "094"},
    },
}
