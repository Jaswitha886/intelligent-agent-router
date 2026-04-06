def retrieve_context():
    with open("data/knowledge_base.txt", "r") as file:
        return file.read()
