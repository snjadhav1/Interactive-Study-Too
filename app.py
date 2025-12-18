"""
Interactive Study Tool - Inspired by NotebookLM
Smart AI-like system with comprehensive knowledge base
"""

from flask import Flask, render_template, request, jsonify
import re
import random
from difflib import SequenceMatcher

app = Flask(__name__)

# =============================================================================
# COMPREHENSIVE KNOWLEDGE BASE - OLIGOPOLY & GAME THEORY
# =============================================================================

KNOWLEDGE_BASE = {
    "oligopoly": {
        "definition": "An oligopoly is a market structure characterized by a small number of large firms that dominate the market. These firms have significant market power and their decisions are interdependent - each firm must consider the reactions of its rivals when making pricing and output decisions.",
        "characteristics": [
            "Few dominant sellers controlling most of the market",
            "High barriers to entry (economies of scale, patents, capital requirements)",
            "Interdependence between firms - each firm's actions affect others",
            "Products may be homogeneous (steel) or differentiated (cars)",
            "Non-price competition is common (advertising, branding)",
            "Price rigidity - prices tend to be stable over time"
        ],
        "examples": "Examples include the smartphone industry (Apple, Samsung), soft drinks (Coca-Cola, Pepsi), airlines, banking, and telecommunications.",
        "keywords": ["oligopoly", "few firms", "market structure", "dominant", "interdependent", "barriers"]
    },
    
    "concentration_ratio": {
        "definition": "The concentration ratio measures the combined market share of the largest firms in an industry. The most common measure is the 4-firm concentration ratio (CR4), which shows the percentage of total market output produced by the four largest firms.",
        "interpretation": "A CR4 above 60% typically indicates an oligopoly. For example, if CR4 = 80%, the top 4 firms control 80% of the market.",
        "formula": "CR4 = Market share of firm 1 + firm 2 + firm 3 + firm 4",
        "limitations": "It doesn't account for the distribution of market share among the top firms, ignores potential competition, and uses arbitrary cutoffs.",
        "keywords": ["concentration", "ratio", "cr4", "market share", "measure", "percentage"]
    },
    
    "barriers_to_entry": {
        "definition": "Barriers to entry are obstacles that make it difficult for new firms to enter a market and compete with existing firms.",
        "types": [
            "Economies of scale - large firms have lower average costs",
            "Brand loyalty and advertising - established firms have customer recognition",
            "Patents and intellectual property - legal protection for innovations",
            "High capital requirements - large initial investment needed",
            "Control of essential resources - owning key inputs",
            "Government regulations and licenses",
            "Network effects - value increases with more users"
        ],
        "importance": "High barriers maintain the oligopolistic structure by preventing new competition.",
        "keywords": ["barriers", "entry", "economies of scale", "patents", "capital", "obstacles"]
    },
    
    "game_theory": {
        "definition": "Game theory is the study of strategic decision-making between interdependent players. In oligopoly, firms use game theory to predict rivals' reactions and choose optimal strategies.",
        "key_concepts": [
            "Players - the decision makers (firms)",
            "Strategies - the choices available to each player",
            "Payoffs - the outcomes/profits from each strategy combination",
            "Nash Equilibrium - no player can improve by unilaterally changing strategy"
        ],
        "applications": "Used to analyze pricing decisions, advertising wars, product launches, and capacity decisions in oligopolies.",
        "keywords": ["game theory", "strategic", "players", "strategies", "payoffs", "decision"]
    },
    
    "prisoners_dilemma": {
        "definition": "The Prisoner's Dilemma is a game theory model showing why two rational individuals might not cooperate even when it's in their best interest. Applied to oligopoly, it explains why firms might compete on price rather than collude.",
        "explanation": "Two prisoners are interrogated separately. If both stay silent (cooperate), they get light sentences. If both confess (defect), they get moderate sentences. If one confesses and one stays silent, the confessor goes free while the other gets a harsh sentence.",
        "oligopoly_application": "Firms face a similar dilemma: if both keep prices high (cooperate), both earn high profits. But each has an incentive to cut prices (defect) to steal market share. The result is often both cutting prices and earning lower profits.",
        "dominant_strategy": "Defection (cutting prices) is often the dominant strategy because it gives a better payoff regardless of what the rival does.",
        "keywords": ["prisoner", "dilemma", "cooperate", "defect", "confess", "dominant strategy"]
    },
    
    "nash_equilibrium": {
        "definition": "A Nash Equilibrium occurs when no player can improve their outcome by unilaterally changing their strategy, given what other players are doing. It's a stable state where everyone is doing their best given others' choices.",
        "example": "In the Prisoner's Dilemma, both defecting is the Nash Equilibrium - neither prisoner can do better by changing their strategy alone.",
        "oligopoly_relevance": "Nash Equilibrium helps predict market outcomes when firms make simultaneous decisions about pricing or output.",
        "keywords": ["nash", "equilibrium", "stable", "optimal", "strategy", "unilateral"]
    },
    
    "collusion": {
        "definition": "Collusion occurs when firms secretly agree to coordinate their actions, typically to raise prices or limit output, acting together like a monopoly to maximize joint profits.",
        "types": [
            "Formal collusion (cartels) - explicit agreements, often illegal",
            "Tacit collusion - implicit coordination without direct communication"
        ],
        "instability": "Collusion is unstable because each firm has an incentive to cheat by secretly cutting prices to gain market share.",
        "factors_affecting_stability": [
            "Number of firms - fewer firms makes coordination easier",
            "Product homogeneity - similar products make price-cutting more attractive",
            "Demand conditions - unstable demand makes cheating harder to detect",
            "Punishment mechanisms - credible threats deter cheating"
        ],
        "keywords": ["collusion", "cartel", "agreement", "coordinate", "cheat", "tacit"]
    },
    
    "kinked_demand_curve": {
        "definition": "The kinked demand curve model explains price rigidity in oligopolies. It assumes rivals will match price cuts but not price increases.",
        "explanation": "If a firm raises its price, rivals won't follow, so it loses many customers (elastic demand above current price). If it cuts price, rivals match it, so it gains few customers (inelastic demand below current price).",
        "result": "The demand curve has a 'kink' at the current price, and there's a discontinuity in the marginal revenue curve. This means firms have little incentive to change prices.",
        "criticism": "The model explains price rigidity but doesn't explain how the initial price was set.",
        "keywords": ["kinked", "demand", "curve", "price rigidity", "elastic", "inelastic"]
    },
    
    "price_leadership": {
        "definition": "Price leadership is a form of tacit collusion where one dominant firm sets the price and others follow.",
        "types": [
            "Dominant firm leadership - the largest firm sets prices",
            "Barometric leadership - the most knowledgeable firm signals price changes",
            "Rotating leadership - different firms lead at different times"
        ],
        "benefits": "Reduces uncertainty and price wars while avoiding illegal explicit collusion.",
        "keywords": ["price", "leadership", "leader", "follower", "dominant", "tacit"]
    },
    
    "non_price_competition": {
        "definition": "Non-price competition refers to strategies firms use to compete without changing prices, including advertising, product differentiation, customer service, and innovation.",
        "methods": [
            "Advertising and marketing campaigns",
            "Product differentiation and branding",
            "Quality improvements",
            "Customer service excellence",
            "Loyalty programs",
            "Research and development"
        ],
        "why_used": "In oligopolies, price competition can lead to destructive price wars. Non-price competition allows firms to compete while maintaining profits.",
        "keywords": ["non-price", "competition", "advertising", "differentiation", "branding", "marketing"]
    },
    
    "efficiency": {
        "definition": "Oligopolies are generally considered less efficient than perfectly competitive markets but may be more efficient than monopolies.",
        "allocative_efficiency": "Oligopolies don't achieve allocative efficiency because P > MC (price exceeds marginal cost), meaning society produces less than the optimal quantity.",
        "productive_efficiency": "Firms may not produce at minimum average cost, leading to productive inefficiency.",
        "dynamic_efficiency": "Oligopolies may achieve dynamic efficiency through innovation, as supernormal profits fund R&D.",
        "keywords": ["efficiency", "allocative", "productive", "dynamic", "welfare", "deadweight loss"]
    },
    
    "opec": {
        "definition": "OPEC (Organization of Petroleum Exporting Countries) is an example of an international cartel that coordinates oil production among member countries to influence global oil prices.",
        "mechanism": "Member countries agree on production quotas to control supply and maintain target prices.",
        "challenges": "Members often cheat on quotas, and non-member producers can increase output, undermining OPEC's power.",
        "keywords": ["opec", "oil", "cartel", "petroleum", "quota", "production"]
    }
}

