import json
import os
from datetime import datetime

# datetime Python 표준 라이브러리(Standard Library)에 포함된 모듈(module)입니다.
# datetime 안에는 datetime, date, time, timedelta 클래스가 포함되었습니다.

def read_log_file(filename):
    
    # 로그 파일을 읽어서 전체 내용을 반환하는 함수
    
    # Args:
    #     filename (str): 읽을 로그 파일명
        
    # Returns:
    #     str: 파일 내용 또는 None (오류 시)
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f'=== {filename} 파일 전체 내용 ===')
            print(content)
            print('=' * 50)
            return content
    except FileNotFoundError:
        print(f'오류: {filename} 파일을 찾을 수 없습니다.')
        return None
    except UnicodeDecodeError:
        print(f'오류: {filename} 파일 인코딩 문제가 발생했습니다.')
        return None
    except Exception as e:
        print(f'오류: 파일 읽기 중 예상치 못한 오류가 발생했습니다. {e}')
        return None

# print('=' * 50) '=' 문자 하나를 50번 반복해서 출력하라는 뜻입니다.
# open 객체 함수는 주로 파일을 열기 위해 사용되는 파이썬 내장 함수입니다.
# FileNotFoundError는 파이썬에서 파일 또는 디렉토리를 찾을 수 없을 때 발생하는 에러(예외 클래스)입니다.
# UnicodeDecodeError는 파이썬에서 텍스트(문자열)를 디코딩할 때 문제가 생기면 발생하는 에러입니다.


def parse_log_to_list(content):
    
    # 로그 내용을 파싱하여 리스트로 변환하는 함수
    
    # Args:
    #     content (str): 로그 파일 내용
        
    # Returns:
    #     list: 파싱된 로그 데이터 리스트
   
    log_list = []
    
    if not content:
        return log_list
    
    lines = content.strip().split('\n')
    
    # 헤더 라인 건너뛰기
    for line in lines[1:]:
        if line.strip():
            parts = line.split(',', 2)  # 최대 3개로 분할
            if len(parts) >= 3:
                timestamp = parts[0].strip()
                event = parts[1].strip()
                message = parts[2].strip()
                
                log_entry = {
                    'timestamp': timestamp,
                    'event': event,
                    'message': message
                }
                log_list.append(log_entry)
    
    return log_list

# for line in lines[1:]:
# 의미: lines라는 리스트에서 첫 번째 줄(0번째 인덱스)을 제외한 두 번째 줄부터 끝까지 순회합니다.
# 용도: 보통 첫 줄은 헤더 이기 때문에 생략하고, 실제 데이터 줄만 처리합니다.

# if line.strip():
# 의미: 현재 줄에서 공백을 제거한 후 내용이 있는지 확인합니다.
# line.strip()은 앞뒤 공백, 개행문자(\n) 등을 제거합니다.
# 비어 있는 줄은 건너뛰기 위한 조건입니다.

# parts = line.split(',', 2)
# 의미: 현재 줄을 콤마(,) 기준으로 최대 3개 항목으로 나눕니다.
# split(',', 2) → 첫 두 개의 ,까지만 나누고, 나머지는 마지막 요소로 남김.

# if len(parts) >= 3:
# 의미: 나눈 결과가 3개 이상인지 확인합니다.
# 데이터가 잘못되어 항목이 부족하면 처리하지 않도록 방어 코드입니다.

# timestamp = parts[0].strip()
# 의미: 첫 번째 항목을 timestamp (시간 정보)로 저장.
# .strip()으로 앞뒤 공백 제거.

# event = parts[1].strip()
# 의미: 두 번째 항목을 event (이벤트 이름 등)로 저장.

# message = parts[2].strip()
# 의미: 세 번째 항목을 message (상세 메시지)로 저장.

