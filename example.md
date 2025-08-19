✅ main.py 코드 예시
import os
import json
from datetime import datetime

LOG_FILE = 'mission_computer_main.log'
JSON_FILE = 'mission_computer_main.json'
DANGER_FILE = 'danger_logs.txt'
DANGER_KEYWORDS = ['폭발', '누출', '고온', 'Oxygen']

def read_log_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return [line.strip() for line in lines if line.strip()]
    except FileNotFoundError:
        print(f"❌ 파일 '{filepath}'을(를) 찾을 수 없습니다.")
        return []
    except UnicodeDecodeError:
        print(f"❌ 파일 '{filepath}' 디코딩 실패. UTF-8 인코딩을 확인하세요.")
        return []

def parse_logs(log_lines):
    parsed = []
    for line in log_lines:
        try:
            timestamp, message = line.split(',', 1)
            parsed.append([timestamp.strip(), message.strip()])
        except ValueError:
            print(f"⚠️ 로그 형식 오류: {line}")
    return parsed

def sort_logs(log_list):
    try:
        return sorted(log_list, key=lambda x: datetime.fromisoformat(x[0]), reverse=True)
    except Exception as e:
        print("❌ 시간 파싱 및 정렬 중 오류:", e)
        return log_list

def convert_to_dict(sorted_logs):
    return {i: {'timestamp': log[0], 'message': log[1]} for i, log in enumerate(sorted_logs)}