# Video transcript content (embedded for offline use)
VIDEO_TRANSCRIPTS = {
    "Ec19ljjvlCI": {
        "title": "Oligopoly Market Structure Explained",
        "content": """
        Welcome to this comprehensive overview of oligopoly market structure.
        
        An oligopoly is a market structure where a few large firms dominate the industry. 
        Unlike perfect competition with many small firms, or monopoly with one firm, 
        oligopoly features a small number of interdependent sellers.
        
        Key characteristics of oligopoly include:
        
        First, there are few dominant sellers. The market is controlled by a small number 
        of large firms. We measure this using concentration ratios - the CR4 ratio shows 
        the market share of the top 4 firms. A CR4 above 60% typically indicates an oligopoly.
        
        Second, there's interdependence between firms. Each firm must consider how rivals 
        will react to their decisions. This is the defining feature of oligopoly and is 
        analyzed using game theory.
        
        Third, there are high barriers to entry. These include economies of scale, 
        brand loyalty, patents, and high capital requirements. These barriers protect 
        existing firms from new competition.
        
        Fourth, products can be homogeneous like steel or oil, or differentiated like 
        cars or smartphones.
        
        Examples of oligopolies include:
        - The smartphone market dominated by Apple and Samsung
        - Soft drinks with Coca-Cola and Pepsi
        - Commercial aircraft with Boeing and Airbus
        - Banking and telecommunications
        
        Price rigidity is common in oligopolies. The kinked demand curve model explains 
        this - firms expect rivals to match price cuts but not price increases.
        
        Firms may engage in collusion, either formal through cartels or tacit through 
        price leadership. However, collusion is often unstable due to the incentive to cheat.
        
        Non-price competition through advertising, branding, and innovation is common 
        because price wars can be destructive for all firms.
        
        In terms of efficiency, oligopolies typically don't achieve allocative efficiency 
        as price exceeds marginal cost. However, they may achieve dynamic efficiency 
        through innovation funded by supernormal profits.
        """,
        "topics": ["oligopoly", "market structure", "concentration ratio", "barriers to entry", 
                  "interdependence", "game theory", "price rigidity", "collusion", "efficiency"]
    },
    
    "Z_S0VA4jKes": {
        "title": "Game Theory and the Prisoner's Dilemma",
        "content": """
        Welcome to this explanation of game theory and its application to oligopoly.
        
        Game theory is the study of strategic decision-making. It analyzes how rational 
        players make choices when their outcomes depend on others' decisions.
        
        Key components of game theory:
        
        Players are the decision makers - in oligopoly, these are the firms.
        
        Strategies are the choices available to each player, such as setting high or 
        low prices.
        
        Payoffs are the outcomes from each combination of strategies, typically measured 
        as profits.
        
        The Prisoner's Dilemma is a fundamental game theory model. Here's how it works:
        
        Two prisoners are arrested and interrogated separately. Each can either stay 
        silent (cooperate) or confess (defect).
        
        If both stay silent, they each get 1 year in prison.
        If both confess, they each get 5 years.
        If one confesses and one stays silent, the confessor goes free while the 
        silent one gets 10 years.
        
        The dominant strategy for each prisoner is to confess - it gives a better 
        outcome regardless of what the other does. But when both confess, they're 
        worse off than if both had stayed silent.
        
        Applying this to oligopoly:
        
        Imagine two firms deciding whether to keep prices high or cut them.
        
        If both keep prices high (cooperate), both earn high profits - say $10 million each.
        If both cut prices (defect), both earn lower profits - say $5 million each.
        If one cuts and one keeps prices high, the price-cutter earns $12 million 
        while the other earns only $2 million.
        
        The dominant strategy is to cut prices. But the resulting Nash Equilibrium - 
        both cutting prices - leaves both firms worse off than if they had cooperated.
        
        This explains why firms might try to collude to keep prices high. But collusion 
        is unstable because each firm has an incentive to cheat.
        
        Nash Equilibrium is reached when no player can improve their outcome by 
        unilaterally changing their strategy. In the price-cutting game, both firms 
        cutting prices is the Nash Equilibrium.
        
        Real-world applications include:
        - Price wars between competitors
        - Advertising spending decisions  
        - Capacity and investment choices
        - Environmental agreements between countries
        
        Understanding game theory helps explain why oligopolies behave the way they do 
        and why cooperation is so difficult to maintain.
        """,
        "topics": ["game theory", "prisoner's dilemma", "nash equilibrium", "dominant strategy",
                  "payoffs", "cooperation", "defection", "collusion", "price wars"]
    }
}

