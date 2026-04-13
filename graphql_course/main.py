from graphql_schema import schema
from icecream import ic, install

query = """
{
  notes {
    title
    content
    created
    due
    
  }
}
"""
def main():
    result = schema.execute(query)
    ic(result.data)
    ic(result.errors)
    # for e in result:
    #     ic(e)


if __name__ == "__main__":
    install()
    main()
