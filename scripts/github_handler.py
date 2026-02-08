"""
GitHub 파일 시스템을 처리하는 모듈
"""
import os
from datetime import datetime
from pathlib import Path

class GitHubHandler:
    def __init__(self, base_path="docs"):
        self.base_path = base_path
    
    def save_til(self, til_data, content):
        """TIL을 파일로 저장"""
        date = til_data['date']
        year, month, day = date.split('-')
        
        # 디렉토리 구조 생성: docs/2025/02/
        dir_path = Path(self.base_path) / year / month
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # 파일명: 2025-02-07.md
        filename = f"{date}.md"
        file_path = dir_path / filename
        
        # 파일 저장
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ TIL 저장 완료: {file_path}")
            return str(file_path)
        except Exception as e:
            print(f"❌ 파일 저장 에러: {e}")
            return None
    
    def update_readme(self, til_data, file_path, summary=None):
        """README.md 업데이트 (최신 TIL 목록 추가)"""
        readme_path = Path("../README.md")

        # 새 항목
        date = til_data['date']
        title = til_data['title']
        category = til_data['category']

        summary_text = f" - {summary}" if summary else ""
        new_entry = f"| {date} | [{title}]({file_path}) | `{category}` |{summary_text}"
        
        try:
            # 기존 README 읽기
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                content = self._create_readme_template()
            
            # "## 최근 학습 기록" 테이블에 새 항목 추가
            if "## 최근 학습 기록" in content:
                lines = content.split('\n')
                insert_idx = None

                for i, line in enumerate(lines):
                    if line.startswith("## 최근 학습 기록"):
                        # 테이블 헤더(2줄) 다음에 삽입
                        insert_idx = i + 4
                        break

                if insert_idx:
                    lines.insert(insert_idx, new_entry)
                    content = '\n'.join(lines)
            
            # 저장
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ README 업데이트 완료")
        except Exception as e:
            print(f"❌ README 업데이트 에러: {e}")
    
    def _create_readme_template(self):
        """README 템플릿 생성"""
        return """# 📚 Today I Learned (TIL)

매일 배운 내용을 기록하는 공간입니다.

## 최근 학습 기록

## 카테고리별 분류

### Python
### JavaScript
### Algorithm
### Database
### DevOps
### ETC

---

**자동화 도구**: Notion + OpenAI GPT-4 + GitHub Actions
"""