# Quiz questions with explanations
QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "What is the defining characteristic of an oligopoly market structure?",
        "options": [
            "Many small firms competing",
            "A single firm dominating the market",
            "A few large firms with interdependent decision-making",
            "Perfect information for all market participants"
        ],
        "answer": "A few large firms with interdependent decision-making",
        "explanation": "Oligopoly is characterized by a small number of large firms whose decisions are interdependent - each firm must consider how rivals will react to their actions."
    },
    {
        "id": 2,
        "question": "What does a 4-firm concentration ratio (CR4) of 80% indicate?",
        "options": [
            "The market is perfectly competitive",
            "The top 4 firms control 80% of the market",
            "80 firms operate in the market",
            "Average costs are 80% of revenue"
        ],
        "answer": "The top 4 firms control 80% of the market",
        "explanation": "The CR4 measures the combined market share of the four largest firms. A CR4 of 80% means these four firms together produce 80% of total market output."
    },
    {
        "id": 3,
        "question": "In the Prisoner's Dilemma, what is the dominant strategy?",
        "options": [
            "Always cooperate",
            "Always defect (confess)",
            "Randomly choose",
            "Copy the other player"
        ],
        "answer": "Always defect (confess)",
        "explanation": "Defecting is the dominant strategy because it provides a better payoff regardless of what the other player does. However, mutual defection leads to a worse outcome than mutual cooperation."
    },
    {
        "id": 4,
        "question": "What is a Nash Equilibrium?",
        "options": [
            "The point where total profit is maximized",
            "When no player can improve by unilaterally changing strategy",
            "When all players choose the same strategy",
            "The most efficient market outcome"
        ],
        "answer": "When no player can improve by unilaterally changing strategy",
        "explanation": "A Nash Equilibrium is a stable state where each player is doing the best they can given what others are doing. No player has an incentive to change their strategy unilaterally."
    },
    {
        "id": 5,
        "question": "Why is collusion between oligopolistic firms often unstable?",
        "options": [
            "Government always detects it",
            "Firms have an incentive to cheat on agreements",
            "Customers refuse to pay high prices",
            "New firms always enter the market"
        ],
        "answer": "Firms have an incentive to cheat on agreements",
        "explanation": "While collusion can maximize joint profits, each individual firm can increase its own profit by secretly cutting prices. This incentive to cheat makes maintaining collusion difficult."
    },
    {
        "id": 6,
        "question": "The kinked demand curve model explains which phenomenon in oligopoly?",
        "options": [
            "How cartels set prices",
            "Why prices tend to be rigid",
            "How new firms enter the market",
            "Why firms maximize profits"
        ],
        "answer": "Why prices tend to be rigid",
        "explanation": "The kinked demand curve model assumes rivals match price cuts but not increases. This creates a kink in the demand curve and explains why oligopolistic prices tend to remain stable."
    },
    {
        "id": 7,
        "question": "Which is NOT a barrier to entry in an oligopoly?",
        "options": [
            "Economies of scale",
            "Brand loyalty",
            "Low startup costs",
            "Patents and licenses"
        ],
        "answer": "Low startup costs",
        "explanation": "High startup costs are a barrier to entry. Low startup costs would actually make it easier for new firms to enter, which is the opposite of a barrier."
    },
    {
        "id": 8,
        "question": "What is tacit collusion?",
        "options": [
            "A written agreement between firms",
            "Implicit coordination without direct communication",
            "Government-approved price fixing",
            "Competition through advertising"
        ],
        "answer": "Implicit coordination without direct communication",
        "explanation": "Tacit collusion occurs when firms coordinate their behavior without explicit agreements, often through price leadership or mutual understanding of market conditions."
    },
    {
        "id": 9,
        "question": "Why do oligopolies often engage in non-price competition?",
        "options": [
            "Price competition is illegal",
            "Price wars can be destructive for all firms",
            "Customers don't care about prices",
            "Advertising is cheaper than price cuts"
        ],
        "answer": "Price wars can be destructive for all firms",
        "explanation": "Price competition in oligopoly can trigger price wars that reduce profits for everyone. Non-price competition through advertising, quality, and innovation allows firms to compete while maintaining profitability."
    },
    {
        "id": 10,
        "question": "OPEC is an example of:",
        "options": [
            "Perfect competition",
            "A monopoly",
            "An international cartel",
            "A perfectly efficient market"
        ],
        "answer": "An international cartel",
        "explanation": "OPEC (Organization of Petroleum Exporting Countries) is a cartel where oil-producing nations coordinate production levels to influence global oil prices."
    }
]

