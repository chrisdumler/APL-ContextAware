# Work Request #002: Behavioral Adaptation Framework

## SPRINT HEADER
```
SPRINT ID: CXT-002-behavioral-adaptation
DURATION: 2-3 hours
FRAMEWORK: SLC
PM: Chris Dumler (Human)
CODING AGENT: Claude Code
```

## SLC DEFINITION

### SIMPLE 🎯
**Single Focus:** Agent behavioral adaptation based on detected energy levels
- **Core Function:** Modify agent responses based on context (high/medium/low energy detection)
- **Scope Boundary:** NO complex personality changes, NO learning systems - just response style adaptation
- **Success Definition:** Clear, obvious behavioral differences between energy levels in agent responses

### LOVABLE ❤️
**User Impact:** Agent feels genuinely intelligent by matching response style to user energy
- **Visible Outcome:** Dramatically different conversation starters and response complexity based on detected energy
- **Quality Bar:** Behavioral changes feel natural and appropriate, not robotic
- **Demo Value:** Perfect demonstration of sophisticated agent capabilities for portfolio

### COMPLETE ✅
**Full Workflow:** Energy detection → Behavioral adaptation → Modified agent response → User experience
- **Input/Output:** Detected energy level → Adapted system prompt → Context-appropriate agent response
- **Integration Points:** Extends AgentFactory._build_system_prompt() with context-aware prompt generation
- **Test Scenarios:** Learning partner responses showing clear adaptation across all 3 energy levels

## TECHNICAL CONTEXT

### Current State
```
PROJECT: APL-ContextAware (/Users/chrisdumler/Projects/APL-ContextAware/)
BRANCH: main (or continue on feature/context-detection, or create feature/behavioral-adaptation)
KEY FILES: 
  - context_manager.py (working energy detection - 83.3% accuracy)
  - agent.py (has context_awareness config field, needs prompt generation enhancement)
  - main.py (displays context detection, needs behavioral integration)
DEPENDENCIES: No additional packages needed beyond current setup
LAST COMMIT: Context detection core completed and approved
```

### Architecture Constraints
```
MAINTAIN: Existing AgentFactory and prompt generation patterns
EXTEND: _build_system_prompt() method with context-aware capabilities
AVOID: Breaking existing agent configurations, complex behavioral models
VERSION COMPATIBILITY: Must work with current APL architecture and agent configs
```

## IMPLEMENTATION GUIDANCE

### Expected Approach
```
PATTERN: Extend existing AgentFactory with context-aware prompt generation
FILE CHANGES: 
  - MODIFY: agent.py (enhance _build_system_prompt with energy-based adaptations)
  - MODIFY: main.py (integrate context detection with agent response generation)
  - CREATE: behavioral_adaptations.py (energy-specific response patterns - optional)
INTEGRATION: Use detected energy from ContextManager to modify agent prompts
ERROR HANDLING: Graceful fallback to standard prompts if context detection fails
```

### AI-Specific Considerations
```
HALLUCINATION GUARDS: Use existing AgentFactory patterns, don't invent new LangChain APIs
CONTEXT LIMITS: Focus on learning partner use case from test scenarios document
VERIFICATION POINTS: Test each energy level adaptation individually before integration
```

## HUMAN-IN-LOOP CHECKPOINTS

### Checkpoint 1: Foundation ✋
**TRIGGER:** Enhanced _build_system_prompt() creates different prompts for each energy level
**VERIFY:** Chris tests prompt generation with high/medium/low energy inputs - prompts should be clearly different
**DECISION:** Prompt differences feel appropriate for energy levels → Continue

### Checkpoint 2: Integration ✋
**TRIGGER:** Context detection integrated with agent response generation in main.py
**VERIFY:** Chris has conversations with context-aware learning partner - agent responds differently based on energy
**DECISION:** Behavioral adaptation working and feeling natural → Continue

### Checkpoint 3: Polish ✋
**TRIGGER:** Learning partner demo scenarios work with clear behavioral differences
**VERIFY:** Chris tests all learning partner scenarios from test-scenarios.md - responses match expected energy adaptations
**DECISION:** Demo ready and compelling → Accept

