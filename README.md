# AsyncLLMInferenceAWS
In this project, I have created an async inference in SageMaker that queues incoming requests and processes them asynchronously.

<img width="485" alt="image" src="https://github.com/Cenrax/AsyncLLMInferenceAWS/assets/43017632/fbcc3313-2ad3-443f-92c4-6fd5ab0cbe0a">

 The primary components and their interconnections are as follows:

1. **User**: The end-user interacts with the system by sending inference requests to the SageMaker asynchronous endpoint. Once the inference is complete, they receive the results either directly or through a notification system.

2. **Async Endpoint**: This is the entry point for inference requests from the user. The endpoint is managed by Amazon SageMaker and is designed to handle incoming requests asynchronously. When a request is received, it is placed in a queue for processing.

3. **Queue**: The queue acts as a buffer to manage the flow of inference requests to the inference infrastructure. It ensures that the system can handle bursts of requests without overloading the compute resources.

4. **Inference Infrastructure**: Within the inference infrastructure, there are multiple instances labeled as "Mistral Instance." These are the Amazon SageMaker compute instances provisioned for running the machine learning model. These instances pull inference requests from the queue and process them independently, thus allowing for parallel processing and scalable performance. I have configured the endpoints to be auto-scalable

5. **S3 Storage for Model Artifacts**: Amazon S3 is used to store the machine learning model artifacts. Each Mistral Instance fetches the model it needs to perform inference from this centralized storage. This ensures that the most up-to-date model is used across all instances.

6. **Success and Error Notifications**: The system is designed to notify the end-user of the success or failure of their inference requests. These notifications are managed by Amazon Simple Notification Service (SNS) and are configured to send messages to predefined topics. Users can subscribe to these topics to receive real-time updates on their requests.

The workflow typically follows these steps:
- The user sends an inference request to the async endpoint.
- The request is queued in the SageMaker managed queue.
- A Mistral Instance retrieves the request from the queue and processes it.
- The Mistral Instance fetches the required model artifacts from the S3 storage.
- After processing the request, the Mistral Instance outputs the results.
- The results are stored in an S3 bucket, and a notification regarding the success or failure of the inference is sent to the user via SNS.