# Flashcards for study
FLASHCARDS = [
    {"term": "Oligopoly", "definition": "A market structure with a few large firms that have interdependent decision-making and significant market power."},
    {"term": "Concentration Ratio", "definition": "A measure of market dominance, typically CR4 showing the combined market share of the four largest firms."},
    {"term": "Barriers to Entry", "definition": "Obstacles that prevent new firms from entering a market, such as economies of scale, patents, and brand loyalty."},
    {"term": "Interdependence", "definition": "The defining feature of oligopoly where each firm must consider rivals' reactions when making decisions."},
    {"term": "Game Theory", "definition": "The study of strategic decision-making between rational players whose outcomes depend on others' choices."},
    {"term": "Prisoner's Dilemma", "definition": "A game theory model showing why rational individuals might not cooperate even when it's mutually beneficial."},
    {"term": "Nash Equilibrium", "definition": "A stable state where no player can improve their outcome by unilaterally changing their strategy."},
    {"term": "Dominant Strategy", "definition": "A strategy that gives the best payoff regardless of what other players choose."},
    {"term": "Collusion", "definition": "When firms coordinate actions, typically to raise prices or limit output, acting like a monopoly."},
    {"term": "Cartel", "definition": "A formal agreement between firms to coordinate prices, output, or market division. Often illegal."},
    {"term": "Tacit Collusion", "definition": "Implicit coordination between firms without direct communication, often through price leadership."},
    {"term": "Price Leadership", "definition": "When one dominant firm sets the price and others follow, a form of tacit collusion."},
    {"term": "Kinked Demand Curve", "definition": "A model explaining price rigidity in oligopoly, assuming rivals match price cuts but not increases."},
    {"term": "Price Rigidity", "definition": "The tendency for prices to remain stable in oligopolies despite changes in costs or demand."},
    {"term": "Non-Price Competition", "definition": "Competition through advertising, quality, service, and innovation rather than price changes."},
    {"term": "Economies of Scale", "definition": "Cost advantages from large-scale production that serve as barriers to entry for smaller firms."},
    {"term": "Allocative Efficiency", "definition": "When P = MC, ensuring optimal resource allocation. Oligopolies typically don't achieve this."},
    {"term": "Productive Efficiency", "definition": "When firms produce at minimum average cost. May not be achieved in oligopoly."},
    {"term": "Dynamic Efficiency", "definition": "Efficiency through innovation over time, which oligopolies may achieve through R&D spending."},
    {"term": "Payoff Matrix", "definition": "A table showing the outcomes for each combination of strategies in a game theory scenario."},
    {"term": "OPEC", "definition": "Organization of Petroleum Exporting Countries - an international oil cartel coordinating production."},
    {"term": "Price War", "definition": "When firms repeatedly cut prices to gain market share, often reducing profits for all."},
    {"term": "Market Power", "definition": "The ability of a firm to influence market prices, typically by restricting output."},
    {"term": "Supernormal Profit", "definition": "Profit above normal return on capital, possible in oligopoly due to barriers to entry."},
    {"term": "Homogeneous Products", "definition": "Identical products from different sellers (e.g., steel, oil) - one type of oligopoly."}
]

