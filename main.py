import mintapi
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import username, password, sheet_name, subsheet_name, ids, id_dict, vendor_dict, category_dict, test_transactions
import datetime as dt


def import_recent_transactions(testing=True):
    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open(sheet_name)
    personal_expenses_2022 = sheet.worksheet(subsheet_name)

    if not testing:
        mint = mintapi.Mint(username, password)

        most_recent_date = personal_expenses_2022.col_values(5)[-1]
        start_date = week_ago(most_recent_date)
        transactions = mint.get_transaction_data(start_date=start_date)
    else:
        transactions = test_transactions

    df = pd.DataFrame(data=transactions)

    if df.shape[0] > 100:
        print("Invalid start date")
        return

    id_column = personal_expenses_2022.col_values(1)
    existing_ids = [i for i in id_column if i]
    df = df[~df['id'].isin(existing_ids)]

    df = df[df.accountId.isin(ids)]
    df = df[df.amount < 0.00]

    df = df.replace(id_dict)
    df = df.replace(vendor_dict)
    df['amount'] = df['amount'].mul(-1)

    df['Item'] = ''
    df['Category'] = df['description'].map(category_dict)
    df.fillna('', inplace=True)

    df = df.reindex(columns=['id', 'Item', 'description', 'amount', 'date', 'Category', 'accountId'])

    df = df[::-1]

    num_rows = len(personal_expenses_2022.col_values(5))
    personal_expenses_2022.update("A" + str(num_rows + 1) + ":H", df.values.tolist(),
                                  value_input_option='USER_ENTERED')

    if not testing:
        mint.close()


def week_ago(date):
    converted_date = dt.datetime.strptime(date, '%m/%d/%Y')
    one_week_prior = converted_date - dt.timedelta(days=7)
    week_ago_str = one_week_prior.strftime('%m/%d/%y')

    return week_ago_str


if __name__ == '__main__':
    import_recent_transactions(testing=False)
