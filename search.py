import re
from db import collection
from typing import Optional

# Function to extract relevant search terms from the user input
def extract_key_terms(query: str):
    """
    Extracts potential key terms like bill_no, job_no, container_no from the user query.
    This ensures better matches even when the query has extra words.
    """
    # Extract words and numbers from the query
    words = re.findall(r"[A-Za-z0-9/-]+", query)

    # If the query contains a likely reference number, return it
    for word in words:
        if "/" in word or "-" in word or word.isnumeric():
            return word  # Assume this is the main reference number

    return query


def search_by_query(user_query: str) -> Optional[dict]:
    """
    Enhanced search function with better exact matching capabilities
    """
    # Normalize the query - trim whitespace and convert to uppercase
    normalized_query = user_query.strip().upper()
    
    # Extract key terms (removes unnecessary words from the query)
    key_term = extract_key_terms(normalized_query)
    
    # Step 1: Try exact matching with case normalization
    exact_query = {
        "$or": [
            {"job_no": key_term},
            {"awb_bl_no": key_term},
            {"bill_no": key_term},
            {"container_nos.container_number": key_term}
        ]
    }
    
    # result = collection.find_one(exact_query, projection)
    result = collection.find_one(exact_query)

    if result:
        return result
    
    # Step 1.5: Try exact match case-insensitive
    case_insensitive_query = {
        "$or": [
            {"job_no": {"$regex": f"^{re.escape(key_term)}$", "$options": "i"}},
            {"awb_bl_no": {"$regex": f"^{re.escape(key_term)}$", "$options": "i"}},
            {"bill_no": {"$regex": f"^{re.escape(key_term)}$", "$options": "i"}},
            {"container_nos.container_number": {"$regex": f"^{re.escape(key_term)}$", "$options": "i"}}
        ]
    }
    
    # result = collection.find_one(case_insensitive_query, projection)
    result = collection.find_one(case_insensitive_query)

    if result:
        return result
    
    
    # Step 3: Check for embedded numbers and search those
    extracted_numbers = re.findall(r"\b\d+\b", key_term)
    for num in extracted_numbers:
        if len(num) >= 3:  # Filter out very short numbers to avoid false positives
            number_query = {
                "$or": [
                    {"job_no": num},
                    {"awb_bl_no": num},
                    {"bill_no": {"$regex": f"{re.escape(num)}", "$options": "i"}},
                    {"container_nos.container_number": {"$regex": f"{re.escape(num)}", "$options": "i"}}
                ]
            }
            
            # result = collection.find_one(number_query, projection)
            result = collection.find_one(number_query)
            if result:
                return result

    
    # Step 4: Perform full-text search as a last fallback
    text_query = {"$text": {"$search": key_term}}
    
    cursor = (
        # collection.find(text_query, projection)
        collection.find(text_query)
        .limit(5)
        .allow_disk_use(True)
        .sort("score", {"$meta": "textScore"})
    )
    
    return next(cursor, None) if cursor else None