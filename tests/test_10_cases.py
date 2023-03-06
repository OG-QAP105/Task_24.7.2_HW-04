from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password

pf = PetFriends()


def warning(mess):
    return print("\n"+79*"-" + f"\n>>> {mess}\n" + 79*"-")


# ТЕСТ 1
# Ввод неверного эл.адреса и пароля:
def test_get_api_key_with_invalid_email_invalid_password(email=invalid_email, password=invalid_password):
    """Тест на ввод неверного эл.адреса и пароля"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    warning("Неверный адрес эл.почты и пароль!")


# ТЕСТ 2
# Ввод верного эл.адреса и неверного пароля:
def test_get_api_key_with_valid_email_invalid_password(email=valid_email, password=invalid_password):
    """Тест на ввод верного эл.адреса и неверного пароля"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    warning("Неверный пароль!")


# ТЕСТ 3
# Ввод неверного эл.адреса и верного пароля:
def test_get_api_key_with_invalid_email_valid_password(email=invalid_email, password=valid_password):
    """Тест на ввод неверного эл.адреса и верного пароля"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    warning("Неверный адрес эл.почты!")


# ТЕСТ 4
# Ввод нового питомца без фотографии:
def test_create_pet_simple(name='Барсик', animal_type='котэ', age='5'):
    """Тест на ввод нового питомца без фотографии"""
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца без фотографии
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# ТЕСТ 5
# Добавление фотографии питомца:
def test_add_pet_photo(pet_photo='images/cat3.jpg'):
    """Тест на добавление фотографии питомца"""
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем добавить его фотографию
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем что статус ответа = 200
        assert status == 200
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception(warning("Своих питомцев нет в наличии!"))


# ТЕСТ 6
# Список своих питомцев:
def test_get_my_pets(filter='my_pets'):
    """Тест наличия своих питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    if len(result['pets']) > 0:
        assert status == 200
    else:
        raise Exception(warning("Своих питомцев нет в наличии!"))


# ТЕСТ 7
#  Удаление питомца:
def test_delete_pet():
    """Тест на возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    assert status == 200
    assert pet_id not in my_pets.values()


# ТЕСТ 8
# Удаление питомца с неверным ключом авторизации:
def test_delete_pet_with_invalid_auth_key():
    """Тест на невозможность удалить питомца при неверном ключе авторизации"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    invalid_auth_key = {'key': '1234567890abcdefghijklmnopqrs'}
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(invalid_auth_key, pet_id)
    assert status == 403
    warning("Неверный ключ авторизации!")


# ТЕСТ 9
# Обновить информацию о питомце с верным ключом авторизации:
def test_update_pet_info_valid_auth_key(name='Барсег', animal_type='Борзый котэ', age=5):
    """Тест на обновление информации о питомце при верном ключе авторизации"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 200
    assert result['name'] == name


# ТЕСТ 10
# Обновить информацию о питомце с неверным ключом авторизации:
def test_update_pet_info_invalid_auth_key(name='Мурзик', animal_type='котейка', age=11):
    """Тест на обновление информации о питомце при неверном ключе авторизации"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    invalid_auth_key = {'key': '1234567890abcdefghijklmnopqrs'}
    status, result = pf.update_pet_info(invalid_auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 403
    warning("Неверный ключ авторизации!")











