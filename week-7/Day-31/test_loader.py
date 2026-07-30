from document_loader import DocumentLoader


loader = DocumentLoader()


files = [
    "sample.pdf",
    "sample.docx",
    "sample.txt"
]


for file in files:

    print("=" * 60)

    print("Loading:", file)

    try:

        documents = loader.load(file)

        for index, document in enumerate(documents, start=1):

            print(f"\nDocument {index}")

            print("\nMetadata:")

            for key, value in document.metadata.items():

                print(f"{key}: {value}")

            print("\nContent Preview:")

            print(document.content[:300])

            print()

    except Exception as error:

        print(error)