import datetime
import os

import pandas
# need xlsxwriter too

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    table = {
        'Column 1': ['Value 1-1', 'Value 1-2', 'Value 1-3'],
        'Column 2': ['Value 2-1', 'Value 2-2', 'Value 2-3'],
        'Column 3': ['Value 3-1', 'Value 3-2', 'Value 3-3'],
    }

    df = pandas.DataFrame(table)

    file_name = f'Report_Log_{datetime.datetime.now().strftime("%y%m%d_%H%M%S")}.xlsx'
    file_path = BASE_DIR
    os.makedirs(file_path, exist_ok=True)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pandas.ExcelWriter(os.path.join(file_path, file_name), engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, index=False)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    print('Done!')
