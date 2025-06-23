#!/usr/bin/env python3
"""
Integration examples for py-agent-client

Examples showing how to integrate py-agent-client with popular frameworks:
- FastAPI web applications
- Django applications  
- Streamlit data apps
- Jupyter notebooks
- CLI tools
"""

import asyncio
from typing import Optional, Dict, Any
import json


# FastAPI Integration Example
try:
    from fastapi import FastAPI, HTTPException, BackgroundTasks
    from pydantic import BaseModel
    
    class ChatRequest(BaseModel):
        message: str
        user_id: Optional[str] = None
        optimize_for: str = "balanced"
        max_cost: Optional[float] = None
    
    class ChatResponse(BaseModel):
        response: str
        model_used: str
        cost: float
        response_time: float
    
    # FastAPI app with py-agent integration
    app = FastAPI(title="AI Chat API with py-agent")
    
    # Global agent instance (in production, use dependency injection)
    from py_agent_client import Agent
    agent = Agent(api_key="your-py-agent-api-key")
    
    @app.post("/chat", response_model=ChatResponse)
    async def chat_endpoint(request: ChatRequest):
        """Chat endpoint with intelligent AI routing"""
        try:
            import time
            start_time = time.time()
            
            # Add user context if provided
            context = {"user_id": request.user_id} if request.user_id else None
            
            result = await agent.route(
                request.message,
                context=context,
                optimize_for=request.optimize_for,
                max_cost=request.max_cost
            )
            
            response_time = time.time() - start_time
            
            return ChatResponse(
                response=result.response,
                model_used=result.model,
                cost=result.cost,
                response_time=response_time
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/usage-stats")
    async def get_usage_stats():
        """Get AI usage statistics"""
        return agent.get_usage_stats()
    
    @app.post("/set-budget")
    async def set_budget(daily: float, monthly: float):
        """Set budget limits"""
        agent.set_budget(daily=daily, monthly=monthly)
        return {"message": "Budget updated successfully"}
    
except ImportError:
    print("FastAPI not installed. Skip FastAPI example.")


# Django Integration Example  
try:
    from django.http import JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    from django.views.decorators.http import require_http_methods
    import json
    
    # Django middleware for py-agent integration
    class PyAgentMiddleware:
        def __init__(self, get_response):
            self.get_response = get_response
            self.agent = Agent(api_key="your-py-agent-api-key")
        
        def __call__(self, request):
            # Add agent to request for use in views
            request.py_agent = self.agent
            response = self.get_response(request)
            return response
    
    @csrf_exempt
    @require_http_methods(["POST"])
    async def django_chat_view(request):
        """Django view with py-agent integration"""
        try:
            data = json.loads(request.body)
            message = data.get('message')
            
            if not message:
                return JsonResponse({'error': 'Message is required'}, status=400)
            
            result = await request.py_agent.route(
                message,
                optimize_for=data.get('optimize_for', 'balanced')
            )
            
            return JsonResponse({
                'response': result.response,
                'model': result.model,
                'cost': result.cost,
                'quality_score': result.quality_score
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
except ImportError:
    print("Django not installed. Skip Django example.")


# Streamlit Integration Example
try:
    import streamlit as st
    
    def streamlit_chat_app():
        """Streamlit app with py-agent integration"""
        st.title("🤖 AI Chat with Cost Optimization")
        st.sidebar.title("Settings")
        
        # Initialize agent in session state
        if 'agent' not in st.session_state:
            api_key = st.sidebar.text_input("py-agent API Key", type="password")
            if api_key:
                st.session_state.agent = Agent(api_key=api_key)
        
        if 'agent' not in st.session_state:
            st.warning("Please enter your py-agent API key in the sidebar.")
            return
        
        # Budget settings
        st.sidebar.subheader("Budget Settings")
        daily_budget = st.sidebar.number_input("Daily Budget ($)", value=10.0, min_value=0.1)
        monthly_budget = st.sidebar.number_input("Monthly Budget ($)", value=100.0, min_value=1.0)
        
        if st.sidebar.button("Update Budget"):
            st.session_state.agent.set_budget(daily=daily_budget, monthly=monthly_budget)
            st.sidebar.success("Budget updated!")
        
        # Optimization settings
        optimize_for = st.sidebar.selectbox(
            "Optimize for",
            ["cost", "quality", "speed", "balanced"]
        )
        
        # Chat interface
        st.subheader("Chat")
        
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if message["role"] == "assistant" and "metadata" in message:
                    with st.expander("Response Details"):
                        st.json(message["metadata"])
        
        # Chat input
        if prompt := st.chat_input("Type your message..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.write(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        result = asyncio.run(st.session_state.agent.route(
                            prompt,
                            optimize_for=optimize_for
                        ))
                        
                        st.write(result.response)
                        
                        # Add assistant message with metadata
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": result.response,
                            "metadata": {
                                "model": result.model,
                                "cost": f"${result.cost:.4f}",
                                "quality_score": result.quality_score,
                                "routing_reason": result.routing_reason
                            }
                        })
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        # Usage statistics
        st.sidebar.subheader("Usage Statistics")
        if st.sidebar.button("Show Stats"):
            stats = st.session_state.agent.get_usage_stats()
            st.sidebar.json(stats)
    
    # Run Streamlit app
    if __name__ == "__main__":
        streamlit_chat_app()
        