# YouTube videos
YOUTUBE_VIDEOS = [
    {
        "id": "Ec19ljjvlCI",
        "title": "Oligopoly Market Structure - Complete Overview",
        "description": "Comprehensive explanation of oligopoly characteristics, concentration ratios, barriers to entry, and firm behavior.",
        "thumbnail": "https://img.youtube.com/vi/Ec19ljjvlCI/maxresdefault.jpg"
    },
    {
        "id": "Z_S0VA4jKes",
        "title": "Game Theory & Prisoner's Dilemma in Economics",
        "description": "Understanding strategic decision-making, Nash equilibrium, and why cooperation is difficult in oligopolies.",
        "thumbnail": "https://img.youtube.com/vi/Z_S0VA4jKes/maxresdefault.jpg"
    }
]

# =============================================================================
# SMART AI RESPONSE SYSTEM
# =============================================================================

def calculate_similarity(str1, str2):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def find_relevant_topics(query):
    """Find relevant topics from knowledge base based on query"""
    query_lower = query.lower()
    relevant = []
    
    for topic_key, topic_data in KNOWLEDGE_BASE.items():
        score = 0
        
        # Check keywords
        for keyword in topic_data.get("keywords", []):
            if keyword in query_lower:
                score += 10
        
        # Check topic name
        if topic_key.replace("_", " ") in query_lower:
            score += 15
        
        # Calculate text similarity
        if "definition" in topic_data:
            similarity = calculate_similarity(query, topic_data["definition"][:200])
            score += similarity * 5
        
        if score > 0:
            relevant.append((topic_key, topic_data, score))
    
    # Sort by relevance score
    relevant.sort(key=lambda x: x[2], reverse=True)
    return relevant[:3]  # Return top 3 relevant topics

def find_video_content(query, video_id=None):
    """Find relevant content from video transcripts"""
    query_lower = query.lower()
    results = []
    
    videos_to_search = {video_id: VIDEO_TRANSCRIPTS[video_id]} if video_id and video_id in VIDEO_TRANSCRIPTS else VIDEO_TRANSCRIPTS
    
    for vid_id, video_data in videos_to_search.items():
        score = 0
        
        # Check topics
        for topic in video_data.get("topics", []):
            if topic in query_lower:
                score += 10
        
        # Check content
        content_lower = video_data["content"].lower()
        query_words = query_lower.split()
        for word in query_words:
            if len(word) > 3 and word in content_lower:
                score += 2
        
        if score > 0:
            results.append((vid_id, video_data, score))
    
    results.sort(key=lambda x: x[2], reverse=True)
    return results

