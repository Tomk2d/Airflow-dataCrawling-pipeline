from src.crack.repository.category_repository import CategoryRepository
from src.crack.repository.collection_repository import CollectionRepository
from src.crack.repository.character_repository import CharacterRepository
import re
import json
import os
import logging

logger = logging.getLogger(__name__)

def get_unique_characters(characters):
    unique_characters = {}
    seen_ids = set()
    
    for char in characters:
        char_id = char.get("_id")
        if char_id not in seen_ids:
            seen_ids.add(char_id)
            unique_characters[char_id] = char
    
    return list(unique_characters.values())

def remove_nul_string(value):
    if value is None:
        return None
    if isinstance(value, str):
        cleaned = re.sub(r'[\x00\u0000]', '', value)
        return cleaned.strip()
    return value

def get_characters_dao(characters):
    character_dtos = []

    for character in characters:
        profile_image = character.get("profileImage")

        profile_image_jason = None
        if profile_image:
            profile_image_jason = {
                "origin": remove_nul_string(profile_image.get("origin")),
                "w200": remove_nul_string(profile_image.get("w200")),
                "w600": remove_nul_string(profile_image.get("w600"))
            }

        category_id = None
        if character.get("categories"):
            category_id = character.get("categories")[0].get("_id")
        
        character_dto = {
            "service_id": remove_nul_string(character.get("_id")),
            "name": remove_nul_string(character.get("name")),
            "description": remove_nul_string(str(character.get("description"))),
            "profile_image": profile_image_jason,
            "initial_messages": remove_nul_string(str(character.get("initialMessages"))),
            "category_id": remove_nul_string(category_id),
        }
        character_dtos.append(character_dto)

    return character_dtos

def get_unique_categories_dao(characters):
    unique_categories = {}
    seen_ids = set()
    
    for character in characters:
        categor_array = character.get("categories")

        if not categor_array:
            continue

        category = categor_array[0]
        
        id = category.get("_id")
        name = category.get("name")
        recommendDescription = category.get("recommendDescription")

        if id not in seen_ids:
            seen_ids.add(id)
            unique_categories[id] = {
                "service_id": id,
                "name": name,
                "recommend_description": recommendDescription
            }
    
    return list(unique_categories.values())

def get_category_id_map():
    id_map = {}
    categories = CategoryRepository().get_all_category()

    for category in categories:
        id_map[category.service_id] = category.id

    return id_map

def get_collection_id_map():
    id_map = {}
    collections = CollectionRepository().get_all_collection()

    for collection in collections:
        id_map[collection.display_index] = collection.id

    return id_map

def get_character_id_map():
    id_map = {}
    characters = CharacterRepository().get_all_character()
    
    for character in characters:
        id_map[character.service_id] = character.id
    return id_map

def save_data_to_json(data, file_name, directory_path):
    
    file_path = os.path.join(directory_path, file_name)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"saved {file_name} to {file_path} \n")
    except Exception as e:
        logger.error(f"Error function(save_data_to_json) : {e} \n")
        return None

def load_data_from_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error function(load_data_from_json) : {e} \n")
        return None
    