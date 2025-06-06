# Work Request #001: Context Detection Core

## SPRINT HEADER
```
SPRINT ID: CXT-001-detection-core
DURATION: 2-3 hours
FRAMEWORK: SLC
PM: Chris Dumler (Human)
CODING AGENT: Claude Code
```

## SLC DEFINITION

### SIMPLE 🎯
**Single Focus:** Basic energy level detection from user input text
- **Core Function:** ContextManager class that analyzes user input and returns energy level (high/medium/low)
- **Scope Boundary:** NO machine learning, NO complex NLP, NO external APIs - just keyword/pattern matching
- **Success Definition:** Can correctly classify 9/10 obvious energy test cases

### LOVABLE ❤️
**User Impact:** Agent actually "reads" user energy and responds appropriately
- **Visible Outcome:** Energy level displayed in UI with confidence score
- **Quality Bar:** Detection feels accurate and intuitive, not random
- **Demo Value:** Foundation for entire context-aware agent demonstration

### COMPLETE ✅
**Full Workflow:** Input text → Energy detection → Confidence score → Logging
- **Input/Output:** String input → {"energy": "high|medium|low", "confidence": 0.0-1.0, "reasoning": "..."}
- **Integration Points:** Called from main.py during message handling
- **Test Scenarios:** 10 test cases covering obvious high/medium/low energy patterns

## TECHNICAL CONTEXT

### Current State
```
PROJECT: APL-ContextAware (/Users/chrisdumler/Projects/APL-ContextAware/)
BRANCH: main (or create feature/context-detection)
KEY FILES: 
  - main.py (has placeholder energy detection)
  - utils.py (has context state functions)
  - agent.py (has context_awareness config field)
DEPENDENCIES: Standard Python, no additional packages needed
LAST COMMIT: Enhanced APL with context awareness hooks
```

### Architecture Constraints
```
MAINTAIN: Existing APL structure and naming conventions
EXTEND: Utils.py for context functions, create new context_manager.py
AVOID: Complex AI/ML libraries, external API calls, heavy dependencies
VERSION COMPATIBILITY: Python 3.9+, existing requirements.txt
```

## IMPLEMENTATION GUIDANCE

### Expected Approach
```
PATTERN: Simple class-based design following APL conventions
FILE CHANGES: 
  - CREATE: context_manager.py (new ContextManager class)
  - MODIFY: main.py (replace placeholder detection)
  - MODIFY: utils.py (add context helper functions if needed)
INTEGRATION: Import ContextManager in main.py, call during message handling
ERROR HANDLING: Graceful fallback to "medium" energy on detection errors
```

### AI-Specific Considerations
```
HALLUCINATION GUARDS: Use only basic Python string methods (in, lower, split, etc.)
CONTEXT LIMITS: Keep energy detection patterns simple and explicit
VERIFICATION POINTS: Test with obvious examples after each pattern group
```

## HUMAN-IN-LOOP CHECKPOINTS

### Checkpoint 1: Foundation ✋
**TRIGGER:** ContextManager class created with basic detection logic
**VERIFY:** Chris tests with 3 obvious cases: "I'm excited!", "What should we do?", "I'm tired"
**DECISION:** Detection accuracy feels reasonable → Continue

### Checkpoint 2: Integration ✋
**TRIGGER:** ContextManager integrated into main.py message handling
**VERIFY:** Chris sees energy levels displayed in UI during conversation
**DECISION:** Integration works without breaking existing functionality → Continue

### Checkpoint 3: Polish ✋
**TRIGGER:** Full test suite of 10 scenarios passes
**VERIFY:** Chris runs through all test cases and verifies accuracy
**DECISION:** 8+ out of 10 correct → Accept, <8 → Refine patterns

## DELIVERY REQUIREMENTS

### Code Quality
- [ ] ContextManager follows APL naming conventions
- [ ] Error handling for empty/invalid inputs
- [ ] Clear docstrings and inline comments
- [ ] No breaking changes to existing functionality

### Testing Strategy
- [ ] 10 test cases with expected energy levels
- [ ] Error handling tests (empty input, special characters)
- [ ] Integration test with main.py message flow
- [ ] Manual testing instructions for Chris

### Handoff Documentation
```
SUMMARY: Energy detection core with simple pattern matching
CHANGES: context_manager.py (new), main.py (updated detection call)
TESTING: Run python main.py and test with provided energy scenarios
NEXT STEPS: Behavioral adaptation based on detected energy
ISSUES: Limited to simple patterns, may need refinement based on usage
```

## VERSION CONTROL STRATEGY

### Git Workflow
```
BRANCH: feature/context-detection (create from main)
COMMITS: 
  1. "Add ContextManager class with basic energy detection"
  2. "Integrate context detection into main UI"
  3. "Add test scenarios and documentation"
MERGE CRITERIA: All checkpoints pass, no regressions in existing functionality
ROLLBACK PLAN: Revert main.py to placeholder detection if integration fails
```

### Protection Points
```
BEFORE: git commit -m "Checkpoint: before context detection implementation"
DURING: Commit after each checkpoint
AFTER: git commit -m "Complete: context detection core with integration"
```

## SPECIFIC TEST SCENARIOS

### High Energy Examples:
1. "I'm pumped up and ready to build something ambitious today!"
2. "Let's tackle something challenging and complex!"
3. "I'm feeling motivated and want to dive deep into this!"

### Medium Energy Examples:
1. "What should we work on today?"
2. "I'm ready to get started on something."
3. "Let's see what we can accomplish."

### Low Energy Examples:
1. "Not feeling super focused today, maybe something small?"
2. "I'm a bit tired, what's a simple task we could do?"
3. "Let me think... maybe something easy to start with?"

### Edge Cases:
1. "" (empty string)
2. "???" (unclear input)
3. "I'm excited but also tired" (mixed signals)

**Expected Accuracy:** 9/10 obvious cases, graceful handling of edge cases

## STATUS: READY FOR CLAUDE CODE 🚀