from rag_generator import RAGGenerator
from models import Document


documents = [

    Document(
        id="1",
        content="Employees receive 12 casual leaves every year.",
        metadata={
            "source":"HR Policy",
            "page":5
        }
    ),

    Document(
        id="2",
        content="Work from home is allowed for two days every week.",
        metadata={
            "source":"HR Policy",
            "page":8
        }
    )

]

generator = RAGGenerator()

print(
    generator.generate(
        query="How many casual leaves are allowed?",
        documents=documents
    )
)