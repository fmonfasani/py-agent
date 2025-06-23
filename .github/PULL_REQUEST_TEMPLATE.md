# Pull Request

## Description
Brief description of what this PR does and why.

Fixes #(issue_number)

## Type of Change
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🧹 Code cleanup or refactoring
- [ ] ⚡ Performance improvement
- [ ] 🔒 Security improvement
- [ ] 🧪 Test improvement

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed
- [ ] Integration tests pass

### Test Coverage
- Current coverage: X%
- Coverage after changes: Y%

### Manual Testing Done
Describe any manual testing you performed:

```python
# Example of how you tested the changes
from py_agent_client import Agent

agent = Agent(api_key="test")
# Test scenarios...
```

## Performance Impact
- [ ] No performance impact
- [ ] Performance improved
- [ ] Performance slightly decreased (justified)
- [ ] Significant performance impact (requires discussion)

**Benchmark Results** (if applicable):
- Before: X ms average response time
- After: Y ms average response time

## Cost Impact
For features that affect routing or cost optimization:
- [ ] No cost impact
- [ ] Cost savings improved
- [ ] Potential cost increase (justified)

## Documentation
- [ ] Code comments added/updated
- [ ] README updated (if needed)
- [ ] API documentation updated
- [ ] Examples updated/added
- [ ] CHANGELOG.md updated

## Security Considerations
- [ ] No security implications
- [ ] Security reviewed and approved
- [ ] Potential security concerns (documented below)

**Security Notes:**
(If applicable, describe any security considerations)

## Backward Compatibility
- [ ] Fully backward compatible
- [ ] Deprecation warnings added for changed functionality
- [ ] Breaking changes (documented in CHANGELOG)

**Migration Guide** (if breaking changes):
Steps users need to take to migrate:

1. Step 1
2. Step 2

## Dependencies
- [ ] No new dependencies
- [ ] New dependencies added (justified below)
- [ ] Dependencies updated

**New Dependencies:**
- dependency-name==version (reason for adding)

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Additional Notes
Any additional information that reviewers should know:

---

**For Maintainers:**
- [ ] Consider for next release
- [ ] Requires design review
- [ ] Needs additional testing
- [ ] Ready to merge