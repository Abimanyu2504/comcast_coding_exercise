from flask import Flask, request, jsonify
import string

app = Flask(__name__)

seen_strings = {}

def get_most_frequent_character(input_string):
    # Remove whitespace and punctuation from the input string
    clean_string = ''.join(char for char in input_string if char not in string.punctuation and not char.isspace())
    
    # Create a dictionary to count occurrences of each character
    char_count = {}
    for char in clean_string:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    
    # Find the character with the maximum occurrence
    if char_count:
        most_frequent_char = max(char_count, key=char_count.get)
        return most_frequent_char, char_count[most_frequent_char]
    else:
        return None, 0

@app.route('/stringinate', methods=['GET', 'POST'])
def stringinate():
    if request.method == 'POST':
        input_string = request.json.get('input', '')
    else:
        input_string = request.args.get('input', '')

    if input_string:
        # Update the dictionary with the input string count
        if input_string in seen_strings:
            seen_strings[input_string] += 1
        else:
            seen_strings[input_string] = 1

        # Calculate the most frequent character and its count
        most_frequent_char, frequency = get_most_frequent_character(input_string)

        return jsonify({
            "input": input_string,
            "length": len(input_string),
            "most_frequent_character": most_frequent_char,
            "frequency": frequency
        })
    else:
        return jsonify({"error": "Please provide an 'input' string."}), 400
