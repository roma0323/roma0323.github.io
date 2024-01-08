from gsheet import get_sheet
from datetime import datetime


def netflix_data():
    SAMPLE_SPREADSHEET_ID = "1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY"
    SAMPLE_RANGE_NAME = "netflix_titles"
    sheet_data = get_sheet(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
    print(f"Spreadsheet: \n{sheet_data['date_added'].head()}")

    converted_dates = []
    for date in sheet_data['date_added']:
        if date:  # 检查是否为空字符串
            try:
                dt = datetime.strptime(date, '%d-%b-%y')
                new_format = dt.strftime('%Y-%m-%d')
                converted_dates.append(new_format)
            except ValueError:
                try:
                    # If the original format fails, try parsing with a different format
                    dt = datetime.strptime(date, '%B %d, %Y')
                    new_format = dt.strftime('%Y-%m-%d')
                    converted_dates.append(new_format)
                except ValueError:
                    print(f"Ignoring invalid date format: {date}")
                    continue
        else:
            print("Encountered an empty date string.")

    print(f"Spreadsheet_date: \n{converted_dates[:5]}")