def save_json(data, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ JSON 파일로 저장됨: {filepath}")
    except Exception as e:
        print("❌ JSON 저장 중 오류:", e)

def save_danger_logs(log_list):
    danger_logs = [f"{ts}, {msg}" for ts, msg in log_list if any(k in msg for k in DANGER_KEYWORDS)]
    if danger_logs:
        with open(DANGER_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(danger_logs))
        print(f"⚠️ 위험 로그 저장됨: {DANGER_FILE}")

def search_logs(json_file):
    if not os.path.exists(json_file):
        print("❌ 검색 대상 JSON 파일이 없습니다.")
        return
    keyword = input("🔍 검색할 문자열을 입력하세요: ")
    with open(json_file, 'r', encoding='utf-8') as f:
        logs = json.load(f)
    results = [entry for entry in logs.values() if keyword in entry['message']]
    print(f"🔎 '{keyword}' 포함 로그:")
    for r in results:
        print(f"{r['timestamp']} - {r['message']}")

def main():
    print("📁 로그 파일 읽기...")
    raw_logs = read_log_file(LOG_FILE)
    if not raw_logs:
        return

    print("\n📋 로그 파싱 중...")
    log_list = parse_logs(raw_logs)
    print(log_list)  # 리스트 객체 출력

    print("\n📌 시간 역순 정렬...")
    sorted_logs = sort_logs(log_list)
    for log in sorted_logs:
        print(log)

    print("\n🗂 리스트 → 딕셔너리 변환...")
    log_dict = convert_to_dict(sorted_logs)

    print("\n💾 JSON 파일 저장...")
    save_json(log_dict, JSON_FILE)

    print("\n🚨 위험 로그 필터링...")
    save_danger_logs(sorted_logs)

    print("\n🔍 검색 기능 실행...")
    search_logs(JSON_FILE)

if __name__ == "__main__":
    main()

✅ 2. log_analysis.md (사고 분석 보고서 예시)
# 🚀 사고 분석 보고서

## 📅 분석 일시
2025-08-18

## 📁 분석 대상
- 로그 파일: `mission_computer_main.log`
- 총 로그 수: N개

## 🧪 분석 결과

### ✅ 정상 로그 예시


2025-08-18T12:30:00, 시스템 점검 완료


### ⚠️ 이상 로그 예시


2025-08-18T12:35:02, 센서 온도 고온 경고 발생
2025-08-18T12:35:10, 산소(Oxygen) 누출 감지
2025-08-18T12:35:15, 엔진실 폭발 감지


## 💥 사고 추론

- **고온 경고** → **산소 누출** → **폭발 감지** 순으로 발생
- 시스템의 과열로 인해 내부 압력이 상승하고, 산소가 누출되면서 가연성 환경이 형성됨
- 이후 작은 스파크 또는 전기적 문제로 **폭발** 발생 가능성 매우 높음

## 🛠 향후 조치
- 온도 센서 정밀도 향상
- 산소 누출 차단 밸브 이중화
- 비상 정지 시스템 강화

---

보고자: 시스템 분석팀

✅ 테스트용 로그 예시 (mission_computer_main.log)
2025-08-18T12:30:00, 시스템 점검 완료
2025-08-18T12:35:02, 센서 온도 고온 경고 발생
2025-08-18T12:35:10, 산소(Oxygen) 누출 감지
2025-08-18T12:35:15, 엔진실 폭발 감지
2025-08-18T12:40:00, 복구 작업 진행 중

✅ 실행 결과 예시 (요약)
📁 로그 파일 읽기...
📋 로그 파싱 중...
[['2025-08-18T12:30:00', '시스템 점검 완료'], ...]

📌 시간 역순 정렬...
['2025-08-18T12:40:00', '복구 작업 진행 중']
...

💾 JSON 파일 저장됨: mission_computer_main.json
⚠️ 위험 로그 저장됨: danger_logs.txt
🔍 검색할 문자열을 입력하세요: Oxygen
🔎 'Oxygen' 포함 로그:
2025-08-18T12:35:10 - 산소(Oxygen) 누출 감지

-----------------------------------------------------------------
1. 로그 파일 내용을 콤마(,)를 기준으로 날짜/시간과 메시지를 분리하여 Python의 리스트(List) 객체로 전환

✅ 1. 로그 파일 내용 형식 예시
2025-08-18T12:35:10, 산소(Oxygen) 누출 감지
2025-08-18T12:35:15, 엔진실 폭발 감지


각 줄은 날짜/시간, 메시지 두 부분으로 구성되어 있고, 콤마(,)로 구분되어 있습니다.

✅ 2. 원하는 전환 결과 (리스트)

위 로그들을 파이썬 리스트 객체로 바꾸면 이렇게 됩니다:

[
    ['2025-08-18T12:35:10', '산소(Oxygen) 누출 감지'],
    ['2025-08-18T12:35:15', '엔진실 폭발 감지']
]


즉, 각 줄을 날짜/시간, 메시지로 나누고, 그것을 다시 하나의 리스트로 감싼 형태입니다.


-----------------------------------------------------------------
2. 리스트 객체를 화면에 출력

✅ 예제와 함께 설명
🔸 예를 들어, 다음과 같은 리스트가 있다고 해봅시다:
logs = [
    ['2025-08-18T12:35:10', '산소(Oxygen) 누출 감지'],
    ['2025-08-18T12:35:15', '엔진실 폭발 감지']
]

✅ 리스트 전체 출력하기
print(logs)


📤 출력 결과:

[['2025-08-18T12:35:10', '산소(Oxygen) 누출 감지'], ['2025-08-18T12:35:15', '엔진실 폭발 감지']]


이 방식은 리스트 구조 전체를 보여줍니다.

✅ 보기 좋게 줄 단위로 출력하기
for log in logs:
    print(log)


📤 출력 결과:

['2025-08-18T12:35:10', '산소(Oxygen) 누출 감지']
['2025-08-18T12:35:15', '엔진실 폭발 감지']


각 로그 항목을 한 줄씩 출력하므로 가독성이 좋아집니다.

✅ 더 보기 좋게 포맷해서 출력하기
for log in logs:
    timestamp, message = log
    print(f"[{timestamp}] {message}")


-------------------------------------------------
3. 리스트 객체를 시간 역순으로 정렬하여 출력

📤 출력:

[2025-08-18T12:35:10] 산소(Oxygen) 누출 감지
[2025-08-18T12:35:15] 엔진실 폭발 감지


상황

리스트 객체: 각 요소가 [시간, 메시지] 형태인 2차원 리스트

시간 문자열은 ISO 8601 형식 (YYYY-MM-DDTHH:MM:SS)이라고 가정

시간 기준으로 내림차순(최신 → 오래된) 정렬 후 출력

1. 예제 리스트
logs = [
    ['2025-08-18T12:30:00', '시스템 점검 완료'],
    ['2025-08-18T12:35:15', '엔진실 폭발 감지'],
    ['2025-08-18T12:35:10', '산소(Oxygen) 누출 감지'],
]

2. 정렬 및 출력 방법
from datetime import datetime

# 시간 문자열을 datetime 객체로 변환하는 함수
def parse_time(log):
    return datetime.fromisoformat(log[0])

# 시간 역순으로 정렬
sorted_logs = sorted(logs, key=parse_time, reverse=True)

# 출력
for log in sorted_logs:
    print(f"[{log[0]}] {log[1]}")

3. 출력 결과
[2025-08-18T12:35:15] 엔진실 폭발 감지
[2025-08-18T12:35:10] 산소(Oxygen) 누출 감지
[2025-08-18T12:30:00] 시스템 점검 완료

4. 요약

sorted() 함수에 key로 시간 파싱 함수 지정

reverse=True 옵션으로 내림차순(역순) 정렬

정렬된 리스트를 반복문으로 출력

---------------------------------------
4. 정렬된 리스트를 사전(Dict) 객체로 변환

1. 상황 설명

정렬된 리스트: 각 요소가 [시간, 메시지] 형태의 2차원 리스트

이 리스트를 키(key) 와 값(value) 로 구성된 파이썬 사전(dict)으로 바꾸는 작업

2. 변환 예시
정렬된 리스트 예제
sorted_logs = [
    ['2025-08-18T12:35:15', '엔진실 폭발 감지'],
    ['2025-08-18T12:35:10', '산소(Oxygen) 누출 감지'],
    ['2025-08-18T12:30:00', '시스템 점검 완료']
]

변환 코드
log_dict = {}

for i, log in enumerate(sorted_logs):
    timestamp, message = log
    log_dict[i] = {'timestamp': timestamp, 'message': message}

결과 출력
print(log_dict)


📤 출력 결과:

{
  0: {'timestamp': '2025-08-18T12:35:15', 'message': '엔진실 폭발 감지'},
  1: {'timestamp': '2025-08-18T12:35:10', 'message': '산소(Oxygen) 누출 감지'},
  2: {'timestamp': '2025-08-18T12:30:00', 'message': '시스템 점검 완료'}
}

3. 설명

enumerate() 함수로 리스트 인덱스 i와 요소 log를 함께 가져옴

각 인덱스를 딕셔너리의 키(key) 로 사용

값(value)은 다시 { 'timestamp': ..., 'message': ... } 형식의 딕셔너리로 저장

결과적으로, dict 객체는 인덱스를 키로 하는 로그 사전이 됨

4. 한 줄로 변환하기 (딕셔너리 컴프리헨션)
log_dict = {i: {'timestamp': log[0], 'message': log[1]} for i, log in enumerate(sorted_logs)}

--------------------------------------------------------------

5. 변환된 Dict 객체를 mission_computer_main.json 파일로 저장 (UTF-8, JSON 포맷)

1. 준비: json 모듈 임포트
import json

2. 예시 dict 객체
log_dict = {
    0: {'timestamp': '2025-08-18T12:35:15', 'message': '엔진실 폭발 감지'},
    1: {'timestamp': '2025-08-18T12:35:10', 'message': '산소(Oxygen) 누출 감지'},
    2: {'timestamp': '2025-08-18T12:30:00', 'message': '시스템 점검 완료'}
}

3. JSON 파일 저장 코드
with open('mission_computer_main.json', 'w', encoding='utf-8') as f:
    json.dump(log_dict, f, ensure_ascii=False, indent=4)

4. 각 인자 설명
인자	설명
'mission_computer_main.json'	저장할 파일명
'w'	쓰기 모드
encoding='utf-8'	UTF-8 인코딩 지정 (한글 등 지원)
json.dump()	dict → JSON 파일로 변환 및 저장
ensure_ascii=False	한글 등 유니코드 문자를 그대로 출력 (이모티콘 등도)
indent=4	JSON 들여쓰기 (가독성 향상)
5. 결과

mission_computer_main.json 파일이 UTF-8로 생성되고,

사람이 읽기 좋은 JSON 형식으로 저장됩니다.

한글 메시지도 깨지지 않고 잘 저장됩니다.

---------------------------------------

1. 로그 파일을 분석하여 사고 원인을 추론

✅ 1. 로그 분석의 목적

로그에 기록된 이벤트를 시간순으로 파악하고,

그 중 **비정상적인 동작(경고, 오류, 위험 징후)**를 탐지하여,

최종적으로 시스템 이상, 폭발, 고장 등 **사고의 근본 원인(Root Cause)**를 추론합니다.

✅ 2. 예시 로그 데이터
2025-08-18 14:33:12,Engine temperature high
2025-08-18 14:34:00,Pressure normal
2025-08-18 14:35:22,Oxygen level critical
2025-08-18 14:36:45,Engine overheating
2025-08-18 14:37:50,Structural integrity compromised
2025-08-18 14:38:20,Explosion detected

✅ 3. 시간순 정렬 후 흐름 해석
시간	메시지
14:33:12	Engine temperature high
14:34:00	Pressure normal
14:35:22	Oxygen level critical ❗️
14:36:45	Engine overheating ❗️
14:37:50	Structural integrity compromised ❗️
14:38:20	Explosion detected 💥
✅ 4. 추론 예시: 사고 분석
🚨 단계별 문제 발생

14:33:12: 엔진 온도 상승 → 초기 경고

14:35:22: 산소 수준이 임계치에 도달 → 생명유지 시스템 이상 가능성

14:36:45: 엔진 과열 → 과열이 지속되어 위험 상태 진입

14:37:50: 구조 손상 → 내부 압력 상승 또는 충격 발생 가능

14:38:20: 최종적으로 폭발 발생

🧠 추론된 사고 원인

"엔진의 과열로 인해 시스템 내 산소 또는 압력이 불안정해졌고, 이는 구조 손상과 폭발로 이어졌다."

즉, **초기 경고(온도, 산소)**를 적절히 처리하지 못한 것이 사고의 근본 원인으로 보입니다.

✅ 5. log_analysis.md에 들어갈 내용 예시
# 사고 분석 보고서

## 📅 로그 분석 날짜
2025-08-18

## 🧾 요약
2025년 8월 18일, 미션 컴퓨터 시스템에서 발생한 일련의 로그를 분석한 결과, **엔진 과열과 산소 수준의 불안정이 복합적으로 작용하여 구조 손상 및 폭발로 이어진 사고**로 판단됨.

## 🕒 로그 이벤트 흐름

1. **14:33:12** - Engine temperature high
2. **14:35:22** - Oxygen level critical
3. **14:36:45** - Engine overheating
4. **14:37:50** - Structural integrity compromised
5. **14:38:20** - Explosion detected

## 🔍 사고 원인 추론

- 초기 경고(온도, 산소)를 무시하거나 대응 실패
- 엔진 과열이 지속되며 구조 내부에 스트레스 증가
- 산소 또는 연료 누출로 인해 내부 폭발 발생 가능성

## 📌 결론

> 시스템 초기 경고에 대한 실시간 대응 부족이 사고의 근본 원인으로 분석됨. 향후 온도 및 산소 센서 이상에 대한 실시간 대응 체계 개선이 필요함.

✅ 요약

로그를 시간 순으로 정렬 → 의미 있는 흐름 파악

위험 키워드 (Oxygen, Overheating, Explosion 등) 확인

메시지 간 인과관계 추론이 중요 (ex: 산소 부족 → 과열 → 구조 손상 → 폭발)

Markdown 보고서는 간결하고 논리적으로 작성

---------------------------------------------------------------------------------

2. 로그를 시간의 역순으로 정렬하여 출력

1. 예제 로그 리스트
logs = [
    ['2025-08-18T12:30:00', '시스템 점검 완료'],
    ['2025-08-18T12:35:15', '엔진실 폭발 감지'],
    ['2025-08-18T12:35:10', '산소(Oxygen) 누출 감지'],
]

2. 시간 역순 정렬 및 출력 코드
from datetime import datetime

# 시간 문자열 → datetime 변환 함수
def get_time(log):
    return datetime.fromisoformat(log[0])

# 시간 역순 정렬
sorted_logs = sorted(logs, key=get_time, reverse=True)

# 출력
for timestamp, message in sorted_logs:
    print(f"[{timestamp}] {message}")

3. 출력 결과
[2025-08-18T12:35:15] 엔진실 폭발 감지
[2025-08-18T12:35:10] 산소(Oxygen) 누출 감지
[2025-08-18T12:30:00] 시스템 점검 완료

-----------------------------------------

3. 폭발, 누출, 고온, Oxygen 등의 위험 키워드가 포함된 로그만 별도로 필터링하여 파일로 저장

1. 위험 키워드 리스트
danger_keywords = ['폭발', '누출', '고온', 'Oxygen']

2. 예제 로그 리스트
logs = [
    ['2025-08-18T12:30:00', '시스템 점검 완료'],
    ['2025-08-18T12:35:15', '엔진실 폭발 감지'],
    ['2025-08-18T12:35:10', '산소(Oxygen) 누출 감지'],
    ['2025-08-18T12:40:00', '정상 운행 중']
]

3. 필터링 및 파일 저장 코드
# 위험 키워드 포함 로그 필터링
filtered_logs = [log for log in logs if any(keyword in log[1] for keyword in danger_keywords)]

# 파일에 저장 (UTF-8, 한 줄에 '시간, 메시지' 형태)
with open('danger_logs.txt', 'w', encoding='utf-8') as f:
    for timestamp, message in filtered_logs:
        f.write(f"{timestamp}, {message}\n")

4. 설명

any(keyword in log[1] for keyword in danger_keywords)
→ 메시지(log[1]) 안에 위험 키워드 중 하나라도 포함되어 있으면 True

필터된 로그를 리스트로 모아서 danger_logs.txt에 저장

각 로그는 시간, 메시지 형태로 한 줄씩 기록

---------------------------------------------------------

4. mission_computer_main.json 파일을 대상으로 사용자가 입력한 특정 문자열을 포함한 로그만 출력하는 검색 기능 구현


1. 전제: JSON 파일 구조 예시
{
  "0": {"timestamp": "2025-08-18T12:35:15", "message": "엔진실 폭발 감지"},
  "1": {"timestamp": "2025-08-18T12:35:10", "message": "산소(Oxygen) 누출 감지"},
  "2": {"timestamp": "2025-08-18T12:30:00", "message": "시스템 점검 완료"}
}

2. 검색 기능 코드 예시
import json

def search_logs(keyword):
    # JSON 파일 읽기
    with open('mission_computer_main.json', 'r', encoding='utf-8') as f:
        log_dict = json.load(f)
    
    # 검색 결과 필터링
    results = []
    for entry in log_dict.values():
        if keyword in entry['message']:
            results.append(entry)
    
    # 결과 출력
    if results:
        print(f"'{keyword}' 를 포함하는 로그:")
        for log in results:
            print(f"[{log['timestamp']}] {log['message']}")
    else:
        print(f"'{keyword}' 를 포함하는 로그가 없습니다.")

# 사용자 입력 받기
search_word = input("검색할 키워드를 입력하세요: ")
search_logs(search_word)

3. 설명

JSON 파일을 읽어서 딕셔너리로 로드

message 필드에 사용자가 입력한 키워드가 포함된 로그만 필터링

해당 로그들을 시간과 메시지 형식으로 출력

검색 결과가 없으면 안내 메시지 출력

------------------------------

1. 파이썬에서 제공하는 List 객체로 변환되어 있는지 Type명령등을 이용해서 확인한다.
1. type() 함수 사용

type() 함수는 변수의 자료형(Type) 을 반환합니다.

my_var = [1, 2, 3]

print(type(my_var))


📤 출력 결과:

<class 'list'>


이렇게 나오면 my_var는 list 객체입니다.

2. isinstance() 함수 사용 (더 권장)
if isinstance(my_var, list):
    print("my_var는 리스트입니다.")
else:
    print("my_var는 리스트가 아닙니다.")


isinstance()는 첫 번째 인자가 두 번째 인자 타입의 인스턴스인지 확인하는 함수입니다.

type()보다 상속 관계도 체크하므로 일반적으로 더 안전합니다.

3. 요약
방법	설명	예시 출력
type(var) == list	정확히 list 타입인지 확인	True / False
isinstance(var, list)	list 혹은 하위 타입까지 확인	True / False


2. json, csv format(포맺) 뜻

1. JSON (JavaScript Object Notation)

형식: 텍스트 기반의 데이터 교환 형식

구조: 키-값 쌍의 객체(object)와 배열(array)로 구성

특징:

사람이 읽고 쓰기 쉽고, 기계가 해석하고 생성하기도 쉬움

중첩 구조(객체 안에 객체나 배열 포함) 가능

주로 웹 API, 설정파일 등에 사용

JSON 예시
{
  "name": "홍길동",
  "age": 30,
  "hobbies": ["독서", "코딩", "축구"]
}

2. CSV (Comma-Separated Values)

형식: 텍스트 기반의 표 형식 데이터

구조: 각 행이 레코드, 각 열이 콤마(,)로 구분된 값

특징:

엑셀, 구글 스프레드시트 등에서 쉽게 읽고 쓸 수 있음

단순한 2차원 데이터 저장에 적합

중첩 구조 표현은 어려움

CSV 예시
name,age,hobby
홍길동,30,독서
김철수,25,코딩

------------------------------

3. dict 객체를 출력하는 이유 설명

1. 데이터 내용 확인

딕셔너리 객체가 어떤 데이터를 담고 있는지 직접 눈으로 확인하기 위해 출력합니다.

특히, 로그 데이터나 설정값 같은 키-값 쌍 구조를 쉽게 이해할 수 있습니다.

예)

