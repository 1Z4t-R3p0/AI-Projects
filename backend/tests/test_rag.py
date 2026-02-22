import pytest
from unittest.mock import MagicMock, patch
from backend.rag.engine import RAGEngine

@pytest.fixture
def rag_engine_mock():
    with patch.dict('os.environ', {'OPENROUTER_API_KEY': 'test_key'}):
        engine = RAGEngine()
        # Mock the client to avoid real API calls
        engine.client = MagicMock()
        return engine

def test_search_web_success(rag_engine_mock):
    """Test successful web search with mocked DuckDuckGo."""
    mock_results = [{'title': 'Test Title', 'href': 'http://test.com', 'body': 'Test Snippet'}]
    
    with patch('backend.rag.engine.DDGS') as MockDDGS:
        mock_ddgs_instance = MockDDGS.return_value
        mock_ddgs_instance.__enter__.return_value.text.return_value = mock_results
        
        results = rag_engine_mock.search_web("test query")
        
        assert len(results) == 1
        assert results[0]['title'] == 'Test Title'
        assert results[0]['link'] == 'http://test.com'

def test_search_web_empty_fallback(rag_engine_mock):
    """Test fallback when search returns no results."""
    with patch('backend.rag.engine.DDGS') as MockDDGS:
        mock_ddgs_instance = MockDDGS.return_value
        mock_ddgs_instance.__enter__.return_value.text.return_value = []
        
        results = rag_engine_mock.search_web("test query")
        
        assert len(results) == 1
        assert results[0]['title'] == "Google Search"
        assert "google.com" in results[0]['link']

def test_classify_intent_roadmap(rag_engine_mock):
    """Test intent classification for roadmap."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "roadmap"
    rag_engine_mock.client.chat.completions.create.return_value = mock_response
    
    intent = rag_engine_mock._classify_intent("Give me a study plan for AI")
    assert intent == "roadmap"

def test_classify_intent_fallback(rag_engine_mock):
    """Test fallback intent classification when API fails."""
    rag_engine_mock.client.chat.completions.create.side_effect = Exception("API Error")
    
    # Keyword fallback test
    intent = rag_engine_mock._classify_intent("I want a roadmap for python")
    assert intent == "roadmap"
    
    intent = rag_engine_mock._classify_intent("find me a tutorial")
    assert intent == "search"

@pytest.mark.asyncio
async def test_generate_roadmap_structure(rag_engine_mock):
    """Test roadmap generation returns valid structure."""
    mock_json = '''
    {
        "title": "Test Roadmap",
        "modules": [
            {"week": 1, "topic": "Basics", "description": "Desc", "resources": []}
        ]
    }
    '''
    mock_response = MagicMock()
    mock_response.choices[0].message.content = mock_json
    rag_engine_mock.client.chat.completions.create.return_value = mock_response
    
    roadmap = await rag_engine_mock.generate_roadmap("AI", "Beginner")
    assert roadmap['title'] == "Test Roadmap"
    assert len(roadmap['modules']) == 1

@pytest.mark.asyncio
async def test_process_query_search_flow(rag_engine_mock):
    """Test the full pipeline for a search query."""
    # 1. Mock Classify to return 'search'
    # 2. Mock Search to return results
    # 3. Mock Final Response
    
    rag_engine_mock._classify_intent = MagicMock(return_value="search")
    rag_engine_mock.search_web = MagicMock(return_value=[
        {"title": "Res 1", "link": "link1", "snippet": "snip1"}
    ])
    
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Here are the search results."
    rag_engine_mock.client.chat.completions.create.return_value = mock_response
    
    response = await rag_engine_mock.process_query("search for python", "General")
    
    assert "Here are the search results." in response
    rag_engine_mock.search_web.assert_called()
