from graphql_schema import schema
from icecream import ic, install


def print_results(result):
    ic(result.data)
    ic(result.errors)

def test_query():
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
    result = schema.execute(query)
    ic(result.data)
    ic(result.errors)

def test_mutation():
    query_mutation = """
    mutation {
      createNote(title: "New Note", content: "New Content") {
        success
      }
    }
    """
    result = schema.execute(query_mutation)
    print_results(result)

    result = schema.execute("""
    {
        notes{
            title
            content
        
        }
    
    }
    
    """)
    print_results(result)



