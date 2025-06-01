from app.tools.sentiment_model import get_sentiment_score

def test_sentiment():
    result = get_sentiment_score("Apple is doing well in the market")
    assert isinstance(result, dict)
    assert all(k in result for k in ["positive", "neutral", "negative"])
