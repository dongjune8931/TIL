"""
Notion API를 처리하는 모듈
"""
from notion_client import Client
from datetime import datetime, timedelta
import os

class NotionHandler:
    def __init__(self, token, database_id):
        self.client = Client(auth=token)
        self.database_id = database_id
    
    def get_today_pages(self):
        """오늘 작성완료 상태인 페이지들 가져오기"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        try:
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "and": [
                        {
                            "property": "날짜",
                            "date": {
                                "equals": today
                            }
                        },
                        {
                            "property": "상태",
                            "select": {
                                "equals": "작성완료"
                            }
                        }
                    ]
                },
                sorts=[
                    {
                        "property": "날짜",
                        "direction": "descending"
                    }
                ]
            )
            return response.get("results", [])
        except Exception as e:
            print(f"Notion API 에러: {e}")
            return []
    
    def get_page_content(self, page_id):
        """페이지의 전체 내용 가져오기"""
        try:
            # 페이지 속성 가져오기
            page = self.client.pages.retrieve(page_id=page_id)
            
            # 제목 추출
            title = self._extract_title(page)
            
            # 카테고리 추출
            category = self._extract_category(page)
            
            # 태그 추출
            tags = self._extract_tags(page)
            
            # 날짜 추출
            date = self._extract_date(page)
            
            # 블록 내용 가져오기
            blocks = self.client.blocks.children.list(block_id=page_id)
            content = self._blocks_to_markdown(blocks.get("results", []))
            
            return {
                "title": title,
                "category": category,
                "tags": tags,
                "date": date,
                "content": content,
                "page_id": page_id
            }
        except Exception as e:
            print(f"페이지 내용 가져오기 에러: {e}")
            return None
    
    def _extract_title(self, page):
        """제목 추출"""
        try:
            title_property = page["properties"]["제목"]["title"]
            if title_property:
                return title_property[0]["plain_text"]
            return "제목 없음"
        except:
            return "제목 없음"
    
    def _extract_category(self, page):
        """카테고리 추출"""
        try:
            category = page["properties"]["카테고리"]["select"]
            return category["name"] if category else "기타"
        except:
            return "기타"
    
    def _extract_tags(self, page):
        """태그 추출"""
        try:
            tags = page["properties"]["태그"]["multi_select"]
            return [tag["name"] for tag in tags]
        except:
            return []
    
    def _extract_date(self, page):
        """날짜 추출"""
        try:
            date = page["properties"]["날짜"]["date"]
            return date["start"] if date else datetime.now().strftime("%Y-%m-%d")
        except:
            return datetime.now().strftime("%Y-%m-%d")
    
    def _blocks_to_markdown(self, blocks):
        """Notion 블록을 마크다운으로 변환"""
        markdown_lines = []
        
        for block in blocks:
            block_type = block["type"]
            
            if block_type == "paragraph":
                text = self._extract_rich_text(block["paragraph"]["rich_text"])
                markdown_lines.append(text)
                markdown_lines.append("")
            
            elif block_type == "heading_1":
                text = self._extract_rich_text(block["heading_1"]["rich_text"])
                markdown_lines.append(f"# {text}")
                markdown_lines.append("")
            
            elif block_type == "heading_2":
                text = self._extract_rich_text(block["heading_2"]["rich_text"])
                markdown_lines.append(f"## {text}")
                markdown_lines.append("")
            
            elif block_type == "heading_3":
                text = self._extract_rich_text(block["heading_3"]["rich_text"])
                markdown_lines.append(f"### {text}")
                markdown_lines.append("")
            
            elif block_type == "bulleted_list_item":
                text = self._extract_rich_text(block["bulleted_list_item"]["rich_text"])
                markdown_lines.append(f"- {text}")
            
            elif block_type == "numbered_list_item":
                text = self._extract_rich_text(block["numbered_list_item"]["rich_text"])
                markdown_lines.append(f"1. {text}")
            
            elif block_type == "code":
                code_text = self._extract_rich_text(block["code"]["rich_text"])
                language = block["code"]["language"]
                markdown_lines.append(f"```{language}")
                markdown_lines.append(code_text)
                markdown_lines.append("```")
                markdown_lines.append("")
            
            elif block_type == "quote":
                text = self._extract_rich_text(block["quote"]["rich_text"])
                markdown_lines.append(f"> {text}")
                markdown_lines.append("")
            
            elif block_type == "to_do":
                text = self._extract_rich_text(block["to_do"]["rich_text"])
                checked = "x" if block["to_do"]["checked"] else " "
                markdown_lines.append(f"- [{checked}] {text}")
        
        return "\n".join(markdown_lines)
    
    def _extract_rich_text(self, rich_text_array):
        """Rich text를 일반 텍스트로 변환"""
        if not rich_text_array:
            return ""
        
        text_parts = []
        for text_obj in rich_text_array:
            plain_text = text_obj.get("plain_text", "")
            annotations = text_obj.get("annotations", {})
            
            # 볼드, 이탤릭 등 처리
            if annotations.get("bold"):
                plain_text = f"**{plain_text}**"
            if annotations.get("italic"):
                plain_text = f"*{plain_text}*"
            if annotations.get("code"):
                plain_text = f"`{plain_text}`"
            
            text_parts.append(plain_text)
        
        return "".join(text_parts)
    
    def update_page_status(self, page_id, status="발행완료"):
        """페이지 상태 업데이트"""
        try:
            self.client.pages.update(
                page_id=page_id,
                properties={
                    "상태": {
                        "select": {
                            "name": status
                        }
                    }
                }
            )
            print(f"페이지 상태 업데이트 완료: {status}")
        except Exception as e:
            print(f"상태 업데이트 에러: {e}")
