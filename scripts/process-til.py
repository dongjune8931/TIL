"""
메인 실행 스크립트
"""
import os
import sys
from dotenv import load_dotenv
from notion_handler import NotionHandler
from openai_handler import OpenAIHandler
from github_handler import GitHubHandler

def main():
    # 환경변수 로드
    load_dotenv()
    
    # API 키 확인
    notion_token = os.getenv("NOTION_TOKEN")
    notion_db_id = os.getenv("NOTION_DATABASE_ID")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not all([notion_token, notion_db_id, openai_key]):
        print("❌ 환경변수가 설정되지 않았습니다.")
        sys.exit(1)
    
    print("🚀 TIL 자동화 프로세스 시작...")
    
    # 핸들러 초기화
    notion = NotionHandler(notion_token, notion_db_id)
    openai = OpenAIHandler(openai_key)
    github = GitHubHandler(base_path="docs")
    
    # 1. Notion에서 오늘 작성완료된 페이지 가져오기
    print("\n📖 Notion에서 TIL 페이지 가져오는 중...")
    pages = notion.get_today_pages()
    
    if not pages:
        print("ℹ️  오늘 작성완료된 TIL이 없습니다.")
        return
    
    print(f"✅ {len(pages)}개의 TIL 페이지를 찾았습니다.")
    
    # 2. 각 페이지 처리
    for i, page in enumerate(pages, 1):
        print(f"\n{'='*60}")
        print(f"📝 처리중 ({i}/{len(pages)})")
        print(f"{'='*60}")
        
        # 페이지 내용 가져오기
        til_data = notion.get_page_content(page["id"])
        
        if not til_data:
            print("❌ 페이지 내용을 가져올 수 없습니다.")
            continue
        
        print(f"제목: {til_data['title']}")
        print(f"카테고리: {til_data['category']}")
        print(f"날짜: {til_data['date']}")
        
        # OpenAI로 내용 정제
        print("\n🤖 OpenAI로 내용 정제 중...")
        refined_content = openai.refine_til_content(til_data)

        if not refined_content:
            print("❌ 내용 정제에 실패했습니다.")
            continue

        print("✅ 내용 정제 완료")

        # 한줄요약 생성
        print("📝 한줄요약 생성 중...")
        summary = openai.generate_summary(til_data)
        print(f"✅ 한줄요약: {summary}")

        # GitHub에 저장
        print("\n💾 GitHub에 저장 중...")
        file_path = github.save_til(til_data, refined_content)

        if file_path:
            # README 업데이트
            github.update_readme(til_data, file_path, summary)
            
            # Notion 상태 업데이트
            notion.update_page_status(page["id"], "발행완료")
            
            print(f"\n✨ TIL 발행 완료: {file_path}")
    
    print(f"\n{'='*60}")
    print(f"🎉 전체 프로세스 완료! ({len(pages)}개 처리)")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
