import os.path

from api import PetFriends
from settings import valid_password, valid_email, faled_password, faled_user

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet_with_valid_data(name="pinguen", animal_type="vampir",
                                     age="988", pet_photo="image/horror023.png"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pets(auth_key, "Super-hero", "human", "20", "images/image_123.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Momo', animal_type='Cat', age=7):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_create_pet_simple(name='Bony', animal_type='Fish', age="3"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_photo_of_pets(pet_photo="image/images_123.jpg"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.add_new_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 200


def test_get_api_key_not_correct_user(email=faled_user, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_api_key_not_correct_password(email=valid_email, password=faled_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_not_correct_filter(filter="2222"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500


def test_add_new_pet_with_not_correct_age(name="pinguen", animal_type="vampir",
                                          age=1, pet_photo="image/horror023.png"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)
    except:
        print(" Ошибка ввода данных")

def test_add_new_pet_with_not_correct_name(name={"pinguen": "momo"}, animal_type="vampir",
                                          age=1, pet_photo="image/horror023.png"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)
    except:
        print(" Ошибка ввода данных")

def test_add_new_pet_with_not_correct_animal_type(name="pinguen", animal_type=["vampir"],
                                          age=1, pet_photo="image/horror023.png"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)
    except:
        print(" Ошибка ввода данных")

def test_add_new_pet_with_not_correct_pet_photo(name="pinguen", animal_type="vampir",
                                                age="1", pet_photo="orror023.png"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)
    except:
        print(" Ошибка ввода данных")


def test_add_photo_of_pets_not_correct_id(pet_photo="image/images_123.jpg"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = "ewqsd123"
    status, _ = pf.add_new_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 500

