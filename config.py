CITYBILL_COLSPECS = [
                        (0, 8),    # BILL ACCOUNT
                        (8, 10),   # BILL TYPE
                        (10, 19),  # REAL VALUE
                        (19, 27),  # PERSONAL VALUE
                        (27, 35),  # EXEMPT VALUE
                        (35, 43),  # DEFER VALUE
                        (43, 46),  # CARS
                        (46, 48),  # DOGS
                        (48, 66),  # PARCEL
                        (66, 68),  # TOWN
                        (68, 78),  # PENALTY
                        (78, 82),  # LENDER
                        (82, 91),  # ACRES
                        (91, 170), # FILLER
                        (170, None) # REMARKS (to end of line)
                        ]  
CITYBILL_COLUMNS = [
                    "BILL_ACCOUNT",
                    "BILL_TYPE",
                    "REAL_VALUE",
                    "PERSONAL_VALUE",
                    "EXEMPT_VALUE",
                    "DEFER_VALUE",
                    "CARS",
                    "DOGS",
                    "PARCEL",
                    "TOWN",
                    "PENALTY",
                    "LENDER", # has some bad values
                    "ACRE",
                    "FILLER",
                    "REMARKS"]  

CITYBILL_DTYPES = {
                    "BILL_ACCOUNT": "string",
                    "BILL_TYPE": "string",
                    "REAL_VALUE": "float64",
                    "PERSONAL_VALUE": "float64",
                    "EXEMPT_VALUE": "float64",
                    "DEFER_VALUE": "float64",
                    "CARS": "int64",
                    "DOGS": "int64",
                    "PARCEL": "int64",
                    "TOWN": "int64",
                    "PENALTY": "int64",
                    "LENDER": "string",
                    "ACRE": "string",
                    "FILLER": "string",
                    "REMARKS": "string"
                }


ACCOUNT_COLSPECS = [
                    (0, 8),
                    (8, 9),  
                    (9, 41),  
                    (41, 73), 
                    (73, 84), 
                    (84, 116),
                    (116, 148),
                    (148, 180),
                    (180, 212),
                    (212, 222),
                    ]  

ACCOUNT_COLUMNS = [
                    "ACCOUNT_NO",
                    "ACCOUNT_TYPE",	
                    "NAM1",
                    "NAM2",	
                    "SSNO",	
                    "BUSINESS_NAME",	
                    "MAIL_ADDRESS1",	
                    "MAIL_ADDRESS2",	
                    "CITY_STATE",	
                    "ZIP"
                    ]  
ACCOUNT_DTYPES = {
                "ACCOUNT_NO": "string",
                "ACCOUNT_TYPE": "string",
                "NAM1": "string",
                "NAM2": "string",
                "SSNO": "string",
                "BUSINESS_NAME": "string",
                "MAIL_ADDRESS1": "string",
                "MAIL_ADDRESS2": "string",
                "CITY_STATE": "string",
                "ZIP": "string"
            }


PARCEL_COLSPECS = [
                    (0, 14),
                    (14, 64),  
                    (64, None)
            ]   


PARCEL_COLUMNS = [
                "PARCEL",
                "LEGAL_DESCRIPTION",	
                "LEGAL2"
                ]    

PARCEL_DTYPES = {
    "PARCEL": "int64",
    "LEGAL_DESCRIPTION": "string",
    "LEGAL2": "string"
}   



NASH_COLSPECS = [
                 (0, 59),        # COLUMN A – JURISDICTION
                (59, 127),      # COLUMN B – PROPERTY ID
                (127, 143),     # COLUMN C – ZIP CODE
                (143, 194),     # COLUMN D – NAME 1
                (194, 245),     # COLUMN E – NAME 2
                (245, 296),     # COLUMN F – ADDRESS 1
                (296, 347),     # COLUMN G – ADDRESS 2
                (347, 398),     # COLUMN H – CITY STATE
                (398, 403),     # COLUMN I – STATUS
                (403, 457),     # COLUMN J – EXEMPT VALUE
                (457, 511),     # COLUMN K – DEF VALUE
                (511, 565),     # COLUMN L – RE VALUE
                (565, 727),     # COLUMN M – PP VALUE
                (727, 744),     # COLUMN N – LATE LIST
                (744, 780),     # COLUMN O – LENDER CODE
                (780, 837),     # COLUMN P – LL VALUE
                (837, 938),     # COLUMN Q – LEGAL DESCRIPTION
                (938, 1434),    # COLUMN R – ACRES
                (1434, 1514),   # COLUMN S – DOG COUNT
                (1514, 1568),   # COLUMN T – LAND VALUE
                (1568, 1676),   # COLUMN U – BUILDING VALUE
                (1676, 1686),   # COLUMN V – M62 AMOUNT (SPECIAL DISTRICT)
                (1686, 1716),   # COLUMN W – ALT PARCEL ID
                (1716, 1722),   # COLUMN X – LOC STREET #
                (1722, 1727),   # COLUMN Y – LOC SUFFIX
                (1727, 1752),   # COLUMN Z – LOC STREET
                (1752, 1757),   # COLUMN AA – LOC UNIT
                (1757, None)    # COLUMN AB – CUSTOMER #
         ]      

