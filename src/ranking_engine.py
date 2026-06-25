from src.candidate_parser import (
    has_only_service_history, 
    calculate_experience_score,
    calculate_skill_score
    )


def calculate_behavioral_multiplier(signals_dict):
    """
    Computes a multiplier (0.5 to 1.3) based on platform engagement metrics
    like response rate, active status, and market demand.
    """
    if not signals_dict:
        return 1.0
            
    modifier = 0.0
    
    # Check response rate: reward highly responsive, penalize unresponsive
    response_rate = signals_dict.get("recruiter_response_rate", 0.5)
    if response_rate >= 0.70:
        modifier += 0.15
    elif response_rate < 0.25:
        modifier -= 0.30

    # Reward active job seekers    
    open_to_work = signals_dict.get("open_to_work_flag", False)
    if open_to_work:
        modifier += 0.10
    
    # Check profile views to gauge active recruiter demand
    views = signals_dict.get("profile_views_received_30d", 0)
    if views > 20:
        modifier += 0.05
        
    multiplier = 1.0 + modifier
    return round(max(0.5, min(multiplier, 1.3)), 2)

def calculate_composite_score(candidate_data):
    """
    Main orchestration logic. Excludes pure-service candidates,
    normalizes technical skills, weights the profile (70% skills, 30% exp),
    and scales the result with the behavioral multiplier.
    """
    
    profile = candidate_data.get("profile", {})
    career_history = candidate_data.get("career_history", [])
    skills_list = candidate_data.get("skills", [])
    signals = candidate_data.get("redrob_signals", {})
    
    if has_only_service_history(career_history):
        return 0.0, "Disqualified: Only has consulting/service company history."
        
    skill_score, matched_skills = calculate_skill_score(skills_list)
    years_exp = profile.get("years_of_experience", 0.0)
    exp_score = calculate_experience_score(years_exp)
    
    normalized_skill_score = min(skill_score / 15.0, 1.0)
    
    base_profile_score = (0.7 * normalized_skill_score) + (0.3 * exp_score)
    
    behavioral_mult = calculate_behavioral_multiplier(signals)
    final_score = base_profile_score * behavioral_mult
    
    reasoning = (
        f"{profile.get('current_title', 'Engineer')} with {years_exp} yrs experience; "
        f"{len(matched_skills)} matched AI skills (Score: {skill_score}); "
        f"response rate {signals.get('recruiter_response_rate', 0.0)}."
    )
    
    return round(final_score, 4), reasoning