log_dict = {
    0: {'timestamp': '2025-08-18T12:35:15', 'message': '엔진실 폭발 감지'}
}
print(log_dict)

2. 디버깅 (버그 찾기)

프로그램 실행 중에 딕셔너리 값이 예상대로 저장되고 있는지 확인하기 위해 출력합니다.

변수의 상태를 점검하는 중요한 방법입니다.

3. 사용자에게 데이터 보여주기

프로그램 결과를 사람이 읽기 쉽게 출력해서 사용자에게 정보를 제공할 때 사용합니다.

키와 값을 명확하게 확인할 수 있어 편리합니다.

4. 저장 전 최종 점검

JSON 파일 등 외부 저장 전에 딕셔너리 내용을 출력해 올바른지 검증할 수 있습니다.


------------------------------------------------------

4. python 딕셔너리 사용
   
   1. 딕셔너리란?

키(key)와 값(value) 쌍으로 데이터를 저장하는 자료구조

{} 중괄호로 감싸고, 키: 값 형태로 저장

키는 보통 문자열이나 숫자 사용

2. 딕셔너리 생성
# 빈 딕셔너리 만들기
my_dict = {}

# 초기값을 가진 딕셔너리 만들기
person = {
    "name": "홍길동",
    "age": 30,
    "job": "개발자"
}

3. 값 조회
print(person["name"])  # 출력: 홍길동


키를 넣어 해당 값을 가져옴

존재하지 않는 키 조회 시 KeyError 발생

4. 값 추가 및 수정
person["email"] = "hong@example.com"  # 추가
person["age"] = 31                    # 수정

5. 값 삭제
del person["job"]   # 키와 값 삭제

6. 주요 메서드
person.keys()    # 키 목록 반환
person.values()  # 값 목록 반환
person.items()   # (키, 값) 튜플 목록 반환

# 안전하게 값 가져오기 (키 없으면 None 또는 기본값)
person.get("phone")         # None 반환
person.get("phone", "없음")  # '없음' 반환

7. 반복문으로 순회
for key, value in person.items():
    print(f"{key}: {value}")

8. 전체 예제
person = {"name": "홍길동", "age": 30}

# 추가
person["job"] = "개발자"

# 출력
for k, v in person.items():
    print(f"{k}: {v}")




   