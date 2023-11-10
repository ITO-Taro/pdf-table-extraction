import numpy as np
import pandas as pd
import pdfplumber
from config import TABLE_SETTINGS, COLUMNS, FIRST_COL_VALS, ROW_IGNORE

class pdfTableExtract:

    def __init__(self, files):
        self.files = files

    def is_table(self, table_object):
        vals = [i[0] for i in table_object if i[0]]
        for val in FIRST_COL_VALS:
            if not val in vals:
                return False
        return True

    def clean_1st_2nd(self, rows):
        try:
            rows[1] += rows[2]
        except:
            pass
        res = {
            'condition':" ".join([i for i in rows[0] if i]),
            'explanation':" ".join([i for i in rows[1] if i]),
        }
        return res

    def get_county_name(self, page):
        table = page.extract_tables(table_settings=TABLE_SETTINGS['county_name'])
        res = [i for i in table[0][0] if i][0]
        return res

    def clean_two_cols(self, df):
        for k, v in {'17_19_St': "*", '16_Co':"^"}.items():
            df[k] = df[k].str.replace(v, "")
        return df

    def to_float(self, df):
        for col in COLUMNS[4:11]:
            df[col] = df[col].replace("", 0).astype(float).fillna(0.0)
        return df

    def extract_data(self, doc, df, county_name=""):
        for page in doc.pages:
            data = page.extract_tables(table_settings=TABLE_SETTINGS['main'])
            if self.is_table(data[0]):
                try:
                    if not county_name:
                        county_name = self.get_county_name(page)
                    else:
                        pass
                except:
                    pass
                first2rows = page.extract_tables(table_settings=TABLE_SETTINGS['condition_description'])
                first2vals = self.clean_1st_2nd(first2rows[0][:3] if not ROW_IGNORE in first2rows[0][2][0] else first2rows[0][:2])

                for datum in data[0][3:]:
                    new_row = list(first2vals.values()) + datum
                    new_df = pd.Series(new_row, index=COLUMNS[:-2]).to_frame().T
                    df = pd.concat([df, new_df], ignore_index=True)
                    del new_df, new_row
        return df, county_name

    def extract_main(self):
        res = pd.DataFrame()
        for file in self.files:
            df = pd.DataFrame()
            # doc = pdfplumber.open(self.dir_path + file)
            doc = pdfplumber.open(file)
            df, county_name = self.extract_data(doc, df)
            df.insert(0, 'county', county_name)
            df['category'] = df['category'].replace("", np.NaN).ffill()
            df['19_Co_St_sig'] = df.apply(lambda x: 1 if "*" in x['17_19_St'] else 0, axis=1)
            df['16_Co_Co_sig'] = df.apply(lambda x: 1 if "^" in x['16_Co'] else 0, axis=1)
            df = df[df.iloc[:, 3:11].all(axis=1)]
            df = df.reset_index(drop=True)
            df = self.clean_two_cols(df)
            df = self.to_float(df)
            doc.close()
            res = pd.concat([res, df], ignore_index=True)
        return res