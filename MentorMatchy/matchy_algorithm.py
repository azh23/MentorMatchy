import psycopg2
import os
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

# Dictionary indicating at what position in a list of info a certain piece of info is.
s2n = {
    'FIRST_NAME' : 0,
    'LAST_NAME' : 1,
    'EMAIL_ADDRESS' : 2,
    'PRONOUNS' : 3,
    'ABOUT_ME' : 4,
    'INTERESTS' : 5,
    'INDUSTRY' : 6,
    'PHOTO_LINK' : 7,
    'MATCHING_ROLE' : 8,
    'WORK_STYLE' : 9,
    'FOCUS_STYLE' : 10,
    'SOLVE_PROBLEM_STYLE' : 11,
    'LEAD_STYLE' : 12,
    'EXPERIENCE' : 13,
    'IS_MATCHED' : 14,
    'MATCHED_EMAIL' : 15,
    'LOOKING_FOR' : 16
}

# Dictionary containing the importance values for each factor.
s_im = {
    'INDUSTRY': 5.0,
    'WORK_STYLE': 1.0,
    'FOCUS_STYLE': 1.0,
    'SOLVE_PROBLEM_STYLE': 1.0,
    'LEAD_STYLE' : 1.0,
    'EXPERIENCE' : 1.0
}

# How much important factors are multiplied. 
IMPORTANCE_MULT = 2.0
# The minimum score a 4th or 5th match needs to be returned. 
MIN_SCORE = 10.0

def _retrieve_potential_match_info(is_mentor: bool):
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM USERS WHERE MATCHING_ROLE = %s AND ISMATCHED IS FALSE',
                   ("Mentee",) if is_mentor else ("Mentor",))
    entries = cursor.fetchall()

    cursor.close()
    conn.close()
    return entries

def _get_matching_scores(user_info: list, candidate_info: list[list]) -> dict:
    factors = _get_important_factors(user_info[s2n['LOOKING_FOR']])
    scores = dict()

    for candidate in candidate_info:
        candidate_score = 0

        for factor in s_im.keys():
            if factor in ['INDUSTRY']:
                candidate_score += _get_discrete_factor_score(factor, factors, user_info, candidate)
            if factor in ['WORK_STYLE', 'FOCUS_STYLE', 'SOLVE_PROBLEM_STYLE', 'LEAD_STYLE', 'EXPERIENCE']:
                candidate_score += _get_quantitative_factor_score(factor, factors, user_info, candidate)

        scores[candidate[s2n['EMAIL_ADDRESS']]] = candidate_score

    return scores

def _get_discrete_factor_score(factor_str, important_factors, user_info, candidate):
    score = int(user_info[s2n[factor_str]] == candidate[s2n[factor_str]])
    if factor_str in important_factors:
        score *= IMPORTANCE_MULT
    score *= s_im[factor_str]
    return score

def _get_quantitative_factor_score(factor_str, important_factors, user_info, candidate):
    score = 5 - abs(candidate[s2n[factor_str]] - user_info[s2n[factor_str]])
    score /= 5

    if factor_str in important_factors:
        score *= IMPORTANCE_MULT
    score *= s_im[factor_str]
    return score

def _get_important_factors(factors: str):
    important_factors = []
    f = factors.split(',')
    #fkkkkk UPDATE LATER TO DEVELOPMENT im just testang
    if 'Professional Matching' in f:
        important_factors.append('INDUSTRY')
        important_factors.append('EXPERIENCE')
    # add more conditionals here once they finalize it
    return important_factors

def _get_top_scores(scores: dict):
    count_scores = Counter(scores)
    # Format of top_scores is [(email, score), ...]
    top_scores = count_scores.most_common(5)

    # Fourth and fifth candidates will only be returned if they meet the minimum score.
    if len(top_scores) == 5:
        if top_scores[3][1] < MIN_SCORE:
            del top_scores[3:5]
    elif len(top_scores) == 4:
        if top_scores[3][1] < MIN_SCORE:
            del top_scores[3]

    return top_scores
            

def return_match_emails(user_info: list, is_mentor: bool) -> list[str]: 
    entries = _retrieve_potential_match_info(is_mentor)
    scores = _get_matching_scores(user_info, entries)
    top_scores = _get_top_scores(scores)
    
    # Return a list of emails.
    return [info[0] for info in top_scores]





# Numerical scale of 1 to 10
# List of all your users and O(n^2) do double for loop and compare every user against one another and 
# then you calculate the absolute value differences between each personality value; do some summation of the differences; 
# one with least differences with each other is a better match