NASH_COLUMNS = [
                'JURISDICTION',
                'PROPERTY_ID',
                'ZIPC',
                'NAM1',
                'NAM2',
                'ADRS1',
                'ADRS2',
                'CITY',
                'STATUS',
                'EXEMPT_VALUE',
                'DEFER_VALUE',
                'REAL_VALUE',
                'PERSONAL_VALUE',
                'LATE_LIST',
                'LENDER_CODE',
                'LL_VALUE',
                'LEGAL_DESCRIPTION',
                'ACRE',
                'DOGS',
                'LAND_VALUE',
                'BUILDING_VALUE',
                'SPECIAL_DISTRICT',
                'ALT_PARCEL',
                'LOC_STREET#',
                'LOC_SUFFIX',
                'LOC_STREET',
                'LOC_UNIT',
                'CUSTOMER_NO'
                ]   

NASH_DTYPES = {
                'JURISDICTION': 'string',
                'PROPERTY_ID': 'int64',
                'ZIPC': 'string',
                'NAM1': 'string',
                'NAM2': 'string',
                'ADRS1': 'string',
                'ADRS2': 'string',
                'CITY': 'string',
                'STATUS': 'string',
                'EXEMPT_VALUE': 'int64',
                'DEFER_VALUE': 'int64',
                'REAL_VALUE': 'int64',
                'PERSONAL_VALUE': 'int64',
                'LATE_LIST': 'string',
                'LENDER_CODE': 'string',
                'LL_VALUE': 'int64',
                'LEGAL_DESCRIPTION': 'string',
                'ACRE': 'float64',
                'DOGS': 'int64',
                'LAND_VALUE': 'int64',
                'BUILDING_VALUE': 'int64',
                'SPECIAL_DISTRICT': 'int64',
                'ALT_PARCEL': 'string',
                'LOC_STREET#': 'int64',
                'LOC_SUFFIX': 'string',
                'LOC_STREET': 'string',
                'LOC_UNIT': 'string',
                'CUSTOMER_NO': 'string'
                }   



FINAL_COLUMN_LIST = [
                    "COUNTY",
                    "TAXYEAR",
                    "CRM_PIDN",
                    "TNSH",
                    "CTYC",
                    "LFUF",
                    "AGEX",
                    "OTHX",
                    "ZIPC",
                    "NAM1",
                    "NAM2",
                    "ADRS1",
                    "ADRS2",
                    "CITY",
                    "FLAG",
                    "CRM_EXEMPT_TOTAL",
                    "CRM_DEFER_TOTAL",
                    "CRM_REAL_TOTAL",
                    "CRM_PERSONAL_TOTAL",
                    "CRM_NET_REAL",
                    "CRM_NET_PERSONAL",
                    "CRM_PENALTY_FLAG",
                    "CRM_MOCO",
                    "EXEMPT_VALUE",
                    "DEFER_VALUE",
                    "PENALTY_VALUE",
                    "LTLS",
                    "MAPN",
                    "PARCEL_DESCR",
                    "ACRE",
                    "LNDC",
                    "NOMH",
                    "NOMV",
                    "MOCO",
                    "AGEX_VALUE",
                    "OTHX_VALUE",
                    "REAL_VALUE",
                    "HHPP_VALUE",
                    "INVE_VALUE",
                    "MACH_VALUE",
                    "FARMMINV_VALUE",
                    "MOTV_VALUE",
                    "ACCTTXACPCOD",
                    "DOGS",
                    "SWAP",
                    "CLAS",
                    "DDAT",
                    "NOTE",
                    "PLAT",
                    "RECN",
                    "DEFV_VALUE",
                    "LAND_VALUE",
                    "BLDG_VALUE",
                    "OBLD_VALUE",
                    "FIRE_DISTRICT",
                    "SPECIAL_DISTRICT",
                    "DCOD",
                    "SSNO",
                    "DEEDBOOKPAGE",
                    "ACCX",
                    "ACCT_TYPE",
                    "BILL_ACCOUNT",
                    "BILL_TYPE",
                    "EMPLOYER_NAME",
                    "LCOD",
                    "LDAT",
                    "BATH",
                    "BDRM",
                    "CNST",
                    "ERYR",
                    "FLFN",
                    "FNDT",
                    "FRPL",
                    "FUEL",
                    "HBTH",
                    "HTAC",
                    "PERI",
                    "RMYR",
                    "ROOM",
                    "SALE",
                    "SDIX",
                    "STYH",
                    "TLVA",
                    "UTIL",
                    "WLFN",
                    "XTFN",
                    "RFTY",
                    "RFMT",
                    "ZONE_CODE",
                    "IMPR",
                    "A_DTTM",
                    "A_ACTION",
                    "A_NAME",
                    "TM_TRANID"
                ]

