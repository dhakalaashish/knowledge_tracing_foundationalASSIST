import pandas as pd

def add_pi_if_missing(input_string):
    # Check if "se 3.14 for" is in the input string
    if "se 3.14 for" in input_string:
        # Check if "pi" is not already present after "se 3.14 for"
        if "pi" not in input_string[input_string.index("se 3.14 for") + len("se 3.14 for"):]:
            return input_string[:input_string.index("se 3.14 for") + len("se 3.14 for")] + " pi" + input_string[input_string.index("se 3.14 for") + len("se 3.14 for"):]
    return input_string

def convert_mathml_to_fraction(mathml_content):
    mathml_content = mathml_content.replace('<ast-r type="text" marker="1">', "___")
    mathml_content = mathml_content.replace('<mfrac>', '(')
    mathml_content = mathml_content.replace('</mfrac>', ')')
    mathml_content = mathml_content.replace('</mn><mn>', '/')
    mathml_content = mathml_content.replace('<mn>', '')
    mathml_content = mathml_content.replace('</mn>', '')
    mathml_content = mathml_content.replace('<mi>', '')
    mathml_content = mathml_content.replace('</mi>', '')
    mathml_content = mathml_content.replace('<mo>', '')
    mathml_content = mathml_content.replace('</mo>', '')
    mathml_content = mathml_content.replace('<mn>', '')
    mathml_content = mathml_content.replace('</mn>', '')
    mathml_content = mathml_content.replace('<math>', '')
    mathml_content = mathml_content.replace('</math>', '')
    mathml_content = mathml_content.replace('<mi mathvariant=¨normal¨>§#960;', '')
    mathml_content = mathml_content.replace('&nbsp;', ' ')
    mathml_content = mathml_content.replace('§#160;', ' ')
    mathml_content = mathml_content.replace('&gt;', '>')
    mathml_content = mathml_content.replace('&lt;', '<')
    mathml_content = mathml_content.replace('&amp;', '&')
    
    mathml_content = mathml_content.replace('«/math', '')

    mathml_content = mathml_content.rstrip('/')
    
    return mathml_content


from bs4 import BeautifulSoup
def alt_text(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    
    # Replace each <img> with its alt text if it exists
    for img in soup.find_all('img'):
        alt = img.get('alt')
        if alt:
            img.replace_with(alt)
    
    return str(soup)

def mathml_to_text(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Convert MathML fractions
    for math in soup.find_all('math'):
        frac = math.find('mfrac')
        if frac:
            nums = frac.find_all('mn')
            if len(nums) == 2:
                numerator = nums[0].text
                denominator = nums[1].text
                frac_text = f"{numerator}/{denominator}"
                math.replace_with(frac_text)
            else:
                math.replace_with(math.get_text())  # Fallback if not a valid mfrac
        else:
            math.replace_with(math.get_text())  # Handle non-fraction math

    # Return clean text
    return soup.get_text(separator=" ", strip=True)


def clean_text(input_text):
    if pd.isna(input_text) or input_text.strip() == "":
        return ""

    # Replace &nbsp; and decode HTML entities
    input_text = input_text.replace('&nbsp;', ' ')
    
    # Replace <img> tags with their alt text
    input_text = mathml_to_text(input_text)
    input_text = alt_text(input_text)

    # Convert MathML if it exists
    soup = BeautifulSoup(input_text, 'html.parser')
    for img in soup.find_all('img', class_='Wirisformula'):
        mathml_formula = img.get('data-mathml')
        if mathml_formula:
            # Extract inner MathML content
            start_index = mathml_formula.find('<math>') + len('<math>')
            end_index = mathml_formula.find('</math>')
            mathml_formula_content = mathml_formula[start_index:end_index]
            mathml_formula_content_cleaned = mathml_formula_content.replace(
                'xmlns=¨http://www.w3.org/1998/Math/MathML¨»', '')
            fraction = convert_mathml_to_fraction(mathml_formula_content_cleaned)
            img.replace_with(fraction)

    text = soup.get_text(separator=' ', strip=True)
    text = convert_mathml_to_fraction(text)
    text = add_pi_if_missing(text)
    return text