import psycopg2

# TimescaleDB 연결 정보
conn = psycopg2.connect(
    dbname="scc-db",
    user="scc",
    password="scc123",
    host="service-timescaledb",
    port="5432"
)

# 커서 생성 및 쿼리 실행
cur = conn.cursor()
cur.execute("SELECT now();")  # 현재 시간 조회

# 결과 출력
print(cur.fetchone())

# 연결 종료
cur.close()
conn.close()
