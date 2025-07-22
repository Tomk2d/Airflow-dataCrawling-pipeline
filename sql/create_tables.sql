-- 프로젝트 데이터베이스 테이블 생성 스크립트

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,                -- 내부 식별자
    service_id VARCHAR UNIQUE NOT NULL,   -- 서비스에서 받은 고유 ID (_id)
    name VARCHAR NOT NULL,
    recommend_description varchar
);

CREATE TABLE characters (
    id SERIAL PRIMARY KEY,                  -- 내부 식별자
    service_id VARCHAR UNIQUE NOT NULL,     -- 서비스에서 받은 고유 ID (_id)
    name VARCHAR NOT NULL,                  -- 캐릭터 이름
    description TEXT,                       -- 설명 (nullable)
    profile_image JSONB,                    -- 프로필 이미지 URL {origin, w200, w600}
    initial_messages TEXT,                  -- 캐릭터의 첫 메세지
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE collections (
    id SERIAL PRIMARY KEY,                -- 내부 식별자
    name VARCHAR NOT NULL,                -- 컬렉션 이름
    page_id VARCHAR UNIQUE NOT NULL,      -- 서비스에서 받은 고유 pageId
    has_hero_banner_section BOOLEAN,      -- 히어로 배너 섹션 존재 여부
    display_index INTEGER                 -- 정렬 인덱스
);

CREATE TABLE collection_characters (
    collection_id INTEGER REFERENCES collections(id) ON DELETE CASCADE,
    character_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    display_order INTEGER,
    PRIMARY KEY (collection_id, character_id)
); 