# log_entry = {
#                 'timestamp': timestamp,
#                 'event': event,
#                 'message': message
#             }
# 의미: 위에서 추출한 3개의 값을 하나의 딕셔너리 형태의 로그 항목으로 만듭니다.
# 딕셔너리 구조로 저장하면 나중에 JSON 등으로 저장하거나 출력하기 편리합니다.

#  log_list.append(log_entry)
# 의미: 위에서 만든 log_entry 딕셔너리를 log_list라는 리스트에 추가합니다.
# 결과적으로 log_list에는 여러 개의 로그 딕셔너리가 쌓입니다.

# return log_list
# 의미: 전체 로그 처리 결과인 리스트 (log_list)를 함수 밖으로 반환합니다.
# 이 리스트는 각 줄에서 추출한 로그 정보를 담고 있습니다.

# 예시 입력 (lines)
# lines = [
#     "timestamp,event,message",  
#     "2025-08-21 09:00:00,LOGIN,User admin logged in",
#     "2025-08-21 09:05:00,LOGOUT,User admin logged out"
# ]

# 처리 결과 (log_list)
# [
#     {'timestamp': '2025-08-21 09:00:00', 'event': 'LOGIN', 'message': 'User admin logged in'},
#     {'timestamp': '2025-08-21 09:05:00', 'event': 'LOGOUT', 'message': 'User admin logged out'}
# ]


def display_list(log_list, title):
    
    # 리스트 내용을 화면에 출력하는 함수
    
    # Args:
    #     log_list (list): 출력할 로그 리스트
    #     title (str): 출력 제목
    
    print(f'\n=== {title} ===')
    for i, entry in enumerate(log_list):
        print(f'{i+1}. {entry["timestamp"]} | {entry["event"]} | {entry["message"]}')
    print('=' * 50)


def sort_logs_reverse_chronological(log_list):
    
    # 로그 리스트를 시간 역순으로 정렬하는 함수
    
    # Args:
    #     log_list (list): 정렬할 로그 리스트
        
    # Returns:
    #     list: 시간 역순으로 정렬된 로그 리스트
    
    try:
        sorted_logs = sorted(log_list, 
                           key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S'), 
                           reverse=True)
        return sorted_logs
    except ValueError as e:
        print(f'날짜 파싱 오류: {e}')
        return log_list


# convert_list_to_dict 사용자 정의 함수이며,
# 리스트를 딕셔너리(dict)로 변환하는 기능을 합니다.

def convert_list_to_dict(log_list):
    
    # 리스트를 사전(Dict) 객체로 변환하는 함수
    
    # Args:
    #     log_list (list): 변환할 로그 리스트
        
    # Returns:
    #     dict: 변환된 사전 객체
    
    log_dict = {}
    
    for i, entry in enumerate(log_list):
        key = f'log_{i+1:03d}'  
        log_dict[key] = {
            'timestamp': entry['timestamp'],
            'event': entry['event'],
            'message': entry['message']
        }
    
    return log_dict

# def convert_list_to_dict(log_list):
# log_list를 받아서 딕셔너리 형태로 변환하는 함수 정의

# log_dict = {}
# 결과를 저장할 빈 딕셔너리를 생성합니다.
# 이 안에 각 로그 항목을 log_001, log_002, ... 같은 키로 저장하게 됩니다.

# for i, entry in enumerate(log_list):
# log_list의 각 항목을 반복하면서 동시에 인덱스 i도 함께 가져옵니다.
# enumerate()는 (index, item) 형태로 반환합니다.

# key = f'log_{i+1:03d}'
# 로그 항목을 저장할 때 사용할 문자열 키 생성
# f'log_{i+1:03d}'는 포맷 문자열
# i = 0 → log_001
# i = 9 → log_010
# i = 99 → log_100
# :03d는 정수를 3자리로 0을 채워 출력하는 포맷입니다.

# log_dict[key] = {
#             'timestamp': entry['timestamp'],
#             'event': entry['event'],
#             'message': entry['message']
#         }