FINAL_COLUMN_DTYPES = {
                    "COUNTY": "string",
                    "TAXYEAR": "int64",
                    "CRM_PIDN": "string",
                    "TNSH": "string",
                    "CTYC": "string",
                    "LFUF": "string",
                    "AGEX": "string",
                    "OTHX": "string",
                    "ZIPC": "string",
                    "NAM1": "string",
                    "NAM2": "string",
                    "ADRS1": "string",
                    "ADRS2": "string",
                    "CITY": "string",
                    "FLAG": "string",
                    "CRM_EXEMPT_TOTAL": "string",
                    "CRM_DEFER_TOTAL": "string",
                    "CRM_REAL_TOTAL": "string",
                    "CRM_PERSONAL_TOTAL": "string",
                    "CRM_NET_REAL": "int64",
                    "CRM_NET_PERSONAL": "int64",
                    "CRM_PENALTY_FLAG": "string",
                    "CRM_MOCO": "string",
                    "EXEMPT_VALUE": "int64",
                    "DEFER_VALUE": "int64",
                    "PENALTY_VALUE": "int64",
                    "LTLS": "string",
                    "MAPN": "string",
                    "PARCEL_DESCR": "string",
                    "ACRE": "string",
                    "LNDC": "string",
                    "NOMH": "string",
                    "NOMV": "string",
                    "MOCO": "string",
                    "AGEX_VALUE": "string",
                    "OTHX_VALUE": "string",
                    "REAL_VALUE": "int64",
                    "HHPP_VALUE": "int64",
                    "INVE_VALUE": "string",
                    "MACH_VALUE": "string",
                    "FARMMINV_VALUE": "string",
                    "MOTV_VALUE": "string",
                    "ACCTTXACPCOD": "string",
                    "DOGS": "string",
                    "SWAP": "string",
                    "CLAS": "string",
                    "DDAT": "string",
                    "NOTE": "string",
                    "PLAT": "string",
                    "RECN": "string",
                    "DEFV_VALUE": "string",
                    "LAND_VALUE": "string",
                    "BLDG_VALUE": "string",
                    "OBLD_VALUE": "string",
                    "FIRE_DISTRICT": "string",
                    "SPECIAL_DISTRICT": "string",
                    "DCOD": "string",
                    "SSNO": "string",
                    "DEEDBOOKPAGE": "string",
                    "ACCX": "string",
                    "ACCT_TYPE": "string",
                    "BILL_ACCOUNT": "string",
                    "BILL_TYPE": "string",
                    "EMPLOYER_NAME": "string",
                    "LCOD": "string",
                    "LDAT": "string",
                    "BATH": "string",
                    "BDRM": "string",
                    "CNST": "string",
                    "ERYR": "string",
                    "FLFN": "string",
                    "FNDT": "string",
                    "FRPL": "string",
                    "FUEL": "string",
                    "HBTH": "string",
                    "HTAC": "string",
                    "PERI": "string",
                    "RMYR": "string",
                    "ROOM": "string",
                    "SALE": "string",
                    "SDIX": "string",
                    "STYH": "string",
                    "TLVA": "string",
                    "UTIL": "string",
                    "WLFN": "string",
                    "XTFN": "string",
                    "RFTY": "string",
                    "RFMT": "string",
                    "ZONE_CODE": "string",
                    "IMPR": "string",
                    "A_DTTM": "datetime64[ns]",
                    "A_ACTION": "string",
                    "A_NAME": "string",
                    "TM_TRANID": "string"
                        }

