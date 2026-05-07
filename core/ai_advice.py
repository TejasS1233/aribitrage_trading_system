import os
import json
from groq import Groq
from core.models import Opportunity


def get_groq_client():
    """Get Groq client from env"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_key_here":
        return None
    return Groq(api_key=api_key)


def generate_ai_advice(opps: list[Opportunity], config: dict = None) -> str:
    """Generate AI-powered market advice using Groq"""
    client = get_groq_client()
    
    if not opps:
        return "No opportunities found. Markets may be efficient or exchanges may be down."
    
    profit_opps = [o for o in opps if o.profit_pct > 0]
    
    if not profit_opps:
        return f"Found {len(opps)} opportunities but all negative. Fees exceed spreads. Try lower fees or wait for volatility."
    
    # Build market summary
    summary = []
    for o in profit_opps[:5]:
        route = f"{o.exchanges} {o.path}"
        summary.append(f"- {o.arb_type.value}: {route} = +{o.profit_pct:.4f}%")
    
    market_summary = "\n".join(summary)
    
    if not client:
        return f"AI not configured. Add GROQ_API_KEY to .env\nBest: {profit_opps[0].path[0]} ({profit_opps[0].arb_type.value}) +{profit_opps[0].profit_pct:.4f}%"
    
    # Build prompt with more educational detail
    best = max(profit_opps, key=lambda o: o.profit_pct)
    trading_size = 1000  # Assume $1000 trade for education
    
    prompt = f"""You are a crypto arbitrage trading coach. Analyze these live opportunities:

{market_summary}

Give brief educational advice (2-3 sentences) covering:
1. What the arbitrage is (how it works)
2. Why it's profitable (the spread)
3. How much to invest and expected return

Keep it beginner-friendly and practical."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI error: {str(e)}"


def check_ai_configured() -> bool:
    """Check if AI is configured"""
    return get_groq_client() is not None