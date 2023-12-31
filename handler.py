import json

from neo4j import GraphDatabase
from aws_lambda_powertools.logging.logger import Logger

logger = Logger()


@logger.inject_lambda_context
def so_questions(event, context):
    input_text = event.get('inputText', 'no input text')
    params = ",".join([str(p['name']) + ":" + str(p['value']) for p in event.get('parameters', [])])

    body = event.get('requestBody', {}).get('content', {}).get('application/json', {}).get('properties', [])
    body = ",".join([str(p['name']) + ":" + str(p['value']) for p in body])

    tag = 'neo4j'  # event['pathParameters']['tag'] or 'neo4j'
    search = 'expand'  # event['queryParameters']['search'] or 'expand'
    database = 'stackoverflow2'
    limit = 3
    database_uri = 'neo4j+s://demo.neo4jlabs.com'

    query = '''
        MATCH (t:Tag {name: $tag})
        MATCH (q:Question)-[:TAGGED]->(t)
        WHERE toLower(q.title) CONTAINS $search 
        CALL { with q
            MATCH (a)-[:ANSWERED]->(q)
            RETURN apoc.text.join(collect(a.body_markdown)[0..3], "\n\n") as answers
        }
        RETURN q.title as title, q.body_markdown, q.link, answers
        ORDER BY q.view_count DESC
        LIMIT $limit
    '''

    with GraphDatabase.driver(database_uri, auth=(database, database)) as driver:
        with driver.session(database=database) as session:
            data = session.run(query, search=search, tag=tag, limit=limit)
            csv_string = data.to_df().to_csv()

    body = {
        'inputs': json.dumps({'inputText': input_text, 'params': params, 'bodyParams': body}),
        'message': 'Top ' + str(limit) + ' questions for tag ' + tag + ' related to ' + search + ":\n\n" + csv_string,
        'input': event,
    }
    response = {
        'messageVersion': '1.0',
        'response': {
            'actionGroup': event.get('actionGroup', ''),
            'apiPath': event.get('apiPath', ''),
            'httpMethod': event.get('httpMethod', 'GET'),
            'httpStatusCode': 200,
            'responseBody': {
                'application/json': {
                    'body': json.dumps(body)
                }
            }
        }
    }

    logger.info('Response: {0}'.format(response))
    return response
