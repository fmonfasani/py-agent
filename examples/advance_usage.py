#!/usr/bin/env python3
"""
Advanced usage examples for py-agent-client

This example demonstrates advanced features including:
- Custom routing rules
- Performance monitoring  
- Cost optimization strategies
- Integration patterns
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from py_agent_client import Agent
from py_agent_client.core.router import CustomRoutingRule
from py_agent_client.models import RouteRequest


class SmartAIWorkflow:
    """Example class showing how to integrate py-agent-client into applications"""
    
    def __init__(self):
        self.agent = Agent(api_key="your-py-agent-api-key")
        self.setup_custom_routing()
        self.setup_monitoring()
    
    def setup_custom_routing(self):
        """Configure custom routing rules based on business logic"""
        
        # Custom rules for different content types
        rules = [
            CustomRoutingRule(
                name="code_generation_rule",
                condition=lambda req: "code" in req.prompt.lower() or "function" in req.prompt.lower(),
                preferred_models=["gpt-4", "deepseek-coder"],
                max_cost=0.10
            ),
            CustomRoutingRule(
                name="simple_qa_rule", 
                condition=lambda req: len(req.prompt.split()) < 20 and "?" in req.prompt,
                preferred_models=["gpt-3.5-turbo"],
                max_cost=0.01
            ),
            CustomRoutingRule(
                name="analysis_rule",
                condition=lambda req: any(word in req.prompt.lower() for word in ["analyze", "report", "summary"]),
                preferred_models=["claude-3-sonnet", "gpt-4"],
                quality_threshold=0.85
            )
        ]
        
        self.agent.router.add_custom_rules(rules)
    
    def setup_monitoring(self):
        """Setup performance and cost monitoring"""
        self.metrics = {
            "requests_per_hour": [],
            "cost_per_hour": [],
            "quality_scores": [],
            "response_times": []
        }
    
    async def intelligent_document_processing(self, documents):
        """Process multiple documents with intelligent routing"""
        print("📄 Intelligent Document Processing")
        print("=" * 50)
        
        results = []
        total_cost = 0.0
        
        for i, doc in enumerate(documents):
            start_time = time.time()
            
            # Analyze document type and choose optimal processing
            doc_analysis = await self.agent.route(
                f"Classify this document type and suggest processing approach: {doc['title']}",
                optimize_for="speed"
            )
            
            # Process based on analysis
            if "technical" in doc_analysis.response.lower():
                result = await self.agent.route(
                    f"Provide technical analysis of: {doc['content']}",
                    optimize_for="quality",
                    context={"doc_type": "technical", "complexity": "high"}
                )
            elif "financial" in doc_analysis.response.lower():
                result = await self.agent.route(
                    f"Extract key financial insights from: {doc['content']}", 
                    optimize_for="balanced",
                    context={"doc_type": "financial", "compliance": True}
                )
            else:
                result = await self.agent.route(
                    f"Summarize key points from: {doc['content']}",
                    optimize_for="cost"
                )
            
            processing_time = time.time() - start_time
            total_cost += result.cost
            
            results.append({
                "document": doc['title'],
                "summary": result.response[:200] + "...",
                "model_used": result.model,
                "cost": result.cost,
                "processing_time": processing_time,
                "quality_score": result.quality_score
            })
            
            print(f"Processed '{doc['title']}' using {result.model} (${result.cost:.4f})")
        
        print(f"\nTotal processing cost: ${total_cost:.4f}")
        print(f"Average cost per document: ${total_cost/len(documents):.4f}")
        return results
    
    async def dynamic_cost_optimization(self):
        """Demonstrate dynamic cost optimization based on usage patterns"""
        print("🎯 Dynamic Cost Optimization")
        print("=" * 50)
        
        # Simulate different time periods with varying budgets
        scenarios = [
            {"name": "Peak Hours", "budget_multiplier": 0.7, "quality_threshold": 0.8},
            {"name": "Off-Peak", "budget_multiplier": 1.5, "quality_threshold": 0.7},
            {"name": "Weekend", "budget_multiplier": 1.0, "quality_threshold": 0.75}
        ]
        
        base_budget = 20.0
        test_prompts = [
            "Explain machine learning algorithms",
            "Write a business plan outline", 
            "Create a marketing strategy",
            "Analyze market trends"
        ]
        
        for scenario in scenarios:
            print(f"\n{scenario['name']} Scenario:")
            adjusted_budget = base_budget * scenario['budget_multiplier']
            
            # Adjust agent settings for scenario
            self.agent.set_budget(daily=adjusted_budget)
            self.agent.router.set_quality_threshold(scenario['quality_threshold'])
            
            scenario_cost = 0.0
            for prompt in test_prompts:
                result = await self.agent.route(
                    prompt,
                    optimize_for="cost" if scenario['budget_multiplier'] < 1.0 else "balanced"
                )
                scenario_cost += result.cost
                print(f"  {prompt[:30]}... → {result.model} (${result.cost:.4f})")
            
            print(f"  Total scenario cost: ${scenario_cost:.4f} (Budget: ${adjusted_budget:.2f})")
    
    async def a_b_testing_framework(self):
        """Demonstrate A/B testing different routing strategies"""
        print("🧪 A/B Testing Framework")
        print("=" * 50)
        
        test_prompts = [
            "Explain quantum computing",
            "Write Python code for data analysis",
            "Create a project timeline", 
            "Analyze customer feedback"
        ]
        
        strategies = {
            "cost_first": {"optimize_for": "cost", "quality_threshold": 0.7},
            "quality_first": {"optimize_for": "quality", "max_cost": 0.20},
            "balanced": {"optimize_for": "balanced", "quality_threshold": 0.75}
        }
        
        results = {strategy: [] for strategy in strategies}
        
        for strategy_name, params in strategies.items():
            print(f"\nTesting strategy: {strategy_name}")
            strategy_cost = 0.0
            strategy_quality = 0.0
            
            for prompt in test_prompts:
                result = await self.agent.route(prompt, **params)
                results[strategy_name].append(result)
                strategy_cost += result.cost
                strategy_quality += result.quality_score
                
                print(f"  {prompt[:25]}... → {result.model} "
                      f"(${result.cost:.4f}, Q:{result.quality_score:.2f})")
            
            avg_cost = strategy_cost / len(test_prompts)
            avg_quality = strategy_quality / len(test_prompts)
            
            print(f"  Strategy summary: Avg cost ${avg_cost:.4f}, Avg quality {avg_quality:.2f}")
        
        # Determine best strategy
        best_value = None
        best_score = 0
        
        for strategy_name, strategy_results in results.items():
            avg_cost = sum(r.cost for r in strategy_results) / len(strategy_results)
            avg_quality = sum(r.quality_score for r in strategy_results) / len(strategy_results)
            
            # Value score: quality per dollar
            value_score = avg_quality / avg_cost if avg_cost > 0 else 0
            
            if value_score > best_score:
                best_score = value_score
                best_value = strategy_name
        
        print(f"\n🏆 Best strategy: {best_value} (Value score: {best_score:.2f})")
    
    async def real_time_monitoring(self):
        """Demonstrate real-time monitoring and alerting"""
        print("📊 Real-time Monitoring")
        print("=" * 50)
        
        monitoring_window = 60  # seconds
        alert_thresholds = {
            "cost_per_minute": 1.0,
            "error_rate": 0.1,
            "avg_response_time": 5.0
        }
        
        start_time = time.time()
        requests_made = 0
        errors = 0
        total_cost = 0.0
        response_times = []
        
        print("Starting monitoring (60 second window)...")
        
        # Simulate continuous requests
        test_prompts = [
            "Quick question about Python",
            "Explain a concept briefly", 
            "Simple calculation",
            "Short answer needed"
        ] * 10  # Repeat for more data
        
        for prompt in test_prompts:
            if time.time() - start_time > monitoring_window:
                break
                
            request_start = time.time()
            
            try:
                result = await self.agent.route(prompt, optimize_for="speed")
                total_cost += result.cost
                response_times.append(time.time() - request_start)
            except Exception as e:
                errors += 1
                print(f"⚠️ Error detected: {e}")
            
            requests_made += 1
            
            # Check alerts every 10 requests
            if requests_made % 10 == 0:
                elapsed = time.time() - start_time
                cost_per_minute = (total_cost / elapsed) * 60
                error_rate = errors / requests_made
                avg_response_time = sum(response_times) / len(response_times) if response_times else 0
                
                # Check thresholds
                if cost_per_minute > alert_thresholds["cost_per_minute"]:
                    print(f"🚨 ALERT: High cost rate: ${cost_per_minute:.4f}/min")
                
                if error_rate > alert_thresholds["error_rate"]:
                    print(f"🚨 ALERT: High error rate: {error_rate:.2%}")
                
                if avg_response_time > alert_thresholds["avg_response_time"]:
                    print(f"🚨 ALERT: Slow responses: {avg_response_time:.2f}s avg")
        
        # Final report
        elapsed = time.time() - start_time
        print(f"\nMonitoring Summary ({elapsed:.1f}s):")
        print(f"  Requests: {requests_made}")
        print(f"  Errors: {errors} ({errors/requests_made:.1%})")
        print(f"  Total cost: ${total_cost:.4f}")
        print(f"  Cost rate: ${(total_cost/elapsed)*60:.4f}/min")
        print(f"  Avg response time: {sum(response_times)/len(response_times):.2f}s")
    
    async def cost_prediction_modeling(self):
        """Demonstrate cost prediction and budgeting"""
        print("💡 Cost Prediction Modeling")
        print("=" * 50)
        
        # Simulate historical usage data
        historical_patterns = [
            {"hour": i, "requests": 50 + (i % 12) * 10, "avg_cost": 0.02 + (i % 8) * 0.005}
            for i in range(24)
        ]
        
        # Predict costs for different scenarios
        scenarios = [
            {"name": "Current usage", "multiplier": 1.0},
            {"name": "50% growth", "multiplier": 1.5},
            {"name": "100% growth", "multiplier": 2.0},
            {"name": "Cost optimization", "multiplier": 0.7}
        ]
        
        print("Hourly cost predictions:")
        for scenario in scenarios:
            daily_cost = 0.0
            peak_hour_cost = 0.0
            
            for pattern in historical_patterns:
                hour_cost = pattern["requests"] * pattern["avg_cost"] * scenario["multiplier"]
                daily_cost += hour_cost
                peak_hour_cost = max(peak_hour_cost, hour_cost)
            
            monthly_cost = daily_cost * 30
            
            print(f"\n{scenario['name']}:")
            print(f"  Daily cost: ${daily_cost:.2f}")
            print(f"  Monthly cost: ${monthly_cost:.2f}")
            print(f"  Peak hour cost: ${peak_hour_cost:.2f}")
            
            # Budget recommendations
            recommended_daily = daily_cost * 1.2  # 20% buffer
            recommended_monthly = monthly_cost * 1.15  # 15% buffer
            
            print(f"  Recommended daily budget: ${recommended_daily:.2f}")
            print(f"  Recommended monthly budget: ${recommended_monthly:.2f}")


async def main():
    """Run advanced examples"""
    print("🚀 py-agent-client Advanced Examples")
    print("=" * 50)
    
    # Sample documents for processing
    sample_docs = [
        {
            "title": "Technical Architecture Document",
            "content": "This document outlines the microservices architecture..."
        },
        {
            "title": "Financial Quarterly Report", 
            "content": "Q3 financial results show revenue growth of 15%..."
        },
        {
            "title": "Marketing Strategy Brief",
            "content": "Our go-to-market strategy focuses on digital channels..."
        }
    ]
    
    workflow = SmartAIWorkflow()
    
    try:
        await workflow.intelligent_document_processing(sample_docs)
        await workflow.dynamic_cost_optimization()
        await workflow.a_b_testing_framework()
        await workflow.real_time_monitoring()
        await workflow.cost_prediction_modeling()
        
        print("\n✅ All advanced examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Advanced example failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())