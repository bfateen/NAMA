          const { S3Client, PutObjectCommand } = require("@aws-sdk/client-s3");
          const { SNSClient, PublishCommand } = require("@aws-sdk/client-sns");

          const s3Client = new S3Client();
          const snsClient = new SNSClient();

          function parseMultipartFormData(body, boundary) {
            console.log('Parsing multipart form data...');
            console.log('Boundary:', boundary);
            const parts = body.split(boundary);
            const result = {};
            for (const part of parts) {
              const contentDispositionMatch = part.match(/Content-Disposition:\s*form-data;\s*name="([^"]+)"(?:;\s*filename="([^"]+)")?/i);
              if (contentDispositionMatch) {
                const name = contentDispositionMatch[1];
                const filename = contentDispositionMatch[2];
                const contentTypeMatch = part.match(/Content-Type:\s*(.+)/i);
                const contentType = contentTypeMatch ? contentTypeMatch[1].trim() : null;
                const content = part.split(/\r\n\r\n|\n\n/).slice(1).join('\n\n').trim();
                result[name] = { content, contentType, filename };
                console.log(`Parsed part: ${name}`);
                console.log(`Content Type: ${contentType}`);
                console.log(`Filename: ${filename}`);
                console.log(`Content length: ${content.length}`);
              }
            }
            return result;
          }

          exports.handler = async (event) => {
            console.log('Received event:', JSON.stringify(event, null, 2));
            
            try {
              const contentType = event.headers['content-type'] || event.headers['Content-Type'];
              if (!contentType) {
                throw new Error('Content-Type header is missing');
              }
              console.log('Content-Type:', contentType);

              const boundaryMatch = contentType.match(/boundary=(?:"([^"]+)"|([^;]+))/i);
              if (!boundaryMatch) {
                throw new Error('Boundary not found in Content-Type header');
              }
              const boundary = boundaryMatch[1] || boundaryMatch[2];
              console.log('Boundary:', boundary);
              
              let parsedBody;
              if (event.isBase64Encoded) {
                console.log('Event body is base64 encoded. Decoding...');
                const decodedBody = Buffer.from(event.body, 'base64').toString('utf-8');
                parsedBody = parseMultipartFormData(decodedBody, boundary);
              } else {
                console.log('Event body is not base64 encoded.');
                parsedBody = parseMultipartFormData(event.body, boundary);
              }
              
              console.log('Parsed body:', JSON.stringify(parsedBody, null, 2));
              
              const { email, file } = parsedBody;
              
              if (!email || !file) {
                throw new Error('Missing required fields in request body');
              }

              if (!file.filename) {
                throw new Error('Filename not found in file data');
              }

              const bucketName = process.env.S3_BUCKET_NAME;
              const topicArn = process.env.SNS_TOPIC_ARN;

              console.log('Bucket Name:', bucketName);
              console.log('SNS Topic ARN:', topicArn);

              const fileContent = Buffer.from(file.content, 'binary');
              const fileName = file.filename;
              console.log('Filename:', fileName);

              const params = {
                Bucket: bucketName,
                Key: `uploads/${Date.now()}-${fileName}`,
                Body: fileContent,
                ContentType: file.contentType,
              };

              console.log('Uploading to S3...');
              const uploadCommand = new PutObjectCommand(params);
              const uploadResult = await s3Client.send(uploadCommand);
              console.log('S3 upload result:', uploadResult);
              
              const fileLocation = `https://${bucketName}.s3.amazonaws.com/${params.Key}`;
              
              console.log('Publishing to SNS...');
              const publishCommand = new PublishCommand({
                TopicArn: topicArn,
                Subject: 'New File Upload',
                Message: `A new file has been uploaded.\nUploader's email: ${email.content}\nFile location: ${fileLocation}`,
              });
              await snsClient.send(publishCommand);
              console.log('SNS publish complete');

              return {
                statusCode: 200,
                headers: {
                  'Access-Control-Allow-Origin': '*',
                  'Access-Control-Allow-Credentials': true,
                },
                body: JSON.stringify({ message: 'File uploaded successfully' }),
              };
            } catch (error) {
              console.error('Error:', error);
              return {
                statusCode: 500,
                headers: {
                  'Access-Control-Allow-Origin': '*',
                  'Access-Control-Allow-Credentials': true,
                },
                body: JSON.stringify({ message: 'Error uploading file', error: error.message, stack: error.stack }),
              };
            }
          };