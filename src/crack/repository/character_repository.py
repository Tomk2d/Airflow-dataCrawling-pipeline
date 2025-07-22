from typing import List, Optional
import json
import os
from ..model.Character import db, Character
import logging

class CharacterRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def save_characters_individual(self, characters_array: List[dict], id_map: dict):

        success_count = 0
        error_count = 0
        failed_characters = []
        
        for i, char in enumerate(characters_array):
            session = db.get_session()
            
            try:
                character = Character(
                    service_id=char.get("service_id"),
                    name=char.get("name"),
                    description=char.get("description"),
                    profile_image=char.get("profile_image"),
                    initial_messages=char.get("initial_messages"),
                    category_id=id_map.get(char.get("category_id"))
                )
                
                session.add(character)
                session.commit()
                success_count += 1
                
            except Exception as e:
                failed_char = {
                    "index": i + 1,
                    "error": str(e),
                    "data": char
                }
                failed_characters.append(failed_char)
                
                session.rollback()
                error_count += 1
                
            finally:
                session.close()
        
        self.logger.info(f"\n=== character DB save result ===")
        self.logger.info(f"all data : {len(characters_array)}")
        self.logger.info(f"success : {success_count}")
        self.logger.info(f"fail : {error_count}")
        
        if failed_characters:
            try:
                self.save_failed_characters_to_json(failed_characters, "failed_save_characters.json", "dags/src/data")
            except Exception as e:
                self.logger.error(f"Error function(save_characters_individual-save_failed_characters_to_json) : {e}")
                return 0
        
        return success_count, error_count

    def save_all_character(self, characters_array: List[dict], id_map: dict):
        session = db.get_session() 
        
        try:
            characters = [
                Character(
                    service_id=char.get("service_id"),
                    name=char.get("name"),
                    description=char.get("description"),
                    profile_image=char.get("profile_image"),
                    initial_messages=char.get("initial_messages"),
                    category_id=id_map.get(char.get("category_id"))
                )
                for char in characters_array
            ]
            
            session.bulk_save_objects(characters)
            session.commit()
            
            self.logger.info(f"Saved {len(characters)} characters \n")
            return len(characters)  
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_all_character(self):
        session = db.get_session() 
        
        try:
            characters = session.query(Character).all()
            return characters
        except Exception as e:
            self.logger.error(f"Error function(get_all_characters) : {e} \n")
            return []
        finally:
            session.close()

    def save_failed_characters_to_json(self, failed_characters, file_name, directory_path):
        try:
            os.makedirs(directory_path, exist_ok=True)
            file_path = os.path.join(directory_path, file_name)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(failed_characters, f, ensure_ascii=False, indent=2)
            self.logger.info(f" {len(failed_characters)} failed data save to {file_path} \n")
        except Exception as e:
            self.logger.error(f"Error function(save_failed_characters_to_json) : {e} \n")