except ImportError:
    print("Streamlit not installed. Skip Streamlit example.")


# Jupyter Notebook Integration Example
def jupyter_notebook_helper():
    """Helper functions for Jupyter notebook integration"""
    
    class NotebookAgent:
        """Wrapper class for convenient notebook usage"""
        
        def __init__(self, api_key: str):
            self.agent = Agent(api_key=api_key)
            self.conversation_history = []
        
        async def ask(self, question: str, **kwargs) -> Dict[str, Any]:
            """Ask a question and get detailed response"""
            result = await self.agent.route(question, **kwargs)
            
            # Store in conversation history
            self.conversation_history.append({
                "question": question,
                "answer": result.response,
                "model": result.model,
                "cost": result.cost,
                "timestamp": "now"  # In real usage, use datetime
            })
            
            # Display in notebook-friendly format
            response_data = {
                "answer": result.response,
                "model_used": result.model,
                "cost": f"${result.cost:.4f}",
                "quality_score": f"{result.quality_score:.2f}",
                "routing_reason": result.routing_reason
            }
            
            return response_data
        
        def show_conversation(self):
            """Display conversation history"""
            for i, entry in enumerate(self.conversation_history):
                print(f"\n--- Conversation {i+1} ---")
                print(f"Q: {entry['question']}")
                print(f"A: {entry['answer'][:200]}...")
                print(f"Model: {entry['model']} | Cost: ${entry['cost']:.4f}")
        
        def get_total_cost(self) -> float:
            """Get total conversation cost"""
            return sum(entry['cost'] for entry in self.conversation_history)
        
        def export_conversation(self, filename: str):
            """Export conversation to JSON file"""
            with open(filename, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
    
    return NotebookAgent


# CLI Tool Integration Example
import argparse
import sys

class PyAgentCLI:
    """Command-line interface for py-agent"""
    
    def __init__(self):
        self.agent = None
    
    def setup_agent(self, api_key: str):
        """Initialize the agent"""
        self.agent = Agent(api_key=api_key)
    
    async def handle_query(self, args):
        """Handle query command"""
        if not self.agent:
            print("Error: API key not set. Use --api-key or set PY_AGENT_API_KEY environment variable.")
            return
        
        try:
            result = await self.agent.route(
                args.prompt,
                optimize_for=args.optimize_for,
                max_cost=args.max_cost
            )
            
            if args.output_format == "json":
                output = {
                    "response": result.response,
                    "model": result.model,
                    "cost": result.cost,
                    "quality_score": result.quality_score
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"Response: {result.response}")
                print(f"Model: {result.model} | Cost: ${result.cost:.4f}")
                
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    async def handle_stats(self, args):
        """Handle stats command"""
        if not self.agent:
            print("Error: API key not set.")
            return
        
        stats = self.agent.get_usage_stats()
        
        if args.output_format == "json":
            print(json.dumps(stats, indent=2))
        else:
            print("Usage Statistics:")
            print(f"  Total requests: {stats['total_requests']}")
            print(f"  Total cost: ${stats['total_cost']:.4f}")
            print(f"  Average cost: ${stats['average_cost']:.4f}")
            print(f"  Cost savings: ${stats['cost_savings']:.4f}")
    
    def create_parser(self):
        """Create command-line argument parser"""
        parser = argparse.ArgumentParser(description="py-agent CLI tool")
        parser.add_argument("--api-key", help="py-agent API key")
        parser.add_argument("--output-format", choices=["text", "json"], default="text")
        
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Query command
        query_parser = subparsers.add_parser("query", help="Send a query to AI")
        query_parser.add_argument("prompt", help="The prompt to send")
        query_parser.add_argument("--optimize-for", choices=["cost", "quality", "speed", "balanced"], 
                                default="balanced", help="Optimization preference")
        query_parser.add_argument("--max-cost", type=float, help="Maximum cost for the request")
        
        # Stats command
        stats_parser = subparsers.add_parser("stats", help="Show usage statistics")
        
        # Budget command
        budget_parser = subparsers.add_parser("budget", help="Set budget limits")
        budget_parser.add_argument("--daily", type=float, help="Daily budget limit")
        budget_parser.add_argument("--monthly", type=float, help="Monthly budget limit")
        
        return parser
    
    async def main(self):
        """Main CLI entry point"""
        parser = self.create_parser()
        args = parser.parse_args()
        
        # Get API key from args or environment
        import os
        api_key = args.api_key or os.getenv("PY_AGENT_API_KEY")
        
        if api_key:
            self.setup_agent(api_key)
        
        if args.command == "query":
            await self.handle_query(args)
        elif args.command == "stats":
            await self.handle_stats(args)
        elif args.command == "budget":
            if args.daily or args.monthly:
                self.agent.set_budget(daily=args.daily, monthly=args.monthly)
                print("Budget updated successfully")
            else:
                print("Specify --daily and/or --monthly budget amounts")
        else:
            parser.print_help()


# Example usage functions
async def demonstrate_integrations():
    """Demonstrate all integration examples"""
    print("🔌 py-agent-client Integration Examples")
    print("=" * 50)
    
    print("\n1. FastAPI Integration:")
    print("   - REST API endpoints for chat and usage stats")
    print("   - Automatic cost tracking and budget management")
    print("   - Production-ready with proper error handling")
    
    print("\n2. Django Integration:")
    print("   - Middleware for easy agent access in views")
    print("   - CSRF-safe endpoints")
    print("   - Session-based user context")
    
    print("\n3. Streamlit Integration:")
    print("   - Interactive chat interface")
    print("   - Real-time cost monitoring")
    print("   - Budget controls and optimization settings")
    
    print("\n4. Jupyter Notebook Integration:")
    print("   - Convenient wrapper class for notebooks")
    print("   - Conversation history tracking")
    print("   - Easy export and analysis capabilities")
    
    print("\n5. CLI Tool Integration:")
    print("   - Command-line interface for batch processing")
    print("   - JSON output for scripting")
    print("   - Environment variable configuration")
    
    print("\nTo use these integrations:")
    print("1. Install required dependencies (fastapi, django, streamlit)")
    print("2. Set your py-agent API key")
    print("3. Copy the relevant integration code to your project")
    print("4. Customize for your specific use case")


if __name__ == "__main__":
    # CLI mode
    if len(sys.argv) > 1:
        cli = PyAgentCLI()
        asyncio.run(cli.main())
    else:
        # Demo mode
        asyncio.run(demonstrate_integrations())