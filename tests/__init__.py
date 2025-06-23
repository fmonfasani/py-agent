"""
Tests package for py-agent-client

This package contains comprehensive test suites for all components
of the py-agent-client library.

Test Structure:
- test_client.py: Main Agent class tests
- test_cost_guardian.py: Budget management tests
- test_router.py: Routing logic tests
- test_providers/: Individual provider adapter tests
- integration/: End-to-end integration tests
- conftest.py: Shared fixtures and configuration

Run tests with:
    pytest
    pytest --cov=py_agent_client
    pytest -v tests/test_client.py
"""
