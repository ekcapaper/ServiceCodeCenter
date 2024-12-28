
import requests
import yaml

# API 엔드포인트 및 인증 정보 설정
API_BASE_URL = "http://127.0.0.1:8000/api/v1/projects"

def stop_project():
    # YAML 파일 불러오기
    with open('project.yaml', 'r') as file:
        data = yaml.safe_load(file)

    # target-state 변경
    data['project']['target-state'] = 'stopped'

    url = f"{API_BASE_URL}/{data["project"]["id"]}"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "targetState": "stopped"
    }

    try:
        response = requests.patch(url, json=payload, headers=headers)

        if response.status_code == 200:
            print("✅ 프로젝트 상태가 성공적으로 업데이트되었습니다.")
            print("📄 응답 데이터:", response.json())
        else:
            print(f"❌ 오류 발생! 상태 코드: {response.status_code}")
            print("📄 오류 메시지:", response.text)

    except requests.exceptions.RequestException as e:
        print("🚨 요청 중 예외 발생:", e)
