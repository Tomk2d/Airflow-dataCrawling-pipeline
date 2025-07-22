# Crack Crawling Project

Crack 플랫폼의 캐릭터, 카테고리, 컬렉션 데이터를 크롤링하고 데이터베이스에 저장하는 데이터 파이프라인 프로젝트입니다.

<br>

## 프로젝트 구조

```
wrtn-crack-crawling/
├── dags/                          # Airflow DAG 파일
│   ├── crack_crawling.py          # 메인 크롤링 DAG
│   └── src/                       # 소스 코드 (DAG에서 참조)
│
├── src/                           # 메인 애플리케이션 소스
│   ├── crack/
│   │   ├── __init__.py
│   │   ├── main.py                # 메인 실행 파일
│   │   ├── create_tables.py       # 데이터베이스 테이블 생성
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   └── connection.py      # 데이터베이스 연결 설정
│   │   ├── model/                 # 데이터 모델
│   │   │   ├── Category.py
│   │   │   ├── Character.py
│   │   │   ├── Collection.py
│   │   │   └── CollectionCharacter.py
│   │   ├── pipeline/              # 데이터 파이프라인
│   │   │   └── run_pipeline.py
│   │   ├── repository/            # 데이터 접근 계층
│   │   │   ├── category_repository.py
│   │   │   ├── character_repository.py
│   │   │   ├── collection_character_repository.py
│   │   │   └── collection_repository.py
│   │   ├── service/               # 비즈니스 로직
│   │   │   ├── character_crawler.py
│   │   │   └── navigation_crawler.py
│   │   └── utils/                 # 유틸리티
│   │       ├── data_processor.py
│   │       └── http_response.py
│   └── data/                      # 데이터 파일
│       ├── characters.json
│       └── crawl_characters.json
│
├── sql/                           # SQL 스크립트
│   └── create_tables.sql
│
├── docker-compose.yml             # Docker Compose 설정
├── Dockerfile                     # 메인 애플리케이션 Dockerfile
├── Dockerfile.airflow             # Airflow Dockerfile
├── setup_docker.sh                # Docker 환경 설정 스크립트
├── pyproject.toml                 # Python 의존성 관리
├── poetry.lock                    # Poetry 잠금 파일
└── README.md                      # 프로젝트 문서
```

<br>

## 플로우 차트
<img width="4347" height="3793" alt="image" src="https://github.com/user-attachments/assets/c1006f6d-d7ab-40a8-8886-19e4772d2caf" />

<br>
<br>

## DB 다이어그램
<img width="2232" height="1124" alt="categories" src="https://github.com/user-attachments/assets/4dc5680c-28e1-4381-857a-caa3d4550c1c" />

<br>

## 기술 스택

- **Python 3.8**
- **PostgreSQL**
- **Apache Airflow 2.7.1**
- **Docker & Docker Compose**
- **SQLAlchemy**
- **Requests**
- **Poetry**

<br>

## DB 테이블 구조

1. **categories**: 카테고리 정보
2. **characters**: 캐릭터 정보
3. **collections**: 컬렉션 정보
4. **collection_characters**: 컬렉션-캐릭터 관계

<br>

## 실행 순서

### 1. Docker 컨테이너 셋업 command

```bash
# ../wrtn-crack-crawling 위치에서

# 1. 실행 권한 부여
chmod +x setup_docker.sh

# 2. Docker 환경 설정 및 실행
./setup_docker.sh
```

<br>

### 2. Airflow UI를 통한 실행

1. 브라우저에서 http://localhost:8080 접속
2. 로그인 (wwy00@naver.com / admin0320)
3. DAG 목록에서 `crack_crawling` 선택하여 run

<br>


## Problem Solve

### 1. 비동기 병렬 처리 크롤링을 통한 성능 개선

#### 기존 크롤링 동기 처리
<img width="690" height="478" alt="image" src="https://github.com/user-attachments/assets/91afbdcd-e2e6-4159-ad33-4befe89e885c" />