# 각 로그 항목(entry)의 내용을 timestamp, event, message 키를 가진 서브 딕셔너리로 구성해서 log_dict에 저장합니다.
# 위에서 만든 key(log_001, log_002 등)를 기준으로 저장됩니다.


#         log_dict[key] = {
#             'timestamp': entry['timestamp'],
#             'event': entry['event'],
#             'message': entry['message']
#         }
# 각 로그 항목(entry)의 내용을 timestamp, event, message 키를 가진 서브 딕셔너리로 구성해서 log_dict에 저장합니다.

# 위에서 만든 key(log_001, log_002 등)를 기준으로 저장됩니다.

# return log_dict
# 최종적으로 생성된 딕셔너리(log_dict)를 반환합니다.

# {
#     'log_001': {
#         'timestamp': '2025-08-21 09:00:00',
#         'event': 'LOGIN',
#         'message': 'User admin logged in'
#     },
#     'log_002': {
#         'timestamp': '2025-08-21 09:05:00',
#         'event': 'LOGOUT',
#         'message': 'User admin logged out'
#     }
# }

# key = f'log_{i+1:03d}'
# f는 f-string (formatted string literal)의 약자로, 문자열 안에서 변수나 표현식을 직접 넣고, 서식을 지정할 수 있게 해주는 기능입니다. 
# f: 포맷 문자열 (formatted string)
# {}: 중괄호 안에 있는 표현식이 실행된 값으로 치환
# i+1: 현재 인덱스에 1을 더한 값
# :03d: 서식 지정 — 정수를 3자리 숫자로 표시하고, 빈 자리는 0으로 채움

# i 값	i+1	f'log_{i+1:03d}' 결과
# 0	1	'log_001'
# 9	10	'log_010'
# 99	100	'log_100'
# 포맷 서식 정리: :03d
# 0	빈 자리를 0으로 채움
# 3	전체 자리수를 3자리로 맞춤
# d	정수(decimal) 형식으로 표시

# f (포맷 문자열, formatted string) : 문자열 안에서 변수를 삽입하고 포맷할 수 있음
# :03d는 숫자를 3자리로 0을 채워 출력하는 형식
# 결과적으로, log_001, log_002, ..., log_100 같은 일관된 키 이름 생성에 유용합니다

# enumerate()는 리스트, 튜플, 문자열 같은 반복 가능한 객체를 입력받아,
# 각 요소에 대해 **인덱스와 값 쌍(tuple)**을 포함하는 열거형 객체를 반환합니다.
# save_dict_to_json() 함수는 사용자 정의 함수로,
# 파이썬의 dict 자료형을 JSON 파일로 저장하는 기능을 합니다.

def save_dict_to_json(log_dict, filename):
    
    # 사전 객체를 JSON 파일로 저장하는 함수
    
    # Args:
    #     log_dict (dict): 저장할 사전 객체
    #     filename (str): 저장할 파일명
        
    # Returns:
    #     bool: 저장 성공 여부
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(log_dict, file, ensure_ascii=False, indent=2)
        print(f'{filename} 파일이 성공적으로 저장되었습니다.')
        return True
    except Exception as e:
        print(f'JSON 파일 저장 오류: {e}')
        return False
    
# filter_danger_keywords() 함수는 "위험한 메시지"만 걸러내는 필터링 함수로,
# 로그 데이터 중 위험 키워드를 포함한 항목만 골라내는 역할을 합니다.

def filter_danger_keywords(log_list):
    
    # 위험 키워드가 포함된 로그만 필터링하는 함수 (보너스 기능)
    
    # Args:
    #     log_list (list): 필터링할 로그 리스트
        
    # Returns:
    #     list: 위험 키워드가 포함된 로그 리스트
    
    danger_keywords = ['폭발', '누출', '고온', 'Oxygen', 'explosion', 'unstable']
    filtered_logs = []
    
    for entry in log_list:
        message_lower = entry['message'].lower()
        if any(keyword.lower() in message_lower for keyword in danger_keywords):
            filtered_logs.append(entry)
    
    return filtered_logs



