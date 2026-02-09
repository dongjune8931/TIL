"""
OpenAI API를 처리하는 모듈
"""
from openai import OpenAI
import os

class OpenAIHandler:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"
    
    def refine_til_content(self, til_data):
        """TIL 내용을 정제하고 보완"""
        
        prompt = self._create_refinement_prompt(til_data)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """당신은 IT 취준생을 위한 개발 학습 콘텐츠 전문가이자, 10년차 시니어 개발자입니다.
주어진 TIL(Today I Learned) 내용을 기술 면접 대비 + 실무 투입 가능한 수준의 학습 자료로 작성해주세요.

핵심 원칙:
1. **원본 내용의 모든 개념을 빠짐없이 다룰 것** - 원본에 언급된 개념은 하나도 빠뜨리지 말고, 각각을 깊이 있게 확장하세요
2. **교과서 수준의 깊이** - 단순 정의가 아닌, "왜 이렇게 설계되었는지", "내부적으로 어떻게 동작하는지" 원리까지 설명
3. **실무 연결** - 현업에서 실제로 어떻게 쓰이는지, 어떤 상황에서 마주치는지 구체적 시나리오 포함
4. **비교 분석** - 유사하거나 헷갈리는 개념은 반드시 비교 표로 차이점 정리
5. **시각화** - 아키텍처, 흐름, 계층 구조 등은 텍스트 기반 ASCII 다이어그램으로 시각화
6. **면접 실전 대비** - 실제 면접에서 나오는 질문과 "이렇게 답하면 합격" 수준의 모범 답변
7. **분량** - 최대한 상세하고 풍부하게, 짧게 끝내지 마세요

대상 독자: 신입 개발자 취업 준비생 (CS 기본기를 다지는 중)
톤: 기술 블로그 스타일. 깔끔하고 전문적이면서 읽기 쉽게. 불필요한 감탄사나 이모지 없이, 핵심을 명확하게 전달하는 글."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=16384
            )
            
            refined_content = response.choices[0].message.content
            return self._format_final_markdown(til_data, refined_content)
            
        except Exception as e:
            print(f"OpenAI API 에러: {e}")
            return None
    
    def _create_refinement_prompt(self, til_data):
        """정제 요청 프롬프트 생성"""
        return f"""
다음은 내가 오늘 공부한 내용입니다. 이 내용을 바탕으로, 내가 적은 모든 개념을 하나도 빠뜨리지 말고 각각을 깊이 있게 확장해서 작성해주세요.
짧게 쓰지 말고, 각 섹션을 최대한 상세하고 풍부하게 채워주세요.

**제목**: {til_data['title']}
**카테고리**: {til_data['category']}
**태그**: {', '.join(til_data['tags'])}

**원본 내용**:
{til_data['content']}

---

아래 형식을 반드시 지켜서 작성해주세요.

## 개요
- 이 주제가 왜 중요한지, 실무에서 왜 알아야 하는지 5문장 이상으로 설명
- 이 기술이 탄생한 배경이나 해결하려는 문제도 간단히 언급

## 상세 내용
- 원본에 등장하는 모든 개념을 소제목(###)으로 나눠서 각각 상세히 설명
- 각 개념마다 다음을 포함:
  - 정의와 동작 원리 (내부적으로 어떻게 동작하는지)
  - 왜 이렇게 설계되었는지 (설계 이유/배경)
  - 실무에서 어떤 상황에 마주치는지 (구체적 시나리오)
  - 주의사항이나 흔한 실수
- 유사하거나 헷갈리는 개념이 있으면 반드시 비교 표 작성
- 구조나 흐름이 있는 개념은 ASCII 다이어그램으로 시각화

## 코드 예제
- 원본 내용과 관련된 실전 코드 작성
- 코드마다 주석으로 한 줄 한 줄 상세 설명
- 가능하면 잘못된 예시(Bad)와 올바른 예시(Good) 비교 포함

## 핵심 포인트
- 반드시 기억해야 할 사항 5-7개
- 각 포인트마다 왜 중요한지 한 줄 설명 추가

## 면접 대비 질문
- 이 주제로 실제 면접에서 나올 수 있는 질문 5개
- 각 질문에 대해 면접관이 감탄할 수준의 모범 답변 작성
- 답변에는 구체적 예시나 수치를 포함하여 설득력 있게 작성
- 꼬리 질문이 나올 수 있는 부분도 미리 대비하여 추가 설명

## 참고사항
- 이 주제를 더 깊이 공부하기 위한 검색 키워드
- 실무에서의 베스트 프랙티스
- 함께 공부하면 좋은 연관 주제와 그 이유
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
