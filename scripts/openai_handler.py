"""
OpenAI API를 처리하는 모듈
"""
from openai import OpenAI
import os

class OpenAIHandler:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"  # 또는 "gpt-4o"
    
    def refine_til_content(self, til_data):
        """TIL 내용을 정제하고 보완"""
        
        prompt = self._create_refinement_prompt(til_data)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """당신은 개발 학습 내용을 정리하는 전문가입니다.
주어진 TIL(Today I Learned) 내용을 다음 기준으로 정제해주세요:

1. **구조화**: 논리적 흐름으로 재구성
2. **명확성**: 애매한 표현을 구체적으로 수정
3. **완성도**: 부족한 설명이나 예제 추가
4. **가독성**: 마크다운 형식으로 깔끔하게 정리
5. **심화**: 관련된 추가 지식이나 베스트 프랙티스 언급

단, 원본의 핵심 내용과 학습자의 목소리는 유지하세요."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            refined_content = response.choices[0].message.content
            return self._format_final_markdown(til_data, refined_content)
            
        except Exception as e:
            print(f"OpenAI API 에러: {e}")
            return None
    
    def _create_refinement_prompt(self, til_data):
        """정제 요청 프롬프트 생성"""
        return f"""
다음 개발 학습 내용을 정제하고 보완해주세요.

**제목**: {til_data['title']}
**카테고리**: {til_data['category']}
**태그**: {', '.join(til_data['tags'])}

**원본 내용**:
{til_data['content']}

---

위 내용을 다음 형식으로 정제해주세요:

## 개요
(배운 내용의 핵심 요약 - 2-3문장)

## 상세 내용
(구조화된 설명, 필요시 소제목 추가)

## 코드 예제
(실용적인 예제 코드, 원본에 있으면 개선하고 없으면 추가)

## 핵심 포인트
(기억해야 할 핵심 사항 3-5개)

## 참고사항
(추가로 알면 좋은 관련 지식, 주의사항, 베스트 프랙티스 등)
"""
    
    def _format_final_markdown(self, til_data, refined_content):
        """최종 마크다운 형식 생성"""
        date = til_data['date']
        title = til_data['title']
        category = til_data['category']
        tags = til_data['tags']
        
        # 메타데이터 헤더 생성
        header = f"""# {title}

> 📅 {date} | 📂 {category} | 🏷️ {', '.join(tags)}

---

"""
        
        # Footer 생성
        footer = f"""

---

**작성일**: {date}  
**카테고리**: {category}
"""
        
        return header + refined_content + footer
