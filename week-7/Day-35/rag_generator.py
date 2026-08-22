def generate(
    self,
    query,
    documents
):

    prompt = self.build_prompt(
        query,
        documents
    )

    if prompt is None:

        return "I could not find relevant information in the provided documents."

    response = self.client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text