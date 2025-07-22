from typing import List, Optional
from ..model.Category import db, Category
import logging

class CategoryRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def save_all_category(self, categories_array: List[dict]):
        session = db.get_session() 
        
        try:
            categories = [
                Category(
                    service_id=cat.get("service_id"), 
                    name=cat.get("name"), 
                    recommend_description=cat.get("recommend_description")
                )
                for cat in categories_array
            ]
            
            session.bulk_save_objects(categories)
            session.commit()
            
            self.logger.info(f"Saved {len(categories)} categories \n")
            return len(categories)
            
        except Exception as e:
            self.logger.error(f"Error function(save_all_category) : {e} \n")
            session.rollback()
            return 0
        finally:
            session.close()
    
    def get_all_category(self):
        session = db.get_session()  
        
        try:
            categories = session.query(Category).all()
            return categories
        except Exception as e:
            self.logger.error(f"Error function(get_all_category) : {e} \n")
            return []
        finally:
            session.close()
    
