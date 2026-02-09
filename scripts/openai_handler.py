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
                        "content": """당신은 IT 취준생을 위한 개발 학습 콘텐츠 전문가입니다.
주어진 TIL(Today I Learned) 내용을 기술 면접 대비용 학습 자료 수준으로 상세하게 정제해주세요.

작성 원칙:
1. **깊이**: 단순 개념 나열이 아닌, "왜 이렇게 동작하는지" 원리까지 설명
2. **실무 연결**: 실제 현업에서 어떻게 쓰이는지 구체적 사례 포함
3. **비교 분석**: 유사 개념이 있으면 차이점을 표로 비교
4. **코드 예제**: 동작하는 실전 코드와 함께 주석으로 상세 설명
5. **면접 대비**: 기술 면접에서 자주 나오는 질문과 모범 답변을 별도 섹션으로 작성
6. **시각화**: 가능하면 텍스트 기반 다이어그램이나 흐름도 포함

대상 독자: 신입 개발자 취업 준비생
톤: 친근하지만 전문적, 기술 블로그 스타일"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4096
            )
            
            refined_content = response.choices[0].message.content
            return self._format_final_markdown(til_data, refined_content)
            
        except Exception as e:
            print(f"OpenAI API 에러: {e}")
            return None
    
    def _create_refinement_prompt(self, til_data):
        """정제 요청 프롬프트 생성"""
        return f"""
다음 개발 학습 내용을 취준생이 기술 면접까지 대비할 수 있도록 상세하게 정제해주세요.

**제목**: {til_data['title']}
**카테고리**: {til_data['category']}
**태그**: {', '.join(til_data['tags'])}

**원본 내용**:
{til_data['content']}

---

아래 형식을 반드시 지켜서 작성해주세요. 각 섹션을 풍부하게 채워주세요.

## 개요
- 이 주제가 왜 중요한지, 어디에 쓰이는지 포함하여 3-5문장으로 요약

## 상세 내용
- 핵심 개념을 소제목(###)으로 나눠서 각각 상세히 설명
- 각 개념의 동작 원리, 장단점, 사용 시 주의사항 포함
- 유사 개념이 있으면 비교 표 작성
- 가능하면 텍스트 기반 다이어그램이나 흐름도 포함

## 코드 예제
- 실제로 동작하는 예제 코드 작성
- 코드 각 줄에 주석으로 상세 설명
- 잘못된 예시(Bad)와 올바른 예시(Good) 비교

## 핵심 포인트
- 반드시 기억해야 할 사항 5-7개를 번호 목록으로 정리

## 면접 대비 질문
- 이 주제와 관련된 기술 면접 질문 3-5개
- 각 질문에 대한 모범 답변을 함께 작성
- 답변은 면접에서 바로 사용할 수 있는 수준으로 구체적으로 작성

## 참고사항
- 관련 공식 문서나 권장 학습 키워드
- 실무에서의 베스트 프랙티스
- 이 주제와 함께 공부하면 좋은 연관 주제
"""
    
    def generate_summary(self, til_data):
        """TIL 한줄요약 생성"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "개발 학습 내용을 한 문장으로 요약해주세요. 30자 이내로, 핵심만 간결하게 작성하세요. 마크다운이나 특수문자 없이 순수 텍스트로만 작성하세요."
                    },
                    {
                        "role": "user",
                        "content": f"제목: {til_data['title']}\n내용:\n{til_data['content']}"
                    }
                ],
                temperature=0.3,
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"한줄요약 생성 에러: {e}")
            return til_data['title']

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
