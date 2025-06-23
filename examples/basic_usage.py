#!/usr/bin/env python3
"""
Basic usage examples for py-agent-client

This example demonstrates the core functionality of py-agent-client
including basic routing, cost optimization, and usage analytics.
"""

import asyncio
import os
from py_agent_client import Agent


async def basic_routing_example():
    """Demonstrate basic AI routing capabilities"""
    print("🚀 Basic Routing Example")
    print("=" * 50)
    
    # Initialize agent with your API keys
    agent = Agent(
        api_key="your-py-agent-api-key",  # Get from py-agent.com
        providers={
            "openai": os.getenv("OPENAI_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "deepseek": os.getenv("DEEPSEEK_API_KEY")
        }
    )
    
    # Simple routing - agent automatically selects optimal model
    result = await agent.route(
        "Explain quantum computing in simple terms"
    )
    
    print(f"Response: {result.response}")
    print(f"Model used: {result.model}")
    print(f"Provider: {result.provider}")
    print(f"Cost: ${result.cost:.4f}")
    print(f"Quality score: {result.quality_score:.2f}")
    print(f"Routing reason: {result.routing_reason}")
    print()


async def optimization_preferences_example():
    """Demonstrate different optimization preferences"""
    print("⚡ Optimization Preferences Example")
    print("=" * 50)
    
    agent = Agent(api_key="your-py-agent-api-key")
    
    prompt = "Write a Python function to calculate fibonacci numbers"
    
    # Optimize for cost (cheapest model that meets quality threshold)
    result_cost = await agent.route(prompt, optimize_for="cost")
    print(f"Cost-optimized: {result_cost.model} - ${result_cost.cost:.4f}")
    
    # Optimize for quality (best model regardless of cost)
    result_quality = await agent.route(prompt, optimize_for="quality")
    print(f"Quality-optimized: {result_quality.model} - ${result_quality.cost:.4f}")
    
    # Optimize for speed (fastest response time)
    result_speed = await agent.route(prompt, optimize_for="speed")
    print(f"Speed-optimized: {result_speed.model} - ${result_speed.cost:.4f}")
    
    # Balanced optimization (default)
    result_balanced = await agent.route(prompt, optimize_for="balanced")
    print(f"Balanced: {result_balanced.model} - ${result_balanced.cost:.4f}")
    print()


async def context_management_example():
    """Demonstrate context management and session persistence"""
    print("🧠 Context Management Example")
    print("=" * 50)
    
    agent = Agent(api_key="your-py-agent-api-key")
    
    # First interaction with context
    context = {
        "user_id": "user123",
        "session_id": "session456",
        "preferences": {"domain": "finance", "complexity": "intermediate"}
    }
    
    result1 = await agent.route(
        "Explain compound interest",
        context=context
    )
    print(f"First response: {result1.response[:100]}...")
    
    # Follow-up interaction - agent remembers context
    result2 = await agent.route(
        "How does it apply to retirement planning?",
        context={"user_id": "user123", "session_id": "session456"}
    )
    print(f"Follow-up response: {result2.response[:100]}...")
    print()


async def budget_management_example():
    """Demonstrate budget management and cost controls"""
    print("💰 Budget Management Example")
    print("=" * 50)
    
    agent = Agent(api_key="your-py-agent-api-key")
    
    # Set budget limits
    agent.set_budget(daily=10.0, monthly=100.0)
    
    # Check current budget status
    remaining = agent.cost_guardian.get_remaining_budget()
    print(f"Remaining budget - Daily: ${remaining[0]:.2f}, Monthly: ${remaining[1]:.2f}")
    
    # Make requests with cost constraints
    try:
        result = await agent.route(
            "Generate a comprehensive market analysis report",
            max_cost=0.05  # Maximum cost for this request
        )
        print(f"Request completed: ${result.cost:.4f}")
    except Exception as e:
        print(f"Request blocked: {e}")
    
    # Get usage statistics
    stats = agent.get_usage_stats()
    print(f"Total requests: {stats['total_requests']}")
    print(f"Total cost: ${stats['total_cost']:.4f}")
    print(f"Average cost per request: ${stats['average_cost']:.4f}")
    print(f"Cost savings: ${stats['cost_savings']:.4f}")
    print()


async def error_handling_example():
    """Demonstrate error handling and fallback mechanisms"""
    print("🛡️ Error Handling Example")
    print("=" * 50)
    
    agent = Agent(api_key="your-py-agent-api-key")
    
    try:
        # Request that might fail or trigger fallbacks
        result = await agent.route(
            "This is a very long prompt that might cause issues..." * 100,
            quality_threshold=0.9,
            max_retries=3
        )
        print(f"Success with fallback: {result.model}")
    except Exception as e:
        print(f"Request failed after retries: {e}")
    
    print()


async def batch_processing_example():
    """Demonstrate batch processing of multiple requests"""
    print("📦 Batch Processing Example")
    print("=" * 50)
    
    agent = Agent(api_key="your-py-agent-api-key")
    
    prompts = [
        "What is machine learning?",
        "Explain blockchain technology",
        "How does quantum computing work?",
        "What is artificial intelligence?",
        "Describe cloud computing"
    ]
    
    # Process multiple requests
    tasks = [agent.route(prompt) for prompt in prompts]
    results = await asyncio.gather(*tasks)
    
    total_cost = sum(result.cost for result in results)
    print(f"Processed {len(results)} requests")
    print(f"Total cost: ${total_cost:.4f}")
    print(f"Average cost: ${total_cost/len(results):.4f}")
    
    # Show model distribution
    models_used = {}
    for result in results:
        models_used[result.model] = models_used.get(result.model, 0) + 1
    
    print("Model distribution:")
    for model, count in models_used.items():
        print(f"  {model}: {count} requests")
    print()


async def analytics_and_insights_example():
    """Demonstrate analytics and optimization insights"""
    print("📊 Analytics and Insights Example")
    print("=" * 50)
    
    agent = Agent(api_key="your-py-agent-api-key")
    
    # Make several requests to generate data
    test_prompts = [
        ("Simple question", "What is Python?"),
        ("Code generation", "Write a sorting algorithm in Python"),
        ("Analysis task", "Analyze the pros and cons of remote work"),
        ("Creative task", "Write a short poem about technology")
    ]
    
    for task_type, prompt in test_prompts:
        result = await agent.route(prompt)
        print(f"{task_type}: {result.model} - ${result.cost:.4f}")
    
    # Get detailed analytics
    analytics = agent.get_analytics()
    print(f"\nAnalytics Summary:")
    print(f"Cost efficiency score: {analytics['efficiency_score']:.2f}")
    print(f"Most cost-effective model: {analytics['best_model_for_cost']}")
    print(f"Highest quality model: {analytics['best_model_for_quality']}")
    print(f"Average response time: {analytics['avg_response_time']:.2f}s")
    
    # Get optimization recommendations
    recommendations = agent.get_recommendations()
    print(f"\nRecommendations:")
    for rec in recommendations:
        print(f"  • {rec}")
    print()


async def main():
    """Run all examples"""
    print("🎯 py-agent-client Examples")
    print("=" * 50)
    print("Make sure to set your API keys in environment variables:")
    print("  export OPENAI_API_KEY='your-openai-key'")
    print("  export ANTHROPIC_API_KEY='your-anthropic-key'")
    print("  export DEEPSEEK_API_KEY='your-deepseek-key'")
    print()
    
    try:
        await basic_routing_example()
        await optimization_preferences_example()
        await context_management_example()
        await budget_management_example()
        await error_handling_example()
        await batch_processing_example()
        await analytics_and_insights_example()
        
        print("✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")
        print("Make sure you have valid API keys configured.")


if __name__ == "__main__":
    asyncio.run(main())