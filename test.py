import requests

# 요청을 보낼 엔드포인트 URL
url = "http://localhost:8080/predict"  # Flask 애플리케이션이 로컬에서 8000 포트로 실행된다고 가정

# POST 요청에 사용할 데이터
data = {
    "sentences": [
        "This is the first sentence.",
        "This is the second sentence."
    ]
}

# POST 요청 보내기
response = requests.post(url, json=data)

# 응답 데이터 출력
print(f"Status Code: {response.status_code}")
print(f"Response JSON: {response.json()}")
