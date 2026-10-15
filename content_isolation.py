
def extract_data(response):
    start_tag = "<data>"
    end_tag = "</data>"

    start_index = response.find(start_tag)
    end_index = response.find(end_tag)

    # Check whether both tags exist
    if start_index == -1 or end_index == -1:
        raise ValueError("Required XML boundary tags not found")

    # Check whether tags are in the correct order
    content_start = start_index + len(start_tag)

    if end_index < content_start:
        raise ValueError("Invalid XML boundary order")

    # Extract content between the tags
    extracted_content = response[content_start:end_index].strip()

    # Check whether extracted content is empty
    if not extracted_content:
        raise ValueError("Data section is empty")

    return extracted_content


# Test cases
test_cases = [
    (
        "Valid data",
        "Here is the result: <data>Name: Sudheer</data> Done."
    ),
    (
        "Missing opening tag",
        "Name: Sudheer</data>"
    ),
    (
        "Missing closing tag",
        "<data>Name: Sudheer"
    ),
    (
        "Empty data",
        "<data></data>"
    ),
    (
        "Incorrect tag order",
        "</data><data>Name: Sudheer"
    )
]

for test_name, response in test_cases:
    print(f"\nTest: {test_name}")

    try:
        result = extract_data(response)
        print("PASS:", result)

    except ValueError as error:
        print("HANDLED:", error)
