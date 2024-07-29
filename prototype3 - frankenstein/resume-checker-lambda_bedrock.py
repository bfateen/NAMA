          import json
          import boto3

          def lambda_handler(event, context):
              try:
                  body = json.loads(event['body'])
                  resume_text = body['resume_text']
              except (KeyError, json.JSONDecodeError):
                  return {
                      'statusCode': 400,
                      'body': json.dumps('Invalid request: resume_text not found in POST body')
                  }

              client = boto3.client("bedrock-runtime")
              
              prompt = f"\n\nHuman:You are an experienced technical recruiter in a software company. Review the following resume text and assign a percent relevancy score for the role of 'Android Developer' and explain why or why not they are qualified. The resume text: {resume_text}\n\nAssistant:"

              body = {
                  "prompt": prompt,
                  "max_tokens_to_sample": 200,
                  "temperature": 0.5,
                  "stop_sequences": ["\n\nHuman:"],
              }
              
              try:
                  resp = client.invoke_model(modelId="anthropic.claude-instant-v1", body=json.dumps(body))
                  response_body = json.loads(resp["body"].read())
                  completion = response_body["completion"]
                  
                  return {
                      'statusCode': 200,
                      'headers': {
                          'Access-Control-Allow-Origin': '*',
                          'Access-Control-Allow-Headers': 'Content-Type',
                          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                      },
                      'body': json.dumps({'response': completion})
                  }
              except Exception as e:
                  return {
                      'statusCode': 500,
                      'body': json.dumps(f'Error: {str(e)}')
                  }