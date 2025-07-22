from typing import List, Optional, Dict
from ..model.CollectionCharacter import db, CollectionCharacter
import logging

class CollectionCharacterRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def save_all_collection_character(
        self,
        collections_dict: Dict[str, List[dict]],
        collection_id_map: dict,
        character_id_map: dict
    ):
        session = db.get_session()

        try:
            collection_characters = []

            for service_collection_id, characters in collections_dict.items():
                collection_id = collection_id_map.get(service_collection_id)
                if collection_id is None:
                    self.logger.warning(f"Unknown collection_id: {service_collection_id}, skipping...")
                    continue

                for character in characters:
                    service_character_id = character.get("_id")
                    character_id = character_id_map.get(service_character_id)
                    if character_id is None:
                        self.logger.warning(f"Unknown character_id: {service_character_id}, skipping...")
                        continue

                    collection_characters.append(
                        CollectionCharacter(
                            collection_id=collection_id,
                            character_id=character_id
                        )
                    )

            session.bulk_save_objects(collection_characters)
            session.commit()
            self.logger.info(f"Saved {len(collection_characters)} collection-character mappings. \n")

        except Exception as e:
            session.rollback()
            self.logger.error(f"Error saving collection-character mappings: {e} \n")

        finally:
            session.close()
