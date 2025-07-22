import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.crack.database.connection import db
from src.crack.pipeline.run_pipeline import *
import asyncio

def main():

    try :
        init_settings(db)
    except Exception as e:
        return

    collections = fetch_collections()
    save_collections(collections)
    # characters, collections_dict = fetch_and_process_characters_sync(collections)
    characters, collections_dict = asyncio.run(fetch_and_process_characters_async(collections))
    
    save_characters_to_json(characters)

    extract_and_save_categories(characters)
    extract_and_save_characters(characters)
    save_collection_characters(collections_dict)
    return 


if __name__ == "__main__":
    db.test_connection()
    main()