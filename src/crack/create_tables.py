#!/usr/bin/env python3

import sys
import os

# 프로젝트 루트 경로를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, 'src'))

try:
    from src.crack.database.connection import db
    from src.crack.model.Character import Character
    from src.crack.model.Category import Category
    from src.crack.model.Collection import Collection
    from src.crack.model.CollectionCharacter import CollectionCharacter
    
    db.create_tables()
    
except Exception as e:
    sys.exit(1) 