def save_danger_logs(danger_logs, filename):
    
    # 위험 로그를 파일로 저장하는 함수
    
    # Args:
    #     danger_logs (list): 저장할 위험 로그 리스트
    #     filename (str): 저장할 파일명
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('timestamp,event,message\n')
            for entry in danger_logs:
                file.write(f'{entry["timestamp"]},{entry["event"]},{entry["message"]}\n')
        print(f'{filename} 파일이 성공적으로 저장되었습니다.')
    except Exception as e:
        print(f'위험 로그 파일 저장 오류: {e}')


def search_logs_by_keyword(json_filename):
    
    # JSON 파일에서 특정 키워드를 포함한 로그를 검색하는 함수 (보너스 기능)
    
    # Args:
    #     json_filename (str): 검색할 JSON 파일명
    
    try:
        with open(json_filename, 'r', encoding='utf-8') as file:
            log_dict = json.load(file)
        
        keyword = input('\n검색할 키워드를 입력하세요: ').strip()
        if not keyword:
            print('키워드가 입력되지 않았습니다.')
            return
        
        print(f'\n=== "{keyword}" 키워드 검색 결과 ===')
        found_count = 0
        
        for log_id, log_entry in log_dict.items():
            if keyword.lower() in log_entry['message'].lower():
                print(f'{log_id}: {log_entry["timestamp"]} | {log_entry["event"]} | {log_entry["message"]}')
                found_count += 1
        
        if found_count == 0:
            print('해당 키워드를 포함한 로그가 없습니다.')
        else:
            print(f'총 {found_count}개의 로그를 찾았습니다.')
        
    except FileNotFoundError:
        print(f'오류: {json_filename} 파일을 찾을 수 없습니다.')
    except json.JSONDecodeError:
        print(f'오류: {json_filename} 파일이 올바른 JSON 형식이 아닙니다.')
    except Exception as e:
        print(f'검색 중 오류가 발생했습니다: {e}')


def main():

    print('Hello Mars')
    print('\n=== 로켓 미션 로그 분석 프로그램 시작 ===')
    
    # 1. 로그 파일 읽기
    log_filename = 'mission_computer_main.log'
    content = read_log_file(log_filename)
    
    if content is None:
        print('프로그램을 종료합니다.')
        return
    
    # 2. 로그를 리스트로 변환
    log_list = parse_log_to_list(content)
    display_list(log_list, '파싱된 로그 리스트')
    
    # 3. 시간 역순으로 정렬
    sorted_log_list = sort_logs_reverse_chronological(log_list)
    display_list(sorted_log_list, '시간 역순으로 정렬된 로그 리스트')
    
    # 4. 리스트를 Dict 객체로 변환
    log_dict = convert_list_to_dict(sorted_log_list)
    
    # 5. JSON 파일로 저장
    json_filename = 'mission_computer_main.json'
    save_dict_to_json(log_dict, json_filename)
    
    # 6. 보너스 기능: 위험 키워드 필터링
    danger_logs = filter_danger_keywords(log_list)
    if danger_logs:
        print(f'\n=== 위험 키워드 감지 로그 ({len(danger_logs)}개) ===')
        for entry in danger_logs:
            print(f'{entry["timestamp"]} | {entry["event"]} | {entry["message"]}')
        save_danger_logs(danger_logs, 'danger_logs.csv')
    else:
        print('\n위험 키워드가 포함된 로그가 없습니다.')
    
    # 7. 보너스 기능: 키워드 검색
    if os.path.exists(json_filename):
        search_logs_by_keyword(json_filename)
    
    print('\n=== 로그 분석 완료 ===')


if __name__ == '__main__':
    main()