- Collection 를 반복문으로 돌면서, 해당하는 캐릭터 데이터 크롤링
- Collection 에서 캐릭터를 불러오는 요청이 **페이징** 으로 구현되어 있고, **nextCursor** 를 활용하여 다음 작업을 명시하고 있었음
- 개별 Collection 내에서는 nextCursor 를 활용하여 동기적으로 요청하지만, 커서들을 병렬적으로 처리하는 방식으로 개선코드 작성

<br>

#### 개선 크롤링 비동기 병렬 처리
<img width="584" height="599" alt="image" src="https://github.com/user-attachments/assets/6b83d554-53bb-41a0-8b38-8de36554c5fb" />
<img width="853" height="297" alt="image" src="https://github.com/user-attachments/assets/32f70d97-597a-4e82-ba45-bfa5de5ba7b1" />

- Collection 레벨 병렬 처리: 모든 Collection을 동시에 처리. 개별 Collection 은 동기적으로 nextCursor 활용
- 비동기 I/O 활용: HTTP 요청 대기 시간을 효율적으로 활용
- 재시도 메커니즘: 네트워크 오류에 대한 안정성 강화

- asyncio 라이브러리 활용
- asyncio.gather()를 통한 병렬 실행
- to_thread()를 통한 동기 함수 비동기 래핑

<br>

#### 결과
<img width="703" height="27" alt="image" src="https://github.com/user-attachments/assets/59a85d26-2abe-4098-9521-7d9738eb3b8a" />
<img width="700" height="34" alt="image" src="https://github.com/user-attachments/assets/17709fad-bf7c-4a9a-9e84-edb5b5577209" />

- 단축된 시간: 704.56초 (약 11분 45초)
- 개선율: 55.49%

<br>

---

### 2. 관계 테이블을 활용한 조회 성능 개선 및 정규화

#### 기존 DB 다이어그램
<img width="728" height="250" alt="image" src="https://github.com/user-attachments/assets/45a0c223-1196-409a-ac50-170828c704e8" />


- Collections 에서 JSONB 형식으로 Characters 의 id 를 갖는 구조
- Characters 에서 JSONB 필드를 통한 복잡한 데이터 구조
- 단일 테이블에 모든 정보를 저장하는 비정규화 구조

<br>

#### 개선 DB 다이어그램
<img width="647" height="368" alt="image" src="https://github.com/user-attachments/assets/89dfed77-a661-4f11-9356-6a2f89debd29" />


- 중간 관계 테이블을 설계하여 Collections 와 Characters 의 id 키를 외래키로 가짐
- 데이터 정규화를 통한 중복 제거 및 일관성 보장
- 인덱스와 JOIN 을 통한 조회 성능 최적화

<br>

---

### 3. DB 접속 최소화와 실패 전략

#### Bulk insert
<img width="536" height="472" alt="image" src="https://github.com/user-attachments/assets/53deeca3-10c4-41bc-8e00-04270b31facb" />

- Bulk insert 를 활용하여 1번의 트랜잭션으로 대규모 데이터 삽입
- 최소한의 데이터베이스 접근
- 병목 현상 최소화

<br>

#### Individual insert 
<img width="609" height="580" alt="image" src="https://github.com/user-attachments/assets/83dd2fd5-9051-4c29-b61b-f72e50638498" />
<img width="838" height="330" alt="image" src="https://github.com/user-attachments/assets/851b682f-1334-4cb2-aaea-7c62d7b41686" />

- Bulk insert 의 경우 하나의 데이터라도 잘못되면 전부 rollback. 실패시 어떠한 데이터인지 찾기 어려움
- Bulk insert 실패시, 해당 함수를 통해 개별로 insert 진행하고, 실패한 데이터를 JSON 파일로 저장
- 디버깅 및 데이터 전처리 효과


