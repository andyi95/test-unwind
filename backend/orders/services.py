from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient import errors
import os


class GoogleSecretError(FileNotFoundError):
    pass


class GoogleSheetService:
    """Сервисный слой работы с Google таблицами.

    В рамках тестового задания не выполняется полный процесс авторизации пользователя и поиск по файлам Google Docs
    """
    def __init__(self):
        self.scopes = (
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        )
        creds = Credentials.from_authorized_user_file('secret.json', self.scopes)
        if not os.path.exists('secret.json'):
            raise GoogleSecretError('Не найден файл secret.json')
        if not creds.valid and creds.refresh_token:
            creds.refresh(Request())
        self.service = build('sheets', 'v4', credentials=creds)

    def retrieve_sheet(self, sheet_name: str =''):
        sheet = self.service.spreadsheets()
        res = sheet.values().get(
            spreadsheetId='1q285IxcuNp5oAF7zGchS-GD9ABHo59iLDxfLyt_-DJ8', range='Лист1!A:E'
        ).execute()
        return res['values']
