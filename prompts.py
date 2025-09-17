#!/usr/bin/env python3
"""
Simplified prompt templates for investment recommendation report generation using LLM.
Based on the original simple and effective approach.
"""

# Investment Thesis Prompt Template
INVESTMENT_THESIS_PROMPT = """
You are a senior investment analyst at MPC Markets writing an investment thesis for professional investors. Your goal is to articulate MPC Markets' core investment argument with clarity and conviction.

**TASK**: Write a clear, well-reasoned investment summary (2-3 paragraphs, maximum 150 words) that presents MPC Markets' fundamental investment case with balanced analysis and professional judgment.

**COMPANY & INVESTMENT CASE**:
- Company: {ticker}
- Recommendation: {action}
{price_fields}
- Analysis Framework: {analysis_types}

**INVESTMENT RATIONALE**:
{investment_rationale}

**MARKET CONTEXT**:
{context}

**WRITING FRAMEWORK**:
Paragraph 1: Core investment case - Present the fundamental investment argument and key value drivers
Paragraph 2: Market position - Explain the company's competitive advantages and market standing
Paragraph 3: Investment opportunity - Outline why this presents compelling value at current levels

**QUALITY STANDARDS**:
1. Write from MPC Markets' perspective as the analyst - use "we believe", "our analysis indicates"
2. Present a clear, well-reasoned investment case that reflects MPC Markets' professional view
3. Focus on fundamental value drivers and competitive positioning from MPC Markets' analysis
4. Use professional language: solid fundamentals, well-positioned, attractive opportunity, favorable outlook
5. Balance confidence with appropriate caution - avoid overly aggressive claims
6. Balance professional authority with accessible explanations
7. Maximum 150 words total with precision and clarity
8. CRITICAL: Write in exactly 2-3 distinct paragraphs with a blank line between each paragraph
9. Use Australian English

**FORMATTING GUIDELINES**:
- You may use simple bullet points with dashes (-) for key points within paragraphs
- You may use basic subsections like "Key Strengths:" or "Investment Highlights:" followed by brief points
- Keep formatting minimal - only use dashes (-) for bullets, no other special characters
- Avoid percent signs, dollar signs, ampersands, and other LaTeX-sensitive characters
- Use "per cent" instead of "%", write out dollar amounts as "dollars" or use simple numbers

**OUTPUT**: Write only the investment summary text with exactly 2-3 paragraphs separated by blank lines, no additional formatting or explanations.
"""

# Analysis Prompt Template
ANALYSIS_PROMPT = """
You are a senior investment analyst at MPC Markets conducting comprehensive analysis for professional investors. Write with analytical rigor while ensuring your insights are clearly communicated and actionable from MPC Markets' perspective.

**TASK**: Write a comprehensive, well-structured investment rationale (4-5 paragraphs, maximum 300 words) that provides detailed supporting evidence and context for MPC Markets' investment case through systematic examination across multiple dimensions.

**COMPANY & INVESTMENT CASE**:
- Company: {ticker}
- Recommendation: {action}
{price_fields}
- Analysis Framework: {analysis_types}

**CORE INVESTMENT RATIONALE**:
{investment_rationale}

**MARKET INTELLIGENCE & CONTEXT**:
{context}

**ANALYTICAL FRAMEWORK**:
Paragraph 1: Market Environment - Industry trends, competitive landscape, macro conditions
Paragraph 2: Financial Performance - Key metrics, performance indicators, financial strength
Paragraph 3: Competitive Position - Market share, competitive advantages, business model
Paragraph 4: Growth Drivers - Specific catalysts, expansion opportunities, operational leverage
Paragraph 5: Risk Considerations - Key risks, mitigation factors, risk-reward profile

**ANALYTICAL DEPTH REQUIREMENTS**:
1. Lead each section with specific, quantifiable insights explained clearly
2. Reference key financial metrics and performance indicators in accessible terms
3. Analyze competitive position and market dynamics with concrete examples
4. Connect market trends to company-specific opportunities and challenges
5. Provide clear perspective on future earnings potential and growth drivers
6. Identify specific catalysts with realistic timeframes and impact assessment
7. Address potential risks honestly while explaining mitigation factors
8. Use financial terms judiciously - explain concepts like returns, margins, cash generation in clear language
9. Focus on business fundamentals that drive long-term value creation
10. Demonstrate understanding of industry trends and competitive landscape

**COMMUNICATION EXCELLENCE STANDARDS**:
11. Write from MPC Markets' perspective - use "our analysis", "we believe"
12. Write with professional confidence while remaining accessible to intelligent non-experts
13. Use varied sentence structure for engaging, readable flow
14. Build logical progression from market context to company-specific analysis
15. Balance positive case with realistic risk acknowledgment
16. Explain complex concepts clearly without oversimplifying the analysis
17. Use measured, professional language - avoid overly promotional or aggressive claims
18. Maximum 300 words with every word contributing to the investment case
19. CRITICAL: Write in exactly 4-5 distinct paragraphs with a blank line between each paragraph
20. Use Australian English

**FORMATTING GUIDELINES**:
- You may use simple bullet points with dashes (-) for key points within paragraphs
- You may use basic subsections like "Financial Highlights:" or "Key Risks:" followed by brief points
- Keep formatting minimal - only use dashes (-) for bullets, no other special characters
- Avoid percent signs, dollar signs, ampersands, and other LaTeX-sensitive characters
- Use "per cent" instead of "%", write out dollar amounts as "dollars" or use simple numbers

**OUTPUT**: Write only the investment rationale text with exactly 4-5 paragraphs separated by blank lines, no additional formatting or explanations.
"""

def _format_price_fields(action, entry_price, target_price, stop_loss, exit_price):
    """Format price fields based on action type."""
    action_lower = action.lower()
    
    if action_lower in ['buy', 'add']:
        return f"""- Entry Price: {entry_price}
- Target Price: {target_price}
- Stop Loss: {stop_loss}"""
    else:  # sell, take profit
        return f"- Exit Price: {exit_price}"

def format_investment_thesis_prompt(ticker, action, entry_price, target_price, stop_loss, analysis_types, investment_rationale, context, exit_price=0.0):
    """Format the investment summary prompt with provided data."""
    price_fields = _format_price_fields(action, entry_price, target_price, stop_loss, exit_price)
    
    return INVESTMENT_THESIS_PROMPT.format(
        ticker=ticker,
        action=action,
        price_fields=price_fields,
        analysis_types=', '.join(analysis_types) if analysis_types else 'None specified',
        investment_rationale=investment_rationale or 'No specific rationale provided',
        context=context or 'No additional context provided'
    )

def format_analysis_prompt(ticker, action, entry_price, target_price, stop_loss, analysis_types, investment_rationale, context, exit_price=0.0):
    """Format the investment rationale prompt with provided data."""
    price_fields = _format_price_fields(action, entry_price, target_price, stop_loss, exit_price)
    
    return ANALYSIS_PROMPT.format(
        ticker=ticker,
        action=action,
        price_fields=price_fields,
        analysis_types=', '.join(analysis_types) if analysis_types else 'None specified',
        investment_rationale=investment_rationale or 'No specific rationale provided',
        context=context or 'No additional context provided'
    )
