from graphql_schema import schema
from icecream import ic


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
      createNote(title: "New Note", content: "New Content", due: "2029-10-20T00:00:00") {
        success
        note {
          title
          content
          due
        }
      }
    }
    """
    ic("--mutation--")
    result = schema.execute(query_mutation)
    print_results(result)

    ic("--query--")
    result = schema.execute("""
    {
        notes{
            title
            content
        
        }
    
    }
    
    """)
    print_results(result)


def test_handle_error():
    query_mutation = """
    mutation {
      createNote(subject: "New Note", content: 42) {
        successik
        note {
          title
          content
        }
      }
    }
    """
    ic("--mutation--")
    result = schema.execute(query_mutation)
    print_results(result)


def test_error_date():
    query_mutation = """
    mutation {
      createNote(title: "New Note", content: "My", due: "2023-10-20T00:00:00") {
        success
        note {
          title
          content
        }
      }
    }
    """
    ic("--mutation--")
    result = schema.execute(query_mutation)
    print_results(result)
