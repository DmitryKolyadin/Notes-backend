import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate

# Импортируем модель пользователя
from django.contrib.auth.models import User

# Импортируем модель токена
from api.models import JWT_token, Note

# Импортируем секретный токен
from config.settings import SECRET_KEY

# Импортируем библиотеку для работы с jwt
import jwt

def error_response(error='', status=400):
	response = {
		'ok': False,
		'error': error,
	}
	return HttpResponse(json.dumps(response), content_type='application/json', status=status)


# Авторизация по паролю и получение токена jwt
def login_password(request):
	if request.method == 'POST':
		
		form = request.POST

		if 'username' not in form or 'password' not in form:
			return error_response('Username or password filed not valid', status=400)

		username = form['username']
		password = form['password']

		user = authenticate(username=username, password=password)

		if user is None:
			return error_response('Username or password not valid', status=401)

		# Создаем токен

		payload = {
			'iss': request.build_absolute_uri(),
			'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
			'iat': datetime.datetime.utcnow(),
		}

		payload['user_id'] = user.id
		payload['user_first_name'] = user.first_name
		payload['user_last_name'] = user.last_name

		token_str = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
		print(token_str)

		# Сохраняем токен в базе данных

		# token = JWT_token(token=token_str, user=user)
		# token.save()

		response = {
			'token': token_str,
			'ok': True,
			'error': None,
		}

		return HttpResponse(json.dumps(response), content_type='application/json')

	else:
		return error_response('Method not allowed', status=405)

# Декоратор для проверки токена
def check_token(func):
	def wrapper(request, *args, **kwargs):
		
		# Получаем токен из заголовка запроса
		
		print(request.META)

		token_str = request.META.get('HTTP_AUTHORIZATION', None)

		if token_str is None:
			return error_response('Token not found', status=401)

		# Проверяем токен
		try:
			payload = jwt.decode(token_str, SECRET_KEY, algorithms=['HS256'])
		except:
			return error_response('Token is not valid', status=401)

		# Проверяем время жизни токена
		if datetime.datetime.utcnow() > datetime.datetime.utcfromtimestamp(payload['exp']):
			return HttpResponse('error - token is expired')

		# Получаем пользователя из токена
		user_id = payload['user_id']
		user = User.objects.get(id=user_id)

		# Проверяем, что пользователь существует
		if user is None:
			return HttpResponse('error - user not found')

		# Передаем в функцию пользователя
		request.user = user

		return func(request, *args, **kwargs)
	return wrapper


# Получение списка заметок и создание новой заметки
@check_token
def notes(request):
	if request.method == 'GET':
		# Получаем список заметок
		notes = Note.objects.filter(user=request.user)

		# Формируем ответ
		response = {
			'notes': [],
			'ok': True,
			'error': None,
		}

		for note in notes:
			response['notes'].append({
				'id': note.id,
				'title': note.title,
				# 'text': note.text,
			})

		return HttpResponse(json.dumps(response), content_type='application/json')

	elif request.method == 'POST':
		
		form = request.POST

		if 'title' not in form or 'text' not in form:
			return error_response('Title or text filed not valid', status=400)

		title = form['title']
		text = form['text']

		# Создаем заметку
		note = Note(
			title=title,
			text=text,
			user=request.user,
		)
		note.save()

		response = {
			'id': note.id,
			'ok': True,
			'error': None,
		}

		return HttpResponse(json.dumps(response), content_type='application/json')

	else:
		return error_response('Method not allowed', status=405)

# Получение, редактирование и удаление заметки
@check_token
def note(request, note_id):
	if request.method == 'GET':
		# Получаем заметку
		note = Note.objects.filter(id=note_id, user=request.user).first()

		# Проверяем, что заметка существует
		if note is None:
			return error_response('Note not found', status=404)

		# Формируем ответ
		response = {
			'note': {
				'id': note.id,
				'title': note.title,
				'text': note.text,
			},
			'ok': True,
			'error': None,
		}

		return HttpResponse(json.dumps(response), content_type='application/json')

	elif request.method == 'POST':
		# Получаем заметку
		note = Note.objects.filter(id=note_id, user=request.user).first()

		# Проверяем, что заметка существует
		if note is None:
			return error_response('Note not found', status=404)

		form = request.POST

		if 'title' not in form or 'text' not in form:
			return error_response('Title or text filed not valid', status=400)

		title = form['title']
		text = form['text']

		# Редактируем заметку
		note.title = title
		note.text = text
		note.save()

		response = {
			'ok': True,
			'error': None,
		}

		return HttpResponse(json.dumps(response), content_type='application/json')

	elif request.method == 'DELETE':
		# Получаем заметку
		note = Note.objects.filter(id=note_id, user=request.user).first()

		# Проверяем, что заметка существует
		if note is None:
			return error_response('Note not found', status=404)

		# Удаляем заметку
		note.delete()

		response = {
			'ok': True,
			'error': None,
		}

		return HttpResponse(json.dumps(response), content_type='application/json')