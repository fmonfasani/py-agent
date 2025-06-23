---
name: Bug Report
about: Create a report to help us improve py-agent-client
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description
A clear and concise description of what the bug is.

## To Reproduce
Steps to reproduce the behavior:

1. Initialize agent with...
2. Call route method with...
3. Observe error...

```python
# Minimal code example that reproduces the issue
from py_agent_client import Agent

agent = Agent(api_key="test-key")
# ... code that causes the bug
```

## Expected Behavior
A clear and concise description of what you expected to happen.

## Actual Behavior
What actually happened instead.

## Error Messages
If applicable, add the full error message and stack trace:

```
Paste the complete error message here
```

## Environment Information
- **OS**: [e.g. macOS 13.0, Ubuntu 22.04, Windows 11]
- **Python Version**: [e.g. 3.9.7]
- **py-agent-client Version**: [e.g. 0.1.0]
- **AI Provider**: [e.g. OpenAI, Anthropic, DeepSeek]
- **Installation Method**: [e.g. pip, poetry, conda]

## Additional Context
- Is this a regression? (worked in a previous version)
- Does this happen consistently or intermittently?
- Any relevant configuration or environment variables?
- Are you using any custom routing rules?

## Impact
- How does this affect your use case?
- Is there a workaround you're currently using?

## Proposed Solution (Optional)
If you have ideas on how to fix this issue, please share them.

---

**Please check the following before submitting:**
- [ ] I have searched existing issues to avoid duplicates
- [ ] I have provided a minimal code example
- [ ] I have included environment information
- [ ] I have tested with the latest version