EXPORTER_COLMIN_WIDTH = [
        51, 8, 31, 11, 5, 7, 7, 7, 16, 51,
        51, 51, 51, 51, 5, 54, 54, 54, 54, 54,
        54, 17, 11, 13, 12, 21, 5, 31, 101, 11,
        5, 12, 12, 11, 54, 54, 54, 54, 54, 54,
        54, 54, 13, 7, 5, 5, 7, 31, 7, 7,
        11, 54, 54, 54, 14, 17, 5, 12, 13, 11,
        11, 13, 51, 51, 5, 7, 54, 54, 5, 5,
        7, 7, 54, 7, 54, 7, 6, 5, 54, 54,
        5, 54, 8, 7, 7, 7, 5, 5, 10, 5,
        55, 51, 51, 9
    ]


CITY_STATE_REPLACEMENTS = {
    "20602, NC": "WALDORF, MD",
    "ATLANTA, NC": "ATLANTA, GA",
    "BATTLEBORO, N, C": "BATTLEBORO, NC",
    "BATTLEBORO NC": "BATTLEBORO, NC",
    "BATTLEBORO NCNC": "BATTLEBORO, NC",
    "BAY HARBOR ISLAND, FL": "BAY HARBOR ISLANDS, FL",
    "BROOKLIN, NY": "BROOKLYN, NY",
    "BLYTHE WOOD, SC": " BLYTHEWOOD, SC",
    "CAMBIA HEIGHTS, NY": "CAMBRIA HEIGHTS, NY",
    "CAMBIA HEIGHTS, NY ": "CAMBRIA HEIGHTS, NY",
    "CAMBIA, HEIGHTS, NY": "CAMBRIA HEIGHTS, NY",
    "CAPITAL HEIGHTS, MD": "CAPITOL HEIGHTS, MD",
    "CAPITOL HEIGHTS, MD": "CAPITOL HEIGHTS, MD",
    "CHAROTTEVILLE, VA": "CHARLOTTESVILLE, VA",
    "CIERRA VISTA, AZ": "SIERRA VISTA, AZ",
    "DURHAM , NC": "DURHAM, NC",
    "ELMSFORD, NEW, YORK": "ELMSFORD, NY",
    "FARROCKAWAY, NY": "FAR ROCKAWAY, NY",
    "PHILADELPHIA , PA": "PHILADELPHIA, PA",
    "MECHANIVILLE, MD":"MECHANICSVILLE, MD",
    "ROANOKE RAPID, NC": "ROANOKE RAPIDS, NC",
    "ROCKY MOUNT NC": "ROCKY MOUNT, NC",
    "ROCKY MOUNT NCNC": "ROCKY MOUNT, NC",
    "ROCKY MOUNT,": "ROCKY MOUNT, NC",
    "ROCKY MOUNT, N, C": "ROCKY MOUNT, NC",
    "ROCKY, MOUNT,": "ROCKY MOUNT, NC",
    "ROCKY, MOUNT, NC": "ROCKY MOUNT, NC",
    "ROCKY, MOUNT,NC": "ROCKY MOUNT, NC",
    "ROCKYMOUNTNC": "ROCKY MOUNT, NC",
    "ROCKY MOUNTNC": "ROCKY MOUNT, NC",
    "ROCLY MOUNT, NC": "ROCKY MOUNT, NC",
    "SILVERSPRINGS, MD": "SILVER SPRINGS, MD",
    "STATON ISLAND, NY": "STATEN ISLAND, NY",
    "STUART, VA": "STUART DRAFT, VA",
    "STUARTS DRAFT, VA": "STUART DRAFT, VA",
    "SCOTTSDALE, AR": "SCOTTSDALE, AZ",
    "TARBORO NC": "TARBORO, NC",
    "UPPR MARLBORO, MD": "UPPER MARLBORO, MD",
    "VIRGINIA BCH, VA": "VIRGINIA BEACH, VA",
    "WINSTON SALEM, NC": "Winston-Salem, NC",
    "WINSTON-SALEM, NC": "Winston-Salem, NC",
    "ZEBULON NC": "ZEBULON, NC",
    "ZEBULON, N.C. 27597": "ZEBULON, NC",
    "PALMBALE, CA": "PALMDALE, CA",
    "BURMINGHAM, AL": "BIRMINGHAM, AL",
    "ABLION, NJ": "ALBION, NJ",
    "ROCLY MOUNT, NC": "ROCKY MOUNT, NC",
    "ATLANTA, NC": "ATLANTA, GA",
    "BLYTHE WOOD, SC": "BLYTHEWOOD, SC",
    "SCOTTSDALE, AR": "SCOTTSDALE, AZ",
    "MECHANIVILLE, MD": "MECHANICSVILLE, MD",
    "NEW PORT NEWS, VA": "NEWPORT NEWS, VA",
    "COCKEYSVILLE HUNT VA, MD": "COCKEYSVILLE, MD"
    }