def generate_ai_response(query, context="general", video_id=None):
    """Generate intelligent AI-like response based on knowledge base"""
    query_lower = query.lower()
    
    # Find relevant topics
    relevant_topics = find_relevant_topics(query)
    video_results = find_video_content(query, video_id)
    
    # Build response
    response_parts = []
    
    # Greeting detection
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    if any(greet in query_lower for greet in greetings):
        return "Hello! I'm your AI study assistant specializing in Oligopoly and Game Theory. I can help you understand market structures, the prisoner's dilemma, Nash equilibrium, collusion, and much more. What would you like to learn about?"
    
    # Help/capability questions
    if any(word in query_lower for word in ["what can you", "help me", "what do you know", "capabilities"]):
        return """I'm an AI tutor specialized in Oligopoly and Game Theory! I can help you with:

📚 **Market Structures**: Understanding oligopoly characteristics, concentration ratios, and barriers to entry

🎮 **Game Theory**: Prisoner's dilemma, Nash equilibrium, dominant strategies, and payoff analysis

💰 **Business Strategy**: Collusion, cartels, price leadership, and non-price competition

📊 **Economic Efficiency**: Allocative, productive, and dynamic efficiency in oligopolies

🎬 **Video Content**: I can answer questions about the embedded educational videos

Just ask me anything about these topics!"""

    # Check for specific question types
    if "what is" in query_lower or "define" in query_lower or "explain" in query_lower:
        if relevant_topics:
            topic_key, topic_data, _ = relevant_topics[0]
            response = f"**{topic_key.replace('_', ' ').title()}**\n\n{topic_data['definition']}"
            
            if "characteristics" in topic_data:
                response += "\n\n**Key Characteristics:**\n"
                for char in topic_data["characteristics"][:4]:
                    response += f"• {char}\n"
            
            if "types" in topic_data:
                response += "\n\n**Types:**\n"
                for t in topic_data["types"][:4]:
                    response += f"• {t}\n"
            
            return response
    
    # Example questions
    if "example" in query_lower:
        if "oligopoly" in query_lower:
            return """**Real-World Examples of Oligopolies:**

🍎 **Smartphones**: Apple and Samsung dominate the global market
🥤 **Soft Drinks**: Coca-Cola and Pepsi control most of the beverage market
✈️ **Commercial Aircraft**: Boeing and Airbus are the main manufacturers
🏦 **Banking**: A few major banks dominate most national markets
📱 **Telecom**: Usually 3-4 major carriers per country
🚗 **Automobiles**: Toyota, Volkswagen, GM, and a few others lead globally

These industries all share oligopoly characteristics: few dominant firms, high barriers to entry, and interdependent decision-making."""
        
        if "prisoner" in query_lower or "dilemma" in query_lower:
            return """**Prisoner's Dilemma - Business Example:**

Imagine two competing firms (Firm A and Firm B) deciding on prices:

| | Firm B: High Price | Firm B: Low Price |
|---|---|---|
| **Firm A: High Price** | Both earn $10M | A: $2M, B: $12M |
| **Firm A: Low Price** | A: $12M, B: $2M | Both earn $5M |

**Analysis:**
• If both keep prices high → Both earn $10M (best collective outcome)
• Each firm is tempted to cut prices → Get $12M while rival gets $2M
• But if both cut prices → Both earn only $5M (Nash Equilibrium)

This shows why maintaining collusion is difficult - there's always an incentive to cheat!"""

    # Why questions
    if "why" in query_lower:
        if "rigid" in query_lower or "stable" in query_lower:
            return """**Why Prices Are Rigid in Oligopolies:**

The kinked demand curve model explains this:

📈 **If a firm RAISES price**: Rivals don't follow → firm loses many customers (elastic demand)

📉 **If a firm CUTS price**: Rivals match the cut → firm gains few customers (inelastic demand)

**Result**: There's a "kink" in the demand curve at the current price. The firm faces:
• Elastic demand above the current price
• Inelastic demand below the current price

This means neither raising nor lowering prices increases profits significantly, so prices remain stable!"""
        
        if "collusion" in query_lower and ("fail" in query_lower or "unstable" in query_lower or "difficult" in query_lower):
            return """**Why Collusion Often Fails:**

🎯 **The Cheating Incentive**: Each firm can increase profits by secretly cutting prices while others maintain high prices

🔍 **Detection Problems**: It's hard to know if rivals are cheating, especially with:
• Many firms in the agreement
• Differentiated products
• Fluctuating demand

⚖️ **Legal Issues**: Formal collusion (cartels) is illegal in most countries

📊 **Factors That Make Collusion Harder:**
• More firms = harder to coordinate
• Heterogeneous products = harder to compare prices
• Unstable demand = price cuts look like cheating
• No credible punishment mechanism

This is the Prisoner's Dilemma in action - individual rationality leads to collective suboptimality!"""

    # How questions
    if "how" in query_lower:
        if "measure" in query_lower or "concentration" in query_lower:
            return """**How to Measure Market Concentration:**

**1. Concentration Ratio (CR)**
• CR4 = Market share of top 4 firms added together
• Example: If top 4 firms have 25%, 20%, 15%, and 10% → CR4 = 70%
• CR4 > 60% typically indicates an oligopoly

**2. Herfindahl-Hirschman Index (HHI)**
• Sum of squared market shares of all firms
• Example: Firms with 30%, 30%, 20%, 20% → HHI = 900 + 900 + 400 + 400 = 2,600
• HHI > 2,500 = highly concentrated market

**Interpreting Results:**
• Higher values = more concentrated = more oligopolistic
• Lower values = more competitive market structure"""

    # Comparison questions
    if "difference" in query_lower or "compare" in query_lower or "vs" in query_lower:
        if "monopoly" in query_lower:
            return """**Oligopoly vs Monopoly:**

| Feature | Oligopoly | Monopoly |
|---------|-----------|----------|
| **Number of Firms** | Few (2-10 typically) | One |
| **Market Power** | Significant but shared | Complete |
| **Pricing** | Interdependent | Price maker |
| **Barriers to Entry** | High | Very high/absolute |
| **Competition** | Yes (strategic) | None |
| **Examples** | Smartphones, airlines | Utilities, patented drugs |

**Key Difference**: In oligopoly, firms must consider rivals' reactions. In monopoly, there are no rivals to consider."""

        if "competition" in query_lower or "perfect" in query_lower:
            return """**Oligopoly vs Perfect Competition:**

| Feature | Oligopoly | Perfect Competition |
|---------|-----------|---------------------|
| **Number of Firms** | Few large firms | Many small firms |
| **Market Power** | Significant | None (price takers) |
| **Products** | May be differentiated | Homogeneous |
| **Barriers to Entry** | High | None |
| **Profits (Long Run)** | Supernormal possible | Normal only |
| **Efficiency** | Allocatively inefficient | Fully efficient |

**Key Difference**: Oligopolists have market power and make strategic decisions; perfectly competitive firms simply accept market prices."""

    # Video-specific questions
    if video_id and video_id in VIDEO_TRANSCRIPTS:
        video = VIDEO_TRANSCRIPTS[video_id]
        video_content = video["content"].lower()
        
        # Check if query relates to video content
        matched_topics = []
        for topic in video["topics"]:
            if topic in query_lower or any(word in query_lower for word in topic.split()):
                matched_topics.append(topic)
        
        if matched_topics:
            # Build response based on matched topics
            response_parts = [f"**Based on the video '{video['title']}':**\n"]
            
            for topic in matched_topics[:2]:
                # Clean topic name for lookup
                topic_key = topic.replace(" ", "_").replace("'", "").replace("-", "_")
                if topic_key in KNOWLEDGE_BASE:
                    topic_data = KNOWLEDGE_BASE[topic_key]
                    response_parts.append(f"\n**{topic.title()}:**\n{topic_data['definition']}")
                elif topic == "prisoner's dilemma" or "prisoner" in topic:
                    response_parts.append(f"\n**Prisoner's Dilemma:**\n{KNOWLEDGE_BASE['prisoners_dilemma']['definition']}")
                elif topic == "nash equilibrium" or "nash" in topic:
                    response_parts.append(f"\n**Nash Equilibrium:**\n{KNOWLEDGE_BASE['nash_equilibrium']['definition']}")
            
            # Add relevant excerpt from video
            response_parts.append(f"\n\n📺 *This is covered in detail in the video at various points.*")
            
            return "\n".join(response_parts)
        
        # Search video content for query words
        query_words = [w for w in query_lower.split() if len(w) > 3]
        matches_in_content = sum(1 for word in query_words if word in video_content)
        
        if matches_in_content > 0:
            # Extract relevant portion from video content
            content_lines = video["content"].strip().split('\n')
            relevant_lines = []
            for line in content_lines:
                line_lower = line.lower()
                if any(word in line_lower for word in query_words if len(word) > 3):
                    if line.strip():
                        relevant_lines.append(line.strip())
            
            if relevant_lines:
                return f"""**Based on the video '{video['title']}':**

{chr(10).join(relevant_lines[:5])}

📺 The video covers: {', '.join(video['topics'][:5])}

Is there a specific concept you'd like me to explain in more detail?"""
        
        # General video question - return video summary
        return f"""**From the video "{video['title']}":**

{video['content'][:800]}...

📚 **Topics covered:** {', '.join(video['topics'])}

Feel free to ask about any specific topic from this video!"""

    # If we found relevant topics, build a comprehensive response
    if relevant_topics:
        topic_key, topic_data, _ = relevant_topics[0]
        
        response = f"Great question! Let me explain **{topic_key.replace('_', ' ').title()}**:\n\n"
        response += topic_data["definition"] + "\n\n"
        
        if "characteristics" in topic_data:
            response += "**Key Points:**\n"
            for char in topic_data["characteristics"][:3]:
                response += f"• {char}\n"
        
        if len(relevant_topics) > 1:
            response += f"\n\n**Related Topics:** "
            related = [t[0].replace('_', ' ').title() for t in relevant_topics[1:]]
            response += ", ".join(related)
            response += "\n\nWould you like me to explain any of these related concepts?"
        
        return response
    
    # Default response with suggestions
    return """I'd be happy to help you learn about Oligopoly and Game Theory! 

Here are some topics I can explain in detail:

📚 **Market Structure Basics:**
• What is an oligopoly?
• How do we measure market concentration?
• What are barriers to entry?

🎮 **Game Theory:**
• What is the Prisoner's Dilemma?
• What is Nash Equilibrium?
• Why is collusion unstable?

💡 **Business Strategy:**
• How does price leadership work?
• Why do oligopolies have rigid prices?
• What is non-price competition?

Just ask me about any of these topics, or ask your own question!"""