## DELIVERY REQUIREMENTS

### Code Quality
- [ ] Maintains backward compatibility with existing agent configurations
- [ ] Clean integration with context detection from request #001
- [ ] Clear separation between context-aware and standard agent behavior
- [ ] Follows existing APL code patterns and conventions

### Testing Strategy
- [ ] Test each energy level adaptation individually
- [ ] Integration test with context detection workflow
- [ ] Learning partner demo scenarios from original test cases
- [ ] Verify non-context-aware agents still work normally

### Handoff Documentation
```
SUMMARY: Behavioral adaptation based on energy detection with learning partner focus
CHANGES: agent.py (enhanced prompt generation), main.py (integrated workflow)
TESTING: Run learning partner agent and test with energy scenarios
NEXT STEPS: UI enhancements and demo polish
ISSUES: Any limitations in behavioral adaptation range or effectiveness
```

## VERSION CONTROL STRATEGY

### Git Workflow
```
BRANCH: feature/behavioral-adaptation (create from main or continue existing)
COMMITS: 
  1. "Add energy-based prompt adaptation to AgentFactory"
  2. "Integrate behavioral adaptation with context detection"
  3. "Add learning partner demo scenarios and testing"
MERGE CRITERIA: All checkpoints pass, learning partner demo compelling
ROLLBACK PLAN: Revert to standard prompt generation if behavioral changes problematic
```

### Protection Points
```
BEFORE: git commit -m "Checkpoint: before behavioral adaptation implementation"
DURING: Commit after each checkpoint
AFTER: git commit -m "Complete: behavioral adaptation with learning partner demo"
```

## SPECIFIC ADAPTATION REQUIREMENTS

### High Energy Adaptation
**Prompt Modifications:**
- Suggest challenging, complex tasks
- Use energetic, enthusiastic tone
- Offer 20-30 minute session types (SYSTEM, INTEGRATE)
- Examples: "Want to build a system for automating evaluation runs across multiple models?"

### Medium Energy Adaptation  
**Prompt Modifications:**
- Suggest balanced, moderate complexity tasks
- Use informative, steady tone
- Offer 15-20 minute session types (AUTOMATE, VISUALIZE)
- Examples: "Should we create a simple dashboard for visualizing evaluation results?"

### Low Energy Adaptation
**Prompt Modifications:**
- Suggest simple, achievable tasks
- Use gentle, supportive tone
- Offer 10-15 minute session types (small utilities)
- Examples: "Want to write a small utility script to help with evaluation data formatting?"

### Integration with Learning Partner Profile
**Reference:** Use coding-learning-partner.md profile as basis for adaptations
**Focus:** Session types, task complexity, and energy-appropriate conversation starters
**Constraint:** Stay within learning partner domain expertise and goals

## EXPECTED DEMO OUTCOME

After completion, users should be able to:
1. **Start conversation** with context-aware learning partner
2. **Express different energy levels** in their messages
3. **See context detection** in UI panel (from request #001)
4. **Receive clearly different responses** based on their energy
5. **Experience natural, appropriate** behavioral adaptation

**Success Metric:** Side-by-side comparison shows obvious, appropriate behavioral differences between energy levels

## TIME TRACKING
**Estimated Duration:** 2-3 hours
**Actual Timestamps:**
- Start: [2025-06-05 16:42 (CST) - Claude Code starting behavioral adaptation work]
- Checkpoint 1: [2025-06-05 16:45 (CST) - Foundation complete]
- Checkpoint 2: [2025-06-05 16:51 (CST) - Integration complete]
- Checkpoint 3: [YYYY-MM-DD HH:MM - Polish complete]
- Complete: [YYYY-MM-DD HH:MM - Work request finished]
**Actual Duration:** [X.X hours - to be calculated]
**Accuracy:** [% difference from estimate]

## STATUS: READY FOR CLAUDE CODE 🚀