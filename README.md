Tested on 
- Windows
- MS SQL Server 2019 and 2022
- turbodbc.__version__ '4.5.5'
- drivers: 'ODBC Driver 17 for SQL Server' and 'SQL Server Native Client 11.0'

Error returned when option fetch_wchar_as_char = True:
"""
turbodbc.exceptions.DatabaseError: ODBC error
state: HY104
native error code: 0
"""

When Error returned when option fetch_wchar_as_char = False:
Some unicode characters are not imported into SQL server correctly, e.g. Ã»Ã©H instead of 'ûéH'

