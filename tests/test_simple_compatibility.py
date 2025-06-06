"""
Simple backward compatibility test focusing on prompt generation.

Tests that existing agent types don't get energy adaptations.
"""

from agent import AgentFactory, AgentConfig
from utils import load_agent_config


def test_backward_compatibility():
    """Test that existing agents don't get energy adaptations."""
    
    print("=== Backward Compatibility Test ===\n")
    
    agent_factory = AgentFactory()
    
    # Test existing agent configurations
    existing_configs = [
        ("formal_technical_writer", "technical_writer"),
        ("casual_customer_support", "customer_support"),
        ("creative_collaborator", "creative_collaborator"),
        ("data_analyst", "data_analyst")
    ]
    
    all_passed = True
    
    for config_name, domain in existing_configs:
        print(f"Testing: {config_name}")
        
        # Load the actual config
        config_dict = load_agent_config(config_name)
        config = AgentConfig(**config_dict)
        
        # Test 1: Normal prompt (no energy)
        normal_prompt = agent_factory._build_system_prompt(config)
        has_adaptation_normal = "ENERGY ADAPTATION" in normal_prompt
        
        # Test 2: Prompt with energy (should be ignored for non-learning-partner)
        energy_prompt = agent_factory._build_system_prompt(config, "high")
        has_adaptation_energy = "ENERGY ADAPTATION" in energy_prompt
        
        # Test 3: Check that prompts are identical
        prompts_identical = normal_prompt == energy_prompt
        
        # Results
        no_adaptation = not has_adaptation_normal and not has_adaptation_energy
        consistent = prompts_identical
        
        print(f"  No energy adaptation: {'✅' if no_adaptation else '❌'}")
        print(f"  Consistent behavior: {'✅' if consistent else '❌'}")
        
        test_passed = no_adaptation and consistent
        all_passed = all_passed and test_passed
        
        print(f"  Result: {'✅ PASSED' if test_passed else '❌ FAILED'}")
        print("-" * 50)
    
    # Test context-aware learning partner
    print("Testing: context_aware_learning_partner")
    
    config_dict = load_agent_config("context_aware_learning_partner")
    config = AgentConfig(**config_dict)
    
    # Should have energy adaptation when enabled
    normal_prompt = agent_factory._build_system_prompt(config)
    energy_prompt = agent_factory._build_system_prompt(config, "high")
    
    no_adaptation_normal = "ENERGY ADAPTATION" not in normal_prompt
    has_adaptation_energy = "ENERGY ADAPTATION" in energy_prompt
    prompts_different = normal_prompt != energy_prompt
    
    print(f"  No adaptation without energy: {'✅' if no_adaptation_normal else '❌'}")
    print(f"  Has adaptation with energy: {'✅' if has_adaptation_energy else '❌'}")
    print(f"  Different prompts: {'✅' if prompts_different else '❌'}")
    
    context_test_passed = no_adaptation_normal and has_adaptation_energy and prompts_different
    print(f"  Result: {'✅ PASSED' if context_test_passed else '❌ FAILED'}")
    
    overall_passed = all_passed and context_test_passed
    
    print(f"\n=== SUMMARY ===")
    print(f"Existing agents: {'✅ No unwanted adaptations' if all_passed else '❌ Have adaptations'}")
    print(f"Context-aware agent: {'✅ Works correctly' if context_test_passed else '❌ Issues found'}")
    print(f"Overall: {'✅ BACKWARD COMPATIBLE' if overall_passed else '❌ COMPATIBILITY ISSUES'}")
    
    return overall_passed


if __name__ == "__main__":
    print("Testing backward compatibility (simplified)...")
    
    success = test_backward_compatibility()
    
    print(f"\n=== CHECKPOINT 3 FINAL STATUS ===")
    if success:
        print("✅ All tests passed!")
        print("✅ Backward compatibility maintained!")
        print("✅ Ready for final acceptance!")
    else:
        print("❌ Some tests failed!")
        print("❌ Needs investigation before acceptance!")