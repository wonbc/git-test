import pyodbc
import oracledb
from dataclasses import dataclass
from typing import List

# MSSQL 연결 설정

# 데이터 구조체 정의
@dataclass
class Order:
    orderseq: int
    orderdate: str
    orderno: str
    pono: str
    regtime: str
    deliverydate: str

# MSSQL 연결 설정
def get_mssql_connection():
    conn = pyodbc.connect(
         "DRIVER={SQL Server Native Client 11.0};"
         "SERVER=192.168.101.13,14233;"
         "DATABASE=LENS;"
         "UID=syt;"
         "PWD=syt3030!@;"
     )
    return conn

# Oracle 연결 설정
def get_oracle_connection():
    """
    Oracle 데이터베이스 연결
    필요한 정보:
    - host: Oracle 서버 주소
    - port: Oracle 포트 (기본값: 1521)
    - sid: Oracle SID (또는 service_name)
    - user: Oracle 사용자명
    - password: Oracle 비밀번호
    """
    try:
        # 방법 1: TNS 이름 사용
        # conn = oracledb.connect(user='username', password='password', dsn='TNS_NAME')
        
        # 방법 2: 직접 연결 정보 입력
        conn = oracledb.connect(
            user='your_username',           # Oracle 사용자명으로 변경
            password='your_password',       # Oracle 비밀번호로 변경
            host='your_host',              # Oracle 서버 주소로 변경
            port=1521,                      # Oracle 포트 (기본값: 1521)
            sid='your_sid'                  # Oracle SID로 변경
        )
        print("Oracle 연결 성공")
        return conn
    except oracledb.DatabaseError as e:
        print(f"Oracle 연결 실패: {e}")
        return None

# 기존 get_db_connection은 MSSQL 연결을 위해 유지
def get_db_connection():
    return get_mssql_connection()

# 데이터 조회 함수
def fetch_orders():
    query = """
    SELECT 
        orderseq, OrderDate, -- 수취일자
        OrderNo, PoNo,
        RegTime, DeliveryDate
    FROM [dbo].[chemi_TLensOrder] a
    WHERE orderdate BETWEEN '2026.08.01' AND '2026.08.25'
    AND clientno IN (
        SELECT CommonCode
        FROM [dbo].[chemi_TLensCustCommon]
        WHERE CommonKind = 'OG' AND ISNULL(SYTCustNo, '') <> ''
    )
    ORDER BY a.orderdate
    """

    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    
    # 결과를 구조체에 담기
    orders: List[Order] = []
    for row in cursor.fetchall():
        orders.append(Order(
            orderseq=row.orderseq,
            orderdate=row.OrderDate,
            orderno=row.OrderNo,
            pono=row.PoNo,
            regtime=row.RegTime,
            deliverydate=row.DeliveryDate
        ))
    
    conn.close()
    return orders

# 결과 출력
if __name__ == "__main__":
    orders = fetch_orders()
    for order in orders:
        print(order)