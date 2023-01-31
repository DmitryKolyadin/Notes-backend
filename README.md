# Notes-backend

Простой бекенд сервер для заметок на Django

### Методы
/api/v0.1/auth/login/password

/api/v0.1/notes
- GET — получение
- POST — создание

/api/v0.1/note
- GET — получение
- POST — обновление
- DELETE — удаление

### Краткая документация

#### /api/v0.1/auth/login/password

POST
Получение токена по паролю:

- username
- password

Возвращает:

```json
{
  "token": "JWT token",
  "ok": true,
  "error": null
}
```

#### /api/v0.1/new_user

POST
Создание пользователя:

- first_name
- last_name
- username
- password

Возвращает:

```json
{
  "user_id": 123,
  "ok": true,
  "error": null
}
```

### ВАЖНО

Токен который был получен необходимо передавать в загаловках запроса в Authorization

#### /api/v0.1/notes

GET Получение заметок

Возвращает:

```json
{
  "notes": [
    {
      "id": 1,
      "title": "11"
    },
    ... ],
  "ok": true,
  "error": null
}
```

POST
Создание заметки:

- title
- text

Возвращает:

```json
{
  "id": 4,
  "ok": true,
  "error": null
}
```

#### /api/v0.1/note/1

GET - Получение заметки

Возвращает:

```json
{
  "note": {
    "id": 1,
    "title": "1",
    "text": "2"
  },
  "ok": true,
  "error": null
}
```

POST
Обновление заметки:

- title
- text

Возвращает:

```json
{
  "ok": true,
  "error": null
}
```

DEL - Удаление заметки

Возвращает:

```json
{
  "ok": true,
  "error": null
}
```
