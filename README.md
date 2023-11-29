sls invoke local -f ask -d '{"queryParameters": {"question":"What is the capital of Sweden?"}}' --aws-profile default

# https://mermade.github.io/openapi-gui/#

I have a question about neo4j - how do I expand nodes in cypher?

<!--
title: 'AWS Simple HTTP Endpoint example in Python'
description: 'This template demonstrates how to make a simple HTTP API with Python running on AWS Lambda and API Gateway using the Serverless Framework.'
layout: Doc
framework: v3
platform: AWS
language: python
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->

# Serverless Framework Python HTTP API on AWS

This template demonstrates how to make a simple HTTP API with Python running on AWS Lambda and API Gateway using the Serverless Framework.

This template does not include any kind of persistence (database). For more advanced examples, check out the [serverless/examples repository](https://github.com/serverless/examples/)  which includes DynamoDB, Mongo, Fauna and other examples.

## Usage

### Deployment

```bash
serverless deploy --aws-profile default --stage prod
```

After deploying, you should see output similar to:

```bash
Running "serverless" from node_modules

Deploying aws-bedrock-stackoverflow-agent to stage prod (us-east-1)

✔ Service deployed to stack aws-bedrock-stackoverflow-agent-prod (88s)

endpoint: GET - https://926tifjrbe.execute-api.us-east-1.amazonaws.com/questions/{tag}
functions:
  so_questions: aws-bedrock-stackoverflow-agent-prod-so_questions (47 MB)
```

_Note_: In current form, after deployment, your API is public and can be invoked by anyone. For production deployments, you might want to configure an authorizer. For details on how to do that, refer to [http event docs](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/).

### Invocation

After successful deployment, you can call the created application via HTTP:

```bash
curl https://926tifjrbe.execute-api.us-east-1.amazonaws.com/questions/neo4j
```

Which should result in response similar to the following:

```json
{"messageVersion": "1.0", "response": {"actionGroup": "", "apiPath": "", "httpMethod": "GET", "httpStatusCode": 200, "responseBody": {"application/json": {"body": "{\"inputs\": \"{\\\"inputText\\\": \\\"no input text\\\", \\\"params\\\": \\\"\\\", \\\"bodyParams\\\": \\\"\\\"}\", \"message\": \"Top 3 questions for tag neo4j related to expand:\\n\\n,title,q.body_markdown,q.link,answers\\n0,Limit Neo4j apoc.path.expand by relationship property value,\\\"Is it possible in a weighted Neo4j graph to find all paths within n hops of a given node with the constraints that only the top m relationships (by weight) from each node are returned/further expanded? \\r\\n\\r\\nFor example, given the following graph:\\r\\n\\r\\n[![enter image description here][1]][1]\\r\\n\\r\\n\\r\\n  [1]: https://i.stack.imgur.com/N50IT.png\\r\\n\\r\\nThis query...
```

### Local development

You can invoke your function locally by using the following command:

```bash
sls invoke local -f so_questions --path test2.json
```

Which should result in response similar to the following:

```
{
    "messageVersion": "1.0",
    "response": {
        "actionGroup": "",
        "apiPath": "",
        "httpMethod": "GET",
        "httpStatusCode": 200,
        "responseBody": {
            "application/json": {
                "body": "{\"inputs\": \"{\\\"inputText\\\": \\\"no input text\\\", \\\"params\\\": \\\"\\\", \\\"bodyParams\\\": \\\"\\\"}\", \"message\": \"Top 3 questions for tag neo4j related to 
```

Alternatively, it is also possible to emulate API Gateway and Lambda locally by using `serverless-offline` plugin. In order to do that, execute the following command:

```bash
serverless plugin install -n serverless-offline
```

It will add the `serverless-offline` plugin to `devDependencies` in `package.json` file as well as will add it to `plugins` in `serverless.yml`.

After installation, you can start local emulation with:

```
serverless offline
```

To learn more about the capabilities of `serverless-offline`, please refer to its [GitHub repository](https://github.com/dherault/serverless-offline).

### Bundling dependencies

In case you would like to include 3rd party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```bash
serverless plugin install -n serverless-python-requirements
```

Running the above will automatically add `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and add it as a `devDependency` to `package.json` file. The `package.json` file will be automatically created if it doesn't exist beforehand. Now you will be able to add your dependencies to `requirements.txt` file (`Pipfile` and `pyproject.toml` is also supported but requires additional configuration) and they will be automatically injected to Lambda package during build process. For more details about the plugin's configuration, please refer to [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).
