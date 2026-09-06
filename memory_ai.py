import json
import requests


def analyze_memories(chatgpt_memory, claude_memory):
    prompt = f"""
너는 MemoryGit의 기억 비교 AI이다.

아래 두 사용자 기억을 비교하라.

[ChatGPT 기억]
{chatgpt_memory}

[Claude 기억]
{claude_memory}

두 기억의 관계를 다음 5개 중 하나로 판단하라.

SAME
COMPLEMENTARY
CONFLICT
UPDATED
INDEPENDENT

각 의미는 다음과 같다.

SAME:
두 기억이 사실상 같은 의미

COMPLEMENTARY:
두 기억이 서로 보완 가능

CONFLICT:
두 기억이 서로 충돌

UPDATED:
한 기억이 다른 기억의 변경되거나 최신 상태

INDEPENDENT:
두 기억이 서로 관련 없음

그리고 두 기억을 자연스럽게 하나로 합칠 수 있다면
병합 문장을 만들어라.

반드시 아래 JSON 형식만 출력하라.

{{
  "relation": "SAME",
  "reason": "두 기억의 관계를 짧게 한국어로 설명",
  "merge_proposal": "병합된 기억"
}}

CONFLICT 또는 INDEPENDENT이면
merge_proposal은 빈 문자열로 작성하라.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    text = result["response"].strip()

    return json.loads(text)