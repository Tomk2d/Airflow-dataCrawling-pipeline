**Airflow DAG** 기반의 데이터 크롤링 파이프라인 입니다.

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
<img width="620" height="544" alt="image" src="https://github.com/user-attachments/assets/d5f54d4a-9837-4142-96c0-5c6a5f648568" />


<br>
<br>

## DB 다이어그램
<img width="2232" height="1124" alt="image" src="https://github.com/user-attachments/assets/03f541a2-579c-456c-a079-37e85a5050f8" />


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
<img width="1380" height="956" alt="image" src="https://github.com/user-attachments/assets/d5dd8fa8-88b5-404f-b51b-774734afac11" />


- Collection 를 반복문으로 돌면서, 해당하는 캐릭터 데이터 크롤링
- Collection 에서 캐릭터를 불러오는 요청이 **페이징** 으로 구현되어 있고, **nextCursor** 를 활용하여 다음 작업을 명시하고 있었음
- **개별 Collection 내** 에서는 nextCursor 를 활용하여 **동기적** 으로 요청하지만, **커서들을 병렬적으로 처리** 하는 방식으로 개선코드 작성

<br>

#### 개선 크롤링 비동기 병렬 처리
<img width="1168" height="1198" alt="image" src="https://github.com/user-attachments/assets/75d14e0e-62b1-4b7a-a56d-88ab7e8d8d6b" />
<img width="1706" height="594" alt="image" src="https://github.com/user-attachments/assets/2eab4034-ce5d-4f9e-81a1-b44e419cec2f" />

- **Collection 레벨** : **병렬 처리.** 모든 Collection을 **동시**에 처리
  **개별 Collection 레벨** : 은 동기적으로 nextCursor 활용
- **비동기 I/O 활용** : HTTP 요청 대기 시간을 효율적으로 활용
- **재시도 메커니즘** : 네트워크 오류에 대한 안정성 강화

- asyncio 라이브러리 활용. **gather()** 를 통한 **병렬 실행**
- **to_thread()** 를 통한 동기 함수 **비동기 래핑**

<br>

#### 결과
<img width="530" height="19" alt="image" src="https://github.com/user-attachments/assets/15f9da92-e209-4b05-bd61-ca7ef1eb59d2" />
<img width="500" height="24" alt="image" src="https://github.com/user-attachments/assets/1361d97c-6391-44fa-9e00-dcd5c764f7bd" />

- 단축된 시간: 704.56초 (약 11분 45초)
- 개선율: 55.49%

<br>

---

### 2. 관계 테이블을 활용한 조회 성능 개선 및 정규화

#### 기존 DB 다이어그램
<img width="1456" height="500" alt="image" src="https://github.com/user-attachments/assets/0e7b85e7-35c3-4304-b70c-ff7b6bf43a3b" />

- **다대다 연결** 이 필요
- Collections 에서 **JSONB** 형식으로 **Characters 의 id** 를 갖는 구조
- Characters 에서 JSONB 필드를 통한 복잡한 데이터 구조
- 단일 테이블에 모든 정보를 저장하는 비정규화 구조

<br>

#### 개선 DB 다이어그램
<img width="1294" height="736" alt="image" src="https://github.com/user-attachments/assets/122d6e01-71ce-46de-a191-d8f2b241034a" />


- **중간 관계 테이블** 을 설계하여 Collections 와 Characters 의 id 키를 **외래키** 로 가짐
- 데이터 **정규화** 를 통한 **중복 제거** 및 **일관성 보장**
- **인덱스** 와 **JOIN** 을 통한 **조회 성능 최적화**

<br>

---

### 3. DB 접속 최소화와 실패 전략

#### Bulk insert
<img width="1072" height="944" alt="image" src="https://github.com/user-attachments/assets/b626312d-7976-426b-9bd0-556e9f70fd3d" />

- **Bulk insert** 를 활용하여 **1번의 트랜잭션** 으로 **대규모 데이터 삽입**
- **최소한의 데이터베이스 접근**
- 병목 현상 최소화

<br>

#### Individual insert 
<img width="1218" height="1160" alt="image" src="https://github.com/user-attachments/assets/f9cf810f-2c3d-4ae0-ad15-832c8027aaba" />
<img width="1676" height="660" alt="image" src="https://github.com/user-attachments/assets/b66c0e76-1221-4ad2-a55e-49b957beca2e" />

- Bulk insert 의 경우 하나의 데이터라도 잘못되면 **전부 rollback.** 실패시 어떠한 데이터인지 찾기 어려움
- **Bulk insert 실패시,** 해당 함수를 통해 **개별로 insert** 진행하고, **실패한 데이터를 JSON 파일** 로 저장
- 디버깅 및 데이터 전처리 효과


