#!/bin/bash

# 1. 기존 컨테이너 중지
echo ""
echo "📦 1단계: 기존 컨테이너 중지 중..."
docker-compose down

# 2. Docker 이미지들 빌드
echo ""
echo "🔨 2단계: Docker 이미지 빌드 : "
echo "📦 Python 애플리케이션 이미지 빌드 중..."
docker-compose build app
echo "📦 Airflow 이미지 빌드 중..."
docker-compose build airflow-webserver airflow-scheduler


# 3. PostgreSQL만 시작
echo ""
echo "🗄️ 3단계: Airflow PostgreSQL 시작 중..."
docker-compose up -d airflow-postgres


# 4. Airflow 데이터베이스 초기화
echo ""
echo "🔧 4단계: Airflow 데이터베이스 초기화 중..."
docker-compose run --rm airflow-webserver airflow db init


# 5. Airflow 관리자 사용자 생성
echo ""
echo "👤 5단계: Airflow 관리자 사용자 생성 중..."
docker-compose run --rm airflow-webserver airflow users create \
    --username admin \
    --firstname WRTN \
    --lastname User \
    --role Admin \
    --email wwy00@naver.com \
    --password admin0320


# 6. 데이터베이스 생성
echo ""
echo "🗄️ 6단계: 애플리케이션 PostgreSQL 시작 중..."
docker-compose up -d postgres


# 7. 테이블 생성 쿼리 실행
echo ""
echo "📋 7단계: 데이터베이스 테이블 생성 중..."
docker-compose exec -T postgres psql -U crack_user -d crack_db < sql/create_tables.sql


# 8. 테이블 생성 확인   
echo ""
echo "🔍 8단계: 테이블 생성 확인 중..."
docker-compose exec -T postgres psql -U crack_user -d crack_db -c "\dt"


# 9. Python 애플리케이션 컨테이너 시작
echo ""
echo "🐍 9단계: Python 애플리케이션 시작 중..."
docker-compose up -d app

# 10. 모든 Airflow 서비스 시작
echo ""
echo "🌪️ 10단계: Airflow 서비스 시작 중..."
docker-compose up -d


# 11. 서비스 상태 확인
echo ""
echo "📊 11단계: 서비스 상태 확인 중..."
docker-compose ps




echo ""
echo "✅ Airflow 설정이 완료되었습니다!"
echo "🌐 Airflow UI: http://localhost:8080"
echo "👤 로그인 정보: wwy00@naver.com / admin0320"
