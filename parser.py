import re

def parse_query(text):
    """
    Extracts product details from a natural language query.
    """
    text = text.lower()
    details = {}

    # A list of common colors to search for
    colors = ['red', 'blue', 'black', 'white', 'silver', 'gold', 'pink', 'green', 'grey', 'purple', 'brown']
    
    # 1. Extract budget
    # Added optional space before ₹ and more flexible keywords
    budget_match = re.search(r'(?:under|below|max|for|in|less than)\s*₹?\s*(\d+)', text)
    if budget_match:
        try:
            details['budget'] = int(budget_match.group(1))
        except ValueError: # Specific error for int conversion
            details['budget'] = 99999  # default in case conversion fails
        # Remove the budget part from the text to not confuse the product parser
        text = text.replace(budget_match.group(0), '')

    # 2. Extract color
    details['color'] = '' # Default to empty string if no color found
    for color in colors:
        if color in text:
            details['color'] = color
            text = text.replace(color, '')  # Remove color from text
            break

    # 3. What's left is likely the product description
    # CORRECTED LINE: Use word boundaries (\b) to match whole words only.
    product_text = re.sub(r'\b(i want|a|an|buy|get|me|find|looking for|some|of)\b', '', text).strip()
    details['product'] = ' '.join(product_text.split())

    # Ensure product is not empty, set a default if necessary or handle it in app.py
    if not details['product']:
        details['product'] = 'item' # Default product if nothing specific is found

    # Set default budget if not found in query
    if 'budget' not in details:
        details['budget'] = 99999 # Default high budget

    return details