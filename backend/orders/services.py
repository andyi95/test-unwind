import datetime
from typing import List

import requests
import xmltodict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class CommonOrderService:
    """Сервисный слой работы с заказами.

    В рамках тестового задания не выполняется полный процесс авторизации пользователя и поиск по файлам Google Docs
    """
    def __init__(self):
        self.scopes = (
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        )
        creds = Credentials.from_authorized_user_file('orders/secret.json', self.scopes)
        if not creds.valid and creds.refresh_token:
            creds.refresh(Request())
        self.service = build('sheets', 'v4', credentials=creds)

    def retrieve_sheet(self, sheet_name: str ='1q285IxcuNp5oAF7zGchS-GD9ABHo59iLDxfLyt_-DJ8') -> List[list]:
        sheet = self.service.spreadsheets()
        res = sheet.values().get(
            spreadsheetId=sheet_name, range='Лист1!A:E'
        ).execute()
        return res['values']

    def get_rate(self, date: datetime.date = None, code: str = 'USD') -> float:
        url = 'https://cbr.ru/scripts/XML_daily.asp'
        params = {'date_req': date.strftime('%d/%m/%Y')} if date else None
        response = requests.get(url, params=params)
        data = xmltodict.parse(response.content)
        valutes = data['ValCurs']['Valute']
        for valute in valutes:
            if valute['CharCode'] == code:
                return float(valute['Value'].replace(',', '.'))
        return 0.0


if __name__ == '__main__':
    serv = CommonOrderService()
    serv.get_rate()
    t = serv.retrieve_sheet()
