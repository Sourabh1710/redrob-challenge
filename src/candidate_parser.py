from src.jd_matcher import JDRequirements

def has_only_service_history(career_history):
    """
    Evaluates if a candidate's entire career has been spent solely at
    consulting/service companies. Returns True only if every job matches
    the JD blacklist.
    """
    if not career_history:
        return False
    
    total_jobs = len(career_history)
    service_jobs_count = 0

    for job in career_history:
        company_name = job.get("company","").lower().strip()

        is_service = False

        # Match company against blacklisted terms
        for blacklisted in JDRequirements.BLACKLISTED_COMPANIES:
            if blacklisted in company_name:
                is_service = True
                break
        if is_service:
            service_jobs_count +=1
    
    return service_jobs_count == total_jobs

def calculate_skill_score(skills_list):
    """
    Scores matched skills by multiplying proficiency weight with duration
    and endorsement modifiers to prevent keyword stuffing. 
    Nice-to-have skills are discounted by 50%.
    """
    proficiency_map = {
        "expert":1.0,
        "advanced":0.8,
        "intermediate":0.6,
        "beginner":0.3 
        }
    total_score = 0.0
    matched_skills = []

    for skill_dict in skills_list:
        skill_name = skill_dict.get("name","").lower().strip()
        
        if skill_name in JDRequirements.REQUIRED_SKILLS:
            prof = skill_dict.get("proficiency","beginner")
            duration = skill_dict.get("duration_months",0)
            endorsements = skill_dict.get("endorsements",0)

            prof_mult = proficiency_map.get(prof,0.3)
            duration_mult = 1.0 + (duration/12.0)
            endorsements_mult = 1.0 + (min(endorsements,100)/50.0) # Cap endorsements at 100 to prevent outliers

            skill_score = prof_mult * duration_mult * endorsements_mult
            total_score += skill_score
            matched_skills.append(skill_name)
        elif skill_name in JDRequirements.PREFERRED_SKILLS:
            prof = skill_dict.get("proficiency","beginner")
            duration = skill_dict.get("duration_months",0)
            endorsements = skill_dict.get("endorsements",0)

            prof_mult = proficiency_map.get(prof,0.3)
            duration_mult = 1.0 + (duration/12.0)
            endorsements_mult = 1.0 + (min(endorsements,100)/50.0) 

            skill_score = (prof_mult * duration_mult * endorsements_mult) * 0.5
            total_score += skill_score
            matched_skills.append(skill_name)
    
    return round(total_score, 2), matched_skills 

def calculate_experience_score(years_of_experience):
    if years_of_experience is None:
        return 0.0
    
    if 6.0 <= years_of_experience <= 8.0:
        return 1.0
    elif 5.0 <= years_of_experience <= 9.0:
        return 0.8
    elif 4.0 <= years_of_experience <= 12.0:
        return 0.5
    else:
        return 0.1
