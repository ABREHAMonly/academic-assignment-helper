#backend\rag_service.py
import os
import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

# Initialize OpenAI client properly
openai_client = None
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.strip():
        openai_client = OpenAI(
            api_key=api_key,
            # Remove proxies parameter if not needed
        )
        print("✅ OpenAI client initialized")
    else:
        logger.warning("⚠️ OPENAI_API_KEY not found in environment variables")
except Exception as e:
    logger.error(f"❌ Failed to initialize OpenAI: {e}")
    openai_client = None

class RAGService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.client = openai_client
        
    def search_sources(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for academic sources using text similarity"""
        try:
            query_sql = text("""
                SELECT id, title, authors, publication_year, abstract, source_type
                FROM academic_sources 
                WHERE to_tsvector('english', title || ' ' || abstract || ' ' || authors) 
                      @@ plainto_tsquery('english', :query)
                OR abstract ILIKE :query_like 
                OR title ILIKE :query_like
                LIMIT :limit
            """)
            
            results = self.db.execute(
                query_sql, 
                {
                    "query": query,
                    "query_like": f"%{query}%",
                    "limit": top_k
                }
            ).fetchall()
            
            sources = []
            for r in results:
                sources.append({
                    "id": r[0],
                    "title": r[1],
                    "authors": r[2],
                    "year": r[3],
                    "abstract": r[4][:500] if r[4] else "",
                    "type": r[5],
                    "similarity_score": 0.8
                })
            
            return sources
            
        except Exception as e:
            print(f"⚠️ Source search failed: {e}")
            return self._fallback_search(query, top_k)
    
    def _fallback_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Fallback search when text search fails"""
        try:
            from models import AcademicSource
            sources = self.db.query(AcademicSource).limit(top_k).all()
            return [
                {
                    "id": s.id,
                    "title": s.title,
                    "authors": s.authors,
                    "year": s.publication_year,
                    "abstract": s.abstract[:500] if s.abstract else "",
                    "type": s.source_type,
                    "similarity_score": 0.7
                }
                for s in sources
            ]
        except:
            return []
    
    def analyze_assignment(self, text: str, sources: List[Dict]) -> Dict[str, Any]:
        """Analyze assignment text with AI"""
        if not self.client:
            return self._mock_analysis()
        
        try:
            source_context = "\n\n".join([
                f"Source {i+1}: {s['title']} by {s['authors']} ({s['year']})\n"
                f"Abstract: {s['abstract'][:300]}..."
                for i, s in enumerate(sources[:3])
            ])
            
            prompt = f"""
            Analyze this student assignment:
            
            Assignment Text (first 2000 chars):
            {text[:2000]}
            
            Relevant Sources:
            {source_context}
            
            Return JSON with: topic, themes, research_questions, academic_level, 
            suggestions, citation_recommendation.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an academic research assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={ "type": "json_object" }
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"⚠️ OpenAI analysis failed: {e}")
            return self._mock_analysis()
    
    def detect_plagiarism(self, text: str, sources: List[Dict]) -> Dict[str, Any]:
        """Check for potential plagiarism"""
        if not self.client:
            return {
                "plagiarism_score": 0.0,
                "flagged_sections": [],
                "confidence": "low"
            }
        
        try:
            prompt = f"""
            Compare assignment with sources. Return JSON with:
            - plagiarism_score: 0-100
            - flagged_sections: [{{text: "...", source: "...", similarity: ...}}]
            - confidence: high/medium/low
            
            Assignment: {text[:1500]}
            
            Sources: {json.dumps(sources[:3], indent=2)}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a plagiarism detection system."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={ "type": "json_object" }
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"⚠️ Plagiarism detection failed: {e}")
            return {
                "plagiarism_score": 0.0,
                "flagged_sections": [],
                "confidence": "low"
            }
    
    def _mock_analysis(self) -> Dict[str, Any]:
        """Return mock analysis when OpenAI is not available"""
        return {
            "topic": "Artificial Intelligence in Education",
            "themes": ["Machine Learning", "Personalized Learning", "Ethical Considerations"],
            "research_questions": ["How can AI improve student outcomes?"],
            "academic_level": "Undergraduate",
            "suggestions": "Add more specific examples and references.",
            "citation_recommendation": "APA"
        }