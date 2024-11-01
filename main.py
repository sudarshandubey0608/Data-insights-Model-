from app import TextChatInterface

# Initialize the chat interface
chat_interface = TextChatInterface()

@app.route('/search', methods=['POST'])
def search():
    # Get the query from the request body
    query = request.json.get('query')

    # Encode the query using the tokenizer
    inputs = tokenizer(query, return_tensors='pt')

    # Generate a response based on the query
    outputs = chat_interface.search(inputs)

    return jsonify(outputs)

from app import TextChatInterface

# Initialize the chat interface
chat_interface = TextChatInterface()

@app.route('/chat', methods=['POST'])
def chat():
    # Get the query from the request body
    query = request.json.get('query')

    # Encode the query using the tokenizer
    inputs = {'input_ids': [tokenizer.encode_plus(query, return_tensors='pt')], 'attention_mask': [torch.tensor([1])], 'labels': [None]}

    # Generate a response based on the query and text chat interface
    output = chat_interface.search(inputs)

    return jsonify(output)
