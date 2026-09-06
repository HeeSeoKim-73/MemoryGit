# MemoryGit

사용자 승인 기반 다중 AI 기억 분기·병합 및 검증 프로토콜

## 소개

MemoryGit은 여러 AI에서 서로 다르게 형성된 사용자 기억을
Git의 Branch / Diff / Merge 개념처럼 관리하는 프로토타입입니다.

AI가 서로 다른 기억을 비교하고 병합안을 제안하며,
사용자가 최종 병합 결과를 승인합니다.

승인된 Canonical Memory는 SHA-256 Hash로 변환되고,
Ethereum Sepolia 테스트넷에 Hash를 기록하여
이후 기억이 변경되지 않았는지 검증할 수 있습니다.

## 핵심 흐름

ChatGPT Branch  
↓  
Claude Branch  
↓  
Semantic Diff  
↓  
AI Merge Proposal  
↓  
User Approval  
↓  
Canonical Memory  
↓  
SHA-256 Hash  
↓  
Ethereum Sepolia  
↓  
Blockchain Verification

## 주요 기능

- ChatGPT / Claude 기억 Branch 입력
- Ollama 기반 Semantic Diff
- SAME / COMPLEMENTARY / CONFLICT / UPDATED / INDEPENDENT 분류
- AI 기억 병합 제안
- 사용자 승인 / 거절
- Canonical Memory 생성
- SQLite 기반 기억 History 저장
- Parent Memory 관계 저장
- SHA-256 Hash 생성
- Ethereum Sepolia Hash 등록
- Blockchain Hash 검증

## 기술 스택

- Python
- Streamlit
- Ollama
- SQLite
- Web3.py
- Solidity
- Ethereum Sepolia
- SHA-256

## 실행 방법

### 1. Python 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. Ollama 설치
```bash
https://ollama.com/
```
### 3. 모델 다운로드
```bash
ollama pull llama3.2:3b
```
### 4. 실행
```bash
streamlit run app.py
```

## Smart Contract

contracts/MemoryRegistry.sol

승인된 기억의 원문은 블록체인에 저장하지 않습니다.

블록체인에는 다음 정보만 기록합니다.

Memory ID
SHA-256 Hash
승인 지갑 주소
Timestamp

## Architecture
AI A ─────┐
          │
          ├── Semantic Diff
          │
AI B ─────┘
              ↓
        Merge Proposal
              ↓
        User Approval
              ↓
       Canonical Memory
              ↓
           SHA-256
              ↓
    Ethereum Sepolia

