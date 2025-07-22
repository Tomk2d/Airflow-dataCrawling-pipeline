from typing import List, Optional
from ..model.Collection import db, Collection
import logging

class CollectionRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)


    def save_all_collection(self, collections_array: List[dict]):
        session = db.get_session()

        try:
            collections = [
                Collection(
                    name=collection.get("name"),
                    page_id=collection.get("pageId"),
                    has_hero_banner_section=collection.get("hasHeroBannerSection"),
                    display_index=collection.get("index")
                )
                for collection in collections_array
            ]

            session.bulk_save_objects(collections)
            session.commit()

            self.logger.info(f"Saved {len(collections)} collections \n")
            return len(collections)

        except Exception as e:
            self.logger.error(f"Error function(save_all_collection) : {e} \n")
            session.rollback()
            return 0

        finally:
            session.close()

    def get_all_collection(self):
        session = db.get_session()
        try :
            collections = session.query(Collection).all()
            return collections
        except Exception as e:
            self.logger.error(f"Error function(get_all_collection) : {e} \n")
            return []
        finally:
            session.close()
