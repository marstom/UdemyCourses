from graphql_schema import schema
from icecream import ic, install

query = """
{
  notes (filters: {
    titleContains: "egg"
  }) {
    title
    content
    created
    due
    contentShort
    
  }
}
"""

# query_mutation = """
# mutation {
#   createNote {
#     success
#   }
# }
# """
query_mutation = """
mutation {
  createNote(title: "New Note", content: "New Content") {
    success
  }
}
"""


def main():
    result = schema.execute(query_mutation)
    ic(result.data)
    ic(result.errors)
    # for e in result:
    #     ic(e)


if __name__ == "__main__":
    install()
    main()

    # Skoczyłem na 4.5 point
