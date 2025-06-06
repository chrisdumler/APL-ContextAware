"""
Test suite for behavioral adaptation in AgentFactory.

Tests the energy-based prompt generation for learning partner agent.
"""

from agent import AgentFactory, AgentConfig


def test_energy_prompt_generation():
    """Test that different energy levels generate different prompts."""
    
    factory = AgentFactory()
    
    # Create learning partner config
    learning_partner_config = AgentConfig(
        name="test_learning_partner",
        description="Test learning partner for energy adaptation",
        expert_domain="learning_partner",
        context_awareness={
            "enabled": True,
            "energy_detection": True,
            "behavioral_adaptation": True
        }
    )
    
    # Test each energy level
    energy_levels = ["high", "medium", "low"]
    prompts = {}
    
    print("=== Behavioral Adaptation Test Results ===\n")
    
    for energy in energy_levels:
        prompt = factory._build_system_prompt(learning_partner_config, energy)
        prompts[energy] = prompt
        
        print(f"=== {energy.upper()} ENERGY PROMPT ===")
        print(prompt)
        print("\n" + "="*50 + "\n")
    
    # Verify prompts are different
    differences = []
    
    if "High Energy User Detected" in prompts["high"]:
        differences.append("✅ High energy adaptation detected")
    else:
        differences.append("❌ High energy adaptation missing")
        
    if "Medium Energy User Detected" in prompts["medium"]:
        differences.append("✅ Medium energy adaptation detected")
    else:
        differences.append("❌ Medium energy adaptation missing")
        
    if "Low Energy User Detected" in prompts["low"]:
        differences.append("✅ Low energy adaptation detected")
    else:
        differences.append("❌ Low energy adaptation missing")
    
    # Check that prompts are actually different
    if len(set(prompts.values())) == 3:
        differences.append("✅ All prompts are unique")
    else:
        differences.append("❌ Some prompts are identical")
    
    print("=== ADAPTATION VERIFICATION ===")
    for diff in differences:
        print(diff)
    
    success = all("✅" in diff for diff in differences)
    print(f"\n=== RESULT ===")
    print(f"Prompt generation: {'✅ PASSED' if success else '❌ FAILED'}")
    
    return success


def test_non_learning_partner():
    """Test that non-learning-partner agents don't get energy adaptations."""
    
    factory = AgentFactory()
    
    # Create non-learning partner config  
    tech_writer_config = AgentConfig(
        name="test_tech_writer",
        description="Test technical writer",
        expert_domain="technical_writer",
        context_awareness={
            "enabled": True,
            "energy_detection": True,
            "behavioral_adaptation": True
        }
    )
    
    prompt = factory._build_system_prompt(tech_writer_config, "high")
    
    has_adaptation = "ENERGY ADAPTATION" in prompt
    print(f"\n=== NON-LEARNING PARTNER TEST ===")
    print(f"Technical writer with high energy has adaptation: {has_adaptation}")
    print(f"Result: {'❌ FAILED - should not have adaptation' if has_adaptation else '✅ PASSED - no adaptation'}")
    
    return not has_adaptation


if __name__ == "__main__":
    print("Testing behavioral adaptation...")
    
    # Test energy-based prompt generation
    main_success = test_energy_prompt_generation()
    
    # Test that only learning partners get adaptations
    isolation_success = test_non_learning_partner()
    
    print(f"\n=== FINAL RESULT ===")
    print(f"Energy adaptation: {'✅ PASSED' if main_success else '❌ FAILED'}")
    print(f"Domain isolation: {'✅ PASSED' if isolation_success else '❌ FAILED'}")
    print("Ready for Checkpoint 1!" if main_success and isolation_success else "Needs refinement")