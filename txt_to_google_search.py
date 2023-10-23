import webbrowser

# Define the text file path
file_path = "C:\\Users\\PATH\\file_name.txt"

try:
    with open(file_path, "r", encoding='utf-8') as file:
        # Read the file line by line
        lines = file.readlines()

        # Initialize a variable to store the concatenated search terms
        concatenated_search = ""

        # Iterate through the lines with a step of n
        n = 4
        for i in range(0, len(lines), n):
            # Extract and concatenate the search terms from all four lines
            concatenated_search = "".join(lines[i:i+n]).strip()

            # Open a Chrome tab with the concatenated search terms
            search_url = f"https://www.google.com/search?q={concatenated_search}"
            webbrowser.open_new_tab(search_url)

except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
