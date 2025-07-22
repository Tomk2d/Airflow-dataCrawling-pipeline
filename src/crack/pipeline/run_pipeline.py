from src.crack.service.navigation_crawler import get_collections
from src.crack.service.character_crawler import get_characters
from src.crack.utils.data_processor import *
from src.crack.repository.character_repository import CharacterRepository
from src.crack.repository.category_repository import CategoryRepository
from src.crack.repository.collection_repository import CollectionRepository
from src.crack.repository.collection_character_repository import CollectionCharacterRepository
import logging
import asyncio

# Python 3.8 호환 to_thread 함수
if hasattr(asyncio, "to_thread"):
    to_thread = asyncio.to_thread
else:
    async def to_thread(func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)

logger = logging.getLogger(__name__)

def init_settings(db):
    try :
        db.create_tables()
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
        logger.info("init settings success : create tables, set logging level \n")
    except Exception as e:
        logger.error(f"failed to init settings: {e} \n")
        raise e
    return

def fetch_collections():
    collections = get_collections()
    return collections

def fetch_and_process_characters_sync(collections):
    logger.info("characters crawling start")

    if collections is None:
        logger.error("\n collections is None")
        return [], {}
    
    all_characters = []
    collections_dict = {}

    for i in range(4 , len(collections)-1):
        collection = collections[i]
        pageId = collection.get("pageId")

        if pageId is None:
            logger.error(f"\n collection pageId is None")
            continue

        characters = []
        
        while True:
            characters = get_characters(pageId)

            if characters is not None:
                collections_dict[collection.get("index")] = characters
                logger.info(f"Page ID: {pageId} success to crawl {len(characters)} characters")
                break
            else:
                logger.error(f"\n Page ID: {pageId} failed to crawl characters. retry...")
                continue

        all_characters.extend(characters)
    
    save_data_to_json(all_characters, "crawl_characters.json", "dags/src/data")

    unique_characters = get_unique_characters(all_characters)

    return unique_characters, collections_dict


def extract_and_save_categories(characters):
    categories_dao = get_unique_categories_dao(characters)

    category_repository = CategoryRepository()
    category_repository.save_all_category(categories_dao)

    return


def extract_and_save_characters(characters):
    characters_dao = get_characters_dao(characters)
    id_map = get_category_id_map()

    character_repository = CharacterRepository()
    try:
        character_repository.save_all_character(characters_dao, id_map)
    except Exception as e:
        logger.warning(f"Bulk save failed. Switching to individual saves. : {e} \n")
        character_repository.save_characters_individual(characters_dao, id_map)
    return


def save_collections(collections):
    collection_repository = CollectionRepository()
    collection_repository.save_all_collection(collections)

    return


def save_collection_characters(collections_dict):
    collection_id_map = get_collection_id_map()
    character_id_map = get_character_id_map()
    collection_character_repository = CollectionCharacterRepository()
    collection_character_repository.save_all_collection_character(collections_dict, collection_id_map, character_id_map)

    return


def save_characters_to_json(characters): 
    try:
        characters = save_data_to_json(characters, "characters.json", "dags/src/data")
    except Exception as e:
        logger.error(f"failed to load characters from json: {e} \n")
        return 
    
    return 


def load_characters_from_json():
    characters = load_data_from_json("dags/src/data/characters.json")

    return characters


async def get_characters_with_retry(pageId, max_retries=3):
    for attempt in range(max_retries):
        try:
            characters = await to_thread(get_characters, pageId)
            if characters is not None:
                return characters
            else:
                logger.error(f"Page ID: {pageId} failed to crawl characters (attempt {attempt + 1}/{max_retries})")
        except Exception as e:
            logger.error(f"Page ID: {pageId} error (attempt {attempt + 1}/{max_retries}): {e}")
        
        if attempt < max_retries - 1:
            await asyncio.sleep(1)
    
    logger.error(f"Page ID: {pageId} failed after {max_retries} attempts")
    return None


async def fetch_and_process_characters_async(collections):
    logger.info("characters crawling start")

    if collections is None:
        logger.error("collections is None")
        return [], {}
    
    all_characters = []
    collections_dict = {}
    
    tasks = []
    for i in range(4, len(collections)-1):
        collection = collections[i]
        pageId = collection.get("pageId")
        if pageId is None:
            logger.error(f"collection pageId is None")
            continue
        
        task = get_characters_with_retry(pageId)
        tasks.append((collection, task))
    
    results = await asyncio.gather(*[task for _, task in tasks])
    
    for (collection, _), characters in zip(tasks, results):
        if characters:
            collections_dict[collection.get("index")] = characters
            all_characters.extend(characters)
    
    save_data_to_json(all_characters, "crawl_characters.json", "dags/src/data")

    unique_characters = get_unique_characters(all_characters)
    
    return unique_characters, collections_dict