# =============================================================================
# FLASK ROUTES
# =============================================================================

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get API status"""
    return jsonify({
        'gemini_enabled': True,  # We have our smart AI system
        'ai_enabled': True,
        'ai_provider': 'Smart Knowledge-Based AI',
        'videos_loaded': len(YOUTUBE_VIDEOS),
        'topics_loaded': len(KNOWLEDGE_BASE),
        'quiz_questions': len(QUIZ_QUESTIONS),
        'flashcards': len(FLASHCARDS)
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        response = generate_ai_response(message)
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/videos')
def get_videos():
    """Get list of videos"""
    return jsonify({'videos': YOUTUBE_VIDEOS})

@app.route('/api/video/<video_id>/ask', methods=['POST'])
def ask_video_question(video_id):
    """Answer questions about a specific video"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        if video_id not in VIDEO_TRANSCRIPTS:
            return jsonify({'error': 'Video not found'}), 404
        
        response = generate_ai_response(question, context="video", video_id=video_id)
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/topics')
def get_topics():
    """Get list of topics"""
    topics = []
    for key, data in KNOWLEDGE_BASE.items():
        topics.append({
            'id': key,
            'title': key.replace('_', ' ').title(),
            'summary': data['definition'][:150] + '...' if len(data['definition']) > 150 else data['definition']
        })
    return jsonify({'topics': topics})

@app.route('/api/topic/<topic_id>')
def get_topic(topic_id):
    """Get details for a specific topic"""
    if topic_id in KNOWLEDGE_BASE:
        topic = KNOWLEDGE_BASE[topic_id]
        return jsonify({
            'id': topic_id,
            'title': topic_id.replace('_', ' ').title(),
            'content': topic
        })
    return jsonify({'error': 'Topic not found'}), 404

@app.route('/api/quiz')
def get_quiz():
    """Get quiz questions"""
    # Shuffle questions for variety
    questions = random.sample(QUIZ_QUESTIONS, min(10, len(QUIZ_QUESTIONS)))
    return jsonify({'questions': questions})

@app.route('/api/flashcards')
def get_flashcards():
    """Get flashcards"""
    # Shuffle flashcards
    cards = random.sample(FLASHCARDS, len(FLASHCARDS))
    return jsonify({'flashcards': cards})

@app.route('/api/generate-dialogue', methods=['POST'])
def generate_dialogue():
    """Generate two-person dialogue about a topic"""
    try:
        data = request.get_json()
        topic = data.get('topic', 'oligopoly')
        
        # Find topic in knowledge base
        topic_key = topic.lower().replace(' ', '_')
        topic_data = KNOWLEDGE_BASE.get(topic_key, KNOWLEDGE_BASE.get('oligopoly'))
        
        # Generate educational dialogue
        dialogue = [
            {
                "speaker": "Professor",
                "text": f"Today we're going to discuss {topic.replace('_', ' ')}. Do you know what this concept means?"
            },
            {
                "speaker": "Student", 
                "text": "I've heard the term before, but I'm not entirely sure about the details."
            },
            {
                "speaker": "Professor",
                "text": topic_data['definition']
            },
            {
                "speaker": "Student",
                "text": "That's interesting! Can you give me some real-world examples?"
            },
            {
                "speaker": "Professor",
                "text": topic_data.get('examples', f"Great examples include major industries like smartphones (Apple, Samsung), soft drinks (Coca-Cola, Pepsi), and airlines.")
            },
            {
                "speaker": "Student",
                "text": "I see! So these big companies have to think carefully about what their competitors might do?"
            },
            {
                "speaker": "Professor",
                "text": "Exactly! That's called interdependence - it's the defining feature of oligopoly. Each firm must consider how rivals will react to their decisions."
            }
        ]
        
        return jsonify({'dialogue': dialogue, 'topic': topic})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================================================
# RUN APPLICATION
# =============================================================================

# For Vercel serverless deployment
app.debug = False

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎓 INTERACTIVE STUDY TOOL - NotebookLM Inspired")
    print("="*60)
    print(f"📚 Knowledge Base: {len(KNOWLEDGE_BASE)} topics loaded")
    print(f"🎬 Videos: {len(YOUTUBE_VIDEOS)} videos available")
    print(f"❓ Quiz: {len(QUIZ_QUESTIONS)} questions ready")
    print(f"📇 Flashcards: {len(FLASHCARDS)} cards loaded")
    print(f"🤖 AI System: Smart Knowledge-Based Response Engine")
    print("="*60)
    print("🌐 Server starting...")
    print("="*60 + "\n")
    
    # Use environment port for deployment or default to 5000
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port, threaded=True)
