# 👀 Customer-Engagement-Platform

> **User Engagement:**
> 
> - What is the average session duration?
> - How many sessions occur per day/week/month?
> - What is the frequency of user interactions within a session (e.g., clicks, swipes, taps)?
> - What is the average time between sessions for a user?
> 1. **Conversion and Retention:**
>     - What is the conversion rate from app install to first purchase?
>     - What is the retention rate over time (e.g., daily, weekly, monthly retention)?
>     - How many users make repeat purchases within a given timeframe?
>     - What is the churn rate (i.e., the percentage of users who stop using the app)?
> 2. **Content and Feature Usage:**
>     - Which app features or pages are most frequently accessed by users?
>     - What type of content (e.g., order history, banners) do users engage with the most?
>     - Are there any specific features or content types that lead to higher user engagement or retention?
> 3. **User Segmentation:**
>     - How do user behaviors vary across different demographics (e.g., age, gender, location)?
>     - Are there any distinct user segments with unique behavior patterns or preferences?
> 4. **Performance and Technical Metrics:**
>     - How frequently do app crashes or errors occur, and what are the common causes?
>     - What is the distribution of device types and operating systems among users?
> 5. **Funnel Analysis:**
>     - What is the conversion rate at each stage of the user journey (e.g., from browsing to adding items to cart to completing a purchase)?
>     - Where do users drop off the most in the conversion funnel, and what are possible reasons for drop-offs?
>     - Are there any specific paths or sequences of actions that lead to higher conversion rates?
> 6. **Session Analysis**
>     - What is the average session length for today?
>     - Which is the most common landing page ?
>     - What is the %of sessions ended in purchase?
>     - Compare user journeys through graphical representation and much more?

## **Objective**

The objective of the Customer Engagement Platform is to provide businesses with comprehensive insights into user behavior, enabling targeted messaging, real-time interactions, and campaign automation based on specific customer behaviors. Through live segmentation and dynamic triggers, businesses can enhance user engagement, drive conversions, and optimize app performance effectively.

---

# 💭 Proposed Solution

<aside>
💡 The most important task here is to built our data infrastructure in such a way that it enables us to derive 100’s and 1000’s of such features in real-time with high availability, scalability and accuracy.

</aside>

> HOW ARE WE DEALING WITH DATA?
> 

Data for our system are user generated events (app launch, add to cart, etc.) Events helps us determine user activity on the application UI 

### EVENTS

https://whimsical.com/BEJVbcwHhCnK3sx58Wvpqt@2bsEvpTYSt1HitqdiVE2LCWrS6EQXUCvvnL

<aside>
💡 Events are the core of this project. All events should have an **Event Name**, a **Timestamp** of when that event has occurred, and a **Distinct ID** (Project’s identifier for a user) to tie all events belonging to the same user. Events can optionally have a set of properties, which describes the event in more detail.

</aside>

### **More on events**

- **Event Types**
    
    `“event_category”`helps us to identify and segment data, right at source in order to enable users to perform analysis at granular levels. 
    
    Example of a few events and their categories to be tracked.
    
    1. **User Actions:**
        - **Login:** User authentication and login events.
        - **Sign-up:** New user registration and account creation.
        - **Search:** User searches for groceries or specific items within the app.
        - **Add to Cart:** User adds items to their shopping cart.
        - **Remove from Cart:** User removes items from their shopping cart.
        - **View Product Details:** User views detailed information about a specific product.
        - **Place Order:** User places an order for groceries.
        - **Cancel Order:** User cancels an existing order before delivery.
        - **Modify Order:** User modifies the contents of their current order.
        - **View Order History:** User views their past order history.
    2. **Delivery and Fulfillment:**
        - **Delivery Confirmation:** User confirms receipt of delivered groceries.
        - **Delivery Tracking:** User tracks the status and location of their delivery.
        - **Delivery Delay:** Notification of delivery delays or changes in delivery schedule.
        - **Out of Stock Notification:** User receives notifications for out-of-stock items in their order.
        - **Substitution Confirmation:** User confirms or rejects substitutions for out-of-stock items.
    3. **System Events:**
        - **App Launch:** User opens the app.
        - **App Close:** User closes the app.
        - **App Update:** User updates the app to the latest version.
        - **App Crashes:** Recording instances of app crashes or errors.
        - **Network Connectivity:** Notifications of network connectivity status (e.g., offline, online).
        - **Push Notifications:** User interaction with push notifications (e.g., opens, dismissals).
        - **App Permissions:** User grants or revokes permissions required by the app (e.g., location, notifications).
    4. **User Engagement:**
        - **Feedback Submission:** User submits feedback or ratings for the app or service.
        - **Customer Support Interaction:** User initiates or responds to customer support inquiries.
        - **Promotions and Discounts:** User engages with promotional offers, discounts, or loyalty programs.
    5. **Analytics and Monitoring:**
        - **Event Tracking:** Recording of custom events for analytics purposes (e.g., user engagement metrics, conversion rates).
        - **Performance Metrics:** Monitoring of app performance metrics (e.g., response times, latency).
        - **Error Logging:** Capture of errors or exceptions encountered within the app for debugging and troubleshooting.
    6. **Custom Events:**
        - Custom events set by end user.
    
- **High level requirements**
    - Each event must be properly formatted JSON.
    - Each event must contain an event_id, time, distinct_id, and insert_id. These are used to deduplicate events, so that this endpoint can be safely retried.
    - Each event must be smaller than 1MB of uncompressed JSON.
- **Default Properties**
    
    
    | property name | description |
    | --- | --- |
    | `event_id` | A unique id that clearly describes the event. |
    | `event_category` | A unique category assigned to the event. |
    | `time` | A unix time epoch that is used to determine the time of an event. Unix timestamp in milliseconds. |
    | `distinct_user_id` | A unique business key that determines user through out all databases and unique id to identify user generating the event. (ph number)
    **Which users spend most time on the app?
    How users are navigating through the app?
    What is the user’s most common ordered item?** |
    | `session_id` | A session_id capturing user sessions. The session starts when the user performs the starting event and ends when the user performs the ending event or based on some timeout.
    **How much time do users spend on my site per session?
    What are the average number of pages visited per session?
    Which page is the most common landing page for a session?
    What % of sessions end with a Purchase?** |
    | `device_id` | When user does not login and `distinct_user_id` could not be fetched and is not defined (default value) for an user, then device_id will be considered as unique identification until the user is identified. |
    | `insert_id` | A unique identifier for each event logged in the system, helps in de-duplication and also to rollback and de-bug. |
    | `source_id` | A unique id to identify the source that produced the event could be services, or partners |
    | `ip`  | geo coding user location data from ip for data enrichment( if gps is allowed, then we can use their exact lats and langs)
    Here's a couple with simple calls...
    `- http://ipinfodb.com/ip_query.php
    - http://freegeoip.appspot.com/`
    Example calls :-
    - http://freegeoip.appspot.com/xml/122.169.8.137
    - http://ipinfodb.com/ip_query.php?ip=122.169.8.137
    
    map with default if null
    
    Example of returned XML (ipinfodb) :-
    `<Response>
    <Ip>122.169.8.137</Ip>
    <Status>OK</Status>
    <CountryCode>IN</CountryCode>
    <CountryName>India</CountryName>
    <RegionCode>10</RegionCode>
    <RegionName>Haryana</RegionName>
    <City>Kaul</City>
    <ZipPostalCode></ZipPostalCode>
    <Latitude>29.85</Latitude>
    <Longitude>76.6667</Longitude>
    </Response>`
    
    **What are different locations, our users belong to?
    Which locations are having the least volume of orders?
    Which are the top selling products based on locations?** |
    | `URL` | URL of the page user generated the event from. e.g.
    `moreretail.com/signup`
    
    **Which page has the highest user drop off rate?
    Which page has highest user interactions?
    How are users moving in the app?** |
- **Custom properties**
    - users can add custom properties
    - `item` and `amount` are additional custom properties added to the event Purchase
    
    ```json
    {
    	"event_id": "Purchase", 
    	"default_properties":	{
    		"time": 1618716477000,
    		"distinct_id": "91304156-cafc-4673-a237-623d1129c801",
    		"$insert_id": "935d87b1-00cd-41b7-be34-b9d98dd08b42",
    	},
    	"custom_properties": {
    		"item": "Coffee", 
    		"amount": 5.0
      }
    }
    ```
    
- **Events Schema**
    - Schema registry : Events schema can be maintained and registered at **AWS Glue Schema Registry** in JSON format.
    - Maintaining schema helps in faster data validation and serves as one source of truth for all events (custom events defined by end user as well as pre-defined events).AWS Glue Schema Registry
    
    [Getting started with Schema Registry - AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/schema-registry-gs.html)
    
    ```json
    {
      "event_name": "Signed up",
      "event_category": "User Actions",
      "default_properties": {
        "time": 1618716477000,
        "distinct_user_id": "91304156-cafc-4673-a237-623d1129c801",
        "session_id": "HD8bcd4D-Sb4673-a237-623d1129c801"
        "device_id": "HD8bcd4D-Sb4673-a237-623d1129c801"
        "insert_id": "29fc2962-6d9c-455d-95ad-95b84f09b9e4",
        "source_id": "channel_name", 
        "URL": "moreretail.com/signup",
        "ip": "136.24.0.114"
      }
      "custom_properties": {
        "Referred by": "Friend"
      }
    }
    ```
    

Events are received from the servers (multiple sources) to our system through **INGEST SERVICE** (**AWS Kinesis/MSK)** into different raw topics. Topics are based on [event types](https://www.notion.so/CUSTOMER-ENGAGEMENT-PLATFORM-0a3dc694aaea47528a991ce6e7ae5b3f?pvs=21). 

## SYSTEM DESIGN

https://whimsical.com/system-architecture-9zr9SN3nfc2xJydtetEX1C

## INGESTION AND PRE-PROCESSING

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/0de39a63-1732-40b6-bb5a-ea675d7a2c11/728f40ce-75fb-492d-8fd9-0724707a2caf/Untitled.png)

- **Events Schema Validation**
    
    Events schema (both custom and pre defined) are maintained in **AWS Glue Schema Registry.** Each time an event is produced by the servers into our ingestion service, it undergoes schema validation check through AWS Glue Schema Registry. 
    This process send back error to the producer as well as to downstream **Transformer** to eliminate events that have wrong schema. 
    
    <aside>
    💡 This helps us to ensure data intactness throughout the pipeline, reduce downstream errors and anomalies, and maintain a centralised registry for ever evolving schemas.
    
    </aside>
    
- **Ingest Service**
    
    > **What should we choose? (Detailed comparison below)**
    > 
    - ***Key differences between AWS MSK and Kinesis***
        1. **For Low Volume Workloads** (up to 10 MB/sec):
            - Kinesis is preferred due to its ease of use and minimal operational management.
            - Kinesis is cheaper to set up and operate compared to provisioning an MSK cluster for the same volume.
            - The smallest MSK cluster is more expensive than a minimum 1 shard stream in Kinesis.
        2. **For Medium Volume Workloads** (up to 100 MB/sec) and **High Volume Workloads** (up to 1000 MB/sec and above):
            - Cost considerations depend on Kafka configuration settings which dictate MSK cluster performance.
            - Optimizing MSK cluster size can reduce costs, but it requires careful configuration.
            - With Kinesis, costs scale directly with the number of shards used, and there is less configuration needed.
        3. **Message Delivery Guarantees**:
            - Kinesis provides at-least-once message delivery.
            - MSK (Kafka) provides exactly-once delivery, but at the expense of increased complexity in application development.
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/0de39a63-1732-40b6-bb5a-ea675d7a2c11/1bf68b39-c6d0-4e96-b71e-065eeb358519/Untitled.png)
        
    
    <aside>
    💡 If we are expecting more than 2000 events/sec and want to have more control over buffer windows, fault tolerance and faster throughput, then the choice would be Kafka.
    
    </aside>
    
    The ingest service stores incoming raw data directly into **AWS S3 (Cold Storage) i**n parquet format making it suitable for use in analytics, pre-prod environment, re generate error scenarios etc.
    
    Ingest service will publish the raw streaming data to **Transformer (AWS managed service for Apache Flink).** 
    
- **Transformer (AWS managed service for Apache Flink)**
    
    <aside>
    💡 Transformer is an **Apache Flink** application that performs various asynchronous tasks to ensure data quality, integrity, enrichment and unifies the data for the entire downstream processes
    
    </aside>
    
    1. **De-duplication**:
        - Duplication in events can occur due to factors such as network failures, retries, or processing errors, resulting in the same event being processed multiple times. Its important to eliminate duplicate events so that data is not biased or incorrect.
        - The Flink application determines unique events based on insert_id, timestamp and user_id.
        - Kafka offers message delivery exactly once and can resolve the problem.
    2. **Unique Session identification:**
        - The application hashes user IDs and device IDs to determine unique sessions (session_id).
        - In cases where a user does not log in, it utilizes the device ID as a session identifier for the time being until user authenticates itself.
        - This helps to group sessions as a sequence of events and track them better.
    3. **Data Enrichment**:
        - Apache Flink enables Stream-Table, Stream-Stream joins.
        - Transformer enriches event data through geographical and user details lookups.
        - Geographical lookups provide insights into the location of users, enabling geo-specific analysis and targeting.
        - User details lookups enhance event data with additional user information, such as demographic details or user preferences (useful for instant recommendations)
        - The application also derives new features from existing properties, allowing for more comprehensive data analysis and modeling.
    4. **Data Filtration**:
        - To ensure data quality and consistency, Transformer includes data filtration capabilities.
        - Incorrect or incomplete data is filtered out before further processing, preventing it from impacting downstream analytics or applications.
        - This step helps maintain data integrity and reliability throughout the processing pipeline.
- **Extractor (AWS Lambda and Apache Flink)**
    1. Stateless Single Flink Application
    2. Read data once, process it and route it to multiple streams
    3. SQL support on streams
    4. Filter, Aggregates, Projection support on streams
    5. Out of box metrics for users
    6. For adhoc and simple tasks (AWS Lambda)
    
    https://imgr.whimsical.com/object/2qPrP8kDXgfUSWAjhTfumy
    
    <aside>
    💡 Extractor - Reads stream of event from various topics and apply necessary filters, transformations and route them to multiple out put streams [data grouped by event_id] [data grouped by session_id] [data grouped by gender] [users living in Bangalore] [frequent users]
    
    </aside>
    
    We can define schemas, transform and write data to multiple sinks as per requirement like AWS RedShift, Dynamo DB, Materialised views (Look ups), S3, Kafka streams for further processing depending on use case.
    Re route data streams based on geography. 
    
    Consider a look up table users_geocode (A look up table indexed by user_id, partitioned by state, city) with below attributes. Multiple such segments can be developed like user_contact_details, user_purchase_history.
    
    | user_id | login_time | city (calculated from ip or default user address) | state | lat, long (for geographical dashboards) | postal_code |
    | --- | --- | --- | --- | --- | --- |
    | n3ende | 11:53:43 | New York | NY | …, … | 67281 |
    | odxo1n | 11:53:45 | San Francisco | CA | …, … | 22821... |
    
    https://whimsical.com/user-data-enrichment-Uob3F4Db1tbLZAMvR4kMjL@2bsEvpTYSt1Hj9p1UNG1J8obArEJR2hasEB
    
    AWS Lambda can be used for simple requirements depending on the use cases. Apache Flink gives us flexibility to define windows, perform sql on streams, project schemas, state management and is optimised for stream processing.
     
    

## ELUID ENGINE

Lets take a example of a funnel to understand proposed ELUID engine
Must read to understand the proposed backend.

> How will funnels work?
> 

Look at a below ui example to find segmented users based on behaviours and send them engagements.

![483d933-ProductExp_Segment_Create.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/0de39a63-1732-40b6-bb5a-ea675d7a2c11/642f1a07-aa30-4b03-858f-b7508366cbb8/36405ceb-8880-4b1e-a5de-3f07c2aec726.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/0de39a63-1732-40b6-bb5a-ea675d7a2c11/f4d61cb2-8980-47cc-bbb1-678ca1b3ca37/Untitled.png)

### Consider below use case

Lets say end user of CEP wants to find users from New York (pre-defined segment) , who launched app in last 5 mins and made a purchase (charged) and send them an e-mail engagement with a message ‘Thanks for ordering’. 

How will our events data stored will be queried, how our data systems enable optimised and fast computations?

- Pre defined segments -
    
    Extractor ([**Extractor (AWS Lambda and Apache Flink)**](https://www.notion.so/Extractor-AWS-Lambda-and-Apache-Flink-790fb738953946f8aa5f2a9d59a5a77e?pvs=21)) calculates and create data streams which auto updates look up tables.
    
    https://whimsical.com/user-data-enrichment-Uob3F4Db1tbLZAMvR4kMjL@2bsEvpTYSt1Hj9p1UNG1J8obArEJR2hasEB
    
    Consider a table users_geocode (A materialised view on Redshift or a Dynamo DB table indexed by user_id, partitioned by state, city) with below attributes. Refer above image to see how the table got materialised with the below data.
    
    | user_id | login_time | city (calculated from ip or default user address) | state | lat, long (for geographical dashboards) | postal_code |
    | --- | --- | --- | --- | --- | --- |
    | n3ende | 11:53:43 | New York | NY | …, … | 67281 |
    | odxo1n | 11:53:45 | San Francisco | CA | …, … | 22821... |
    
    Given that the data in AWS DynamoDB is partitioned based on the attribute “state” and "city," executing a query with a filter condition where "city" equals 'New York' will exhibit high performance due to the efficient partitioning strategy, minimizing the need for full table scans and resulting in low latency query execution.
    
    - **example code and get request to query dynamodb tables with params sent dynamically**
        
        ```python
        **#Request params
        #{
        #  "TableName": "users_geocode",
        #  "FilterExpression": "city = :city", //dynamic
        #  "ExpressionAttributeValues": {
        #    ":city": "New York" //dynamic
        #  },
        #  "**ProjectionExpression": "user_id"
        **#}
        
        #Sample code to query dynamodb with params sent dynamically**
        import boto3
        
        def execute_dynamodb_query(**kwargs):
            # Create DynamoDB Resource
            dynamodb = boto3.resource('dynamodb')
        
            # Define the table resource
            table = dynamodb.Table('users_geocode')
        
            # Define the parameters for the query
            params = {
                'FilterExpression': 'city = :city',
                'ExpressionAttributeValues': {
                    ':city': city
                },
                'ProjectionExpression': 'user_id'  # Specify the attribute you want to retrieve
            }
        
            # Execute the query
            response = table.scan(**params)
        
            # Process the response
            if 'Items' in response:
                return response
            else:
                print("No items found")
        
        # Example usage:
        city = 'New York'
        result = execute_dynamodb_query(city)
        print(result)
        
        ```
        

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/0de39a63-1732-40b6-bb5a-ea675d7a2c11/e647b6e8-a345-4eb4-8b98-96e5f09d279f/Untitled.png)

- Events (Sequence)
    - App launch in last 5 mins (user’s first event in the funnel) 
    Events of all kinds are stored in Cassandra or S3 partitioned by event_category, event_id, day, hour.  ‣ (More on S3)
    A user from CEP UI can easily send a dynamic get request with parameters to select user_id from events table where  event_category = ? AND event_id = ? AND time > ? (example below)
        
        ```sql
        // cassandra table events
        CREATE TABLE IF NOT EXISTS events (
            event_category TEXT,
            event_id TEXT,
            day INT,
            hour INT,
            insert_id UUID,
            device TEXT,
            -- Add other properties as needed
            PRIMARY KEY ((event_category, event_id, day, hour), insert_id)
        )
        WITH CLUSTERING ORDER BY (timestamp);
        ```
        
        ```python
        from cassandra.cluster import Cluster
        from datetime import datetime, timedelta
        
        def execute_cassandra_query(event_category, event_id, time_range_minutes):
            # Connect to Cassandra cluster
            cluster = Cluster(['localhost'])  # Replace 'localhost' with your Cassandra cluster IP
            session = cluster.connect('your_keyspace')  # Replace 'your_keyspace' with your keyspace name
        
            # Calculate start time based on time range
            curr_time = datetime.now()
            start_time = curr_time - timedelta(minutes=time_range_minutes)
        
            # Define query
            query = "SELECT user_id FROM events WHERE event_category = ? AND event_id = ? AND time > ?"
        
            # Execute query with parameters
            rows = session.execute(query, (event_category, event_id, start_time))
        
            # Process the result
            result = []
            for row in rows:
                result.append(row)
        
            return result
        
        # Example request parameters for first event
        request_body = {
            "event_category": "system_events",
            "event_id": "App launch",
            "time_range_minutes": 5
        }
        # Example request parameters for second event
        request_body = {
            "event_category": "user_events",
            "event_id": "Charged",
            "time_range_minutes": 5
        }
        
        # Extract parameters from request body
        event_category = request_body["event_category"]
        event_id = request_body["event_id"]
        time_range_minutes = request_body["time_range_minutes"]
        
        # Execute the Cassandra query
        response_data = execute_cassandra_query(event_category, event_id, time_range_minutes)
        
        ```
        
        From above code, it can be implied that the end user can dynamically query events data.
        
    - Users who are charged in last 5 mins
    We can make use of a similar logic above to find user_id’s who completed purchase in last 5 mins by sending event_category = user_events, AND event_id = “charged” AND time > 5 mins.
        
        ```python
        from flask import Flask, jsonify, request as req, response as res
        from cassandra.cluster import Cluster
        
        app = Flask(__name__)
        
        # Function to execute Cassandra queries with parameterized query
        def dynamic_execute_dynamodb_query():
            params = req.body[0]
            return execute_dynamodb_query(params)
        
        # Function to retrieve user IDs for a specific event
        def get_users_for_event():
            params = req.body[1]
            return execute_cassandra_query(params.event_category, 
            params.event_id, params.time_range_minutes):
        
        # Route to calculate the funnel and send email engagement
        @app.route('/calculate_funnel_and_send_email', methods=['GET'])
        def calculate_funnel_and_send_email():
            # Get users for the specified event
        		users_for_segment = set(dynamic_execute_dynamodb_query(req))
            users_for_event = set(get_users_for_event(req))
        		
        		user_id = users_for_event.intersection(users_for_segment)
        		user_data = ....		# enrich user_data with email/contact_number 
            return user_data
        if __name__ == '__main__':
            app.run(debug=True)
        
        ```
        
        The whole code can be parameterised and made dynamic based on **Request Params** and can be used to send engagements to user segments.
        

This will return user data containing user_id, user_name, email_id, WhatsApp_number, push_token. CEP’s end user can choose the communication channel through ui (email, WhatsApp, notification) and send customised messages to segmented users.

## **API Documentation**

### **Segment - iPhone users in New York**

### **Endpoint: `/lookup/users_geocode/city=?"New York"&time=?5mins`**

**Method:** GET

**Description:** Retrieves iPhone users located in New York within the specified time frame.

**Request Parameters:**

- **`city`**: The city name (e.g., "New York").
- **`time`**: Time frame for filtering the users (e.g., 5mins).
- `table`: Look up (segments) for filtering users.

**Response Body:**

```json

{
  "users": [
    {
      "user_id": "12345",
      "session_id": "session_123",
      "lat": "40.7128",
      "long": "-74.0060",
      "city": "New York",
      "state": "NY",
      "postal_code": "10001"
    },
    {
      "user_id": "67890",
      "session_id": "session_456",
      "lat": "40.7306",
      "long": "-73.9352",
      "city": "New York",
      "state": "NY",
      "postal_code": "10002"
    }
    // More users...
  ]
}

```

**Event Funnel**

### **1. App Launch**

### **Endpoint: `/events/event_id=?"App Launch"&time=?5mins`**

**Method:** GET

**Description:** Retrieves users who launched the app within the specified time frame.

**Request Parameters:**

- **`event_id`**: The ID of the event (e.g., "App Launch").
- **`time`**: Time frame for filtering the events (e.g., 5mins).

**Response Body:**

```json
{
  "users": ["12345", "67890", "54321", ...]
}

```

### **2. Charged**

### **Endpoint: `/events/event_id=?"Charged"&time=?5mins`**

**Method:** GET

**Description:** Retrieves users who made a purchase within the specified time frame.

**Request Parameters:**

- **`event_id`**: The ID of the event (e.g., "Charged").
- **`time`**: Time frame for filtering the events (e.g., 5mins).

**Response Body:**

```json
{
  "users": [
    {
      "user_id": "12345",
      "email_id": "user1@example.com",
      "device_type": "iPhone"
    },
    {
      "user_id": "67890",
      "email_id": "user2@example.com",
      "device_type": "iPhone"
    }
    // More users...
  ]
}

```

### **List of Users Satisfying the Funnel**

### **Endpoint: `/funnel/create_funnel`**

**Method:** GET

**Description:** Retrieves users who satisfy the defined funnel criteria.

**Request Body:**

```json

{
  "segment": {
    "city": "New York"
  },
  "event_id_1": "App Launch",
  "event_id_2": "Charged",
  "time": "5mins"
}

```

**Response Body:**

```json

{
  "users": [
    {
      "user_id": "12345",
      "email_id": "user1@example.com",
    },
    {
      "user_id": "67890",
      "email_id": "user2@example.com",
    }
    // More users...
  ]
}
```

---

This API documentation outlines the endpoints, request parameters, request bodies, and response bodies for each operation. 

****

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/0de39a63-1732-40b6-bb5a-ea675d7a2c11/599e68fe-dab0-46c9-be1f-845c7ab59cba/Untitled.png)

## SLUID ENGINE

The SLUID ENGINE helps us determine answers to questions like below

**How much time do users spend on my site per session?
What are the average number of pages visited per session?
Which page is the most common landing page for a session?
What % of sessions end with a Purchase?
Compare user journeys?**

- **Real-time sessionizer**
    
    Real time sessionizer groups events by session_id key, and write them in redis stream cache. Redis stores aggregate/consolidated events per session as a session object. A user session begins when app is launched or start_event is recorded for a user and it ends when a closing_event is recorded. In case when closing_event is not recorded for a user, an inactivity timer closes the session based on set configuration. 
    
- **Unique User Session Tracking**
    
    End users of our CUSTOMER ENGAGEMENT PLATFORM ‘CEP’ can track each customer activity and related properties in the app as a stream of events in real time through redis with latency of ~1s (real-time).
    Unique session tracking service will request user sessions asynchronously by sending user_id as param to the GET request and get a stream of user events (maybe redis streams or web socket).
    **Redis Streams**: Redis Streams are a built-in data structure in Redis designed for streaming data processing. We can use Redis Streams to publish events from producers and consume them in real-time by clients. Clients can use the **`XREAD`** command to read events from a Redis stream, allowing for efficient and scalable events tracking.
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/0de39a63-1732-40b6-bb5a-ea675d7a2c11/d8f9f70c-1d4e-44ac-b962-339dfc551fdd/Untitled.png)
    
- **Real-Time Campaign Triggers Through Redis (Pre-Defined) And Cassandra**
    
    e.g., if a user adds an item to a cart but doesn't check out within 1 hour, and we want to send custom notifications. 
    Redis solves this problem as it stores each session as collection of events performed by app-user and we can write REDIS TRIGGER functions that determines the inactivity time of an user using SESSION TIMEOUT and user’s last event.
    so, if after session timeout of say 1 hour, if user’s last event was add to cart, we can send the information to a LAMBDA function (Server-less and on demand) to send pre defined customer engagements.
    Also, we can run scheduled pre defined **ad hoc or scheduled** cron jobs and spark jobs on CASSANDRA and AWS S3 on near real time session data (partitioned by session_id)  to send engagements **(e.g. discount in Bangalore)** to users in Bangalore.
    
- **Near Real-Time Queries And Dashboard for CEP**
    
    Once the session is closed, data from redis is rolled over and stored as an object in [Cassandra.](https://www.notion.so/CUSTOMER-ENGAGEMENT-PLATFORM-0a3dc694aaea47528a991ce6e7ae5b3f?pvs=21) 
    Cassandra serves as a hot storage and stores user sessions partitioned by session_id for a day/week (serves as an db for api calls, dashboard, KPI’s, metrics). We can also partition the data by event_id, user_id (research required). End users of CEP can be made available with near real-time dashboards showing key metrics and answering important questions **(most common landing page per session), (%of sessions ended in purchase) , (compare user journeys through graphical representation and much more), (identify type of user journeys end up in conversion).**
    
    For medium storage, we can move rolled over data to S3 or Redshift after necessary transformations.  Make calculations and aggregations, denormalise tables into facts and dimensions for daily, weekly and monthly reports and serve them on CEP dashboards to display KPIs (using simple GET requests targeting the tables) for end user to visualise actionable insights.
    **(average session length per day), (users activity on different days of week)** 
    
    Also, both of these data solutions can be used to run ad hoc or scheduled jobs to send important engagements to users based on pre defined triggers (business logic).
    
- **Data Model**
    - **Cassandra**
        
        <aside>
        💡 CASSANDRA -  Cassandra was chosen as a hot storage for its object based distributed database for NoSQL data, scalability, high availability, flexible data model, performance, consistency options, and strong community support, making it well-suited for storing and processing session-based data with varying event types in a distributed environment.
        
        </aside>
        
        Sessions will be stored as an object in a Cassandra keyspace for a day or two and data will be processed into relational model to be stored in Data warehouses like Redshift or S3 for enabling users use power of SQL queries.
        Cassandra keyspace will be partitioned on Day, Hour, session_id for faster access. This will enable us to fetch sessions data by applying filters on time, sessions etc.
        Our CEP will be able to make GET API Requests to our CASSANDRA Keyspace ‘sessions’  by sending in session_ids with desired filters dynamically.
        
        Click to view data model example for events and sessions
        
        https://docs.google.com/spreadsheets/d/1N9wNE6_cF8rUVmyBcUoUnmAxz5EIzoXYrmqocth1Ask/edit?usp=sharing
        
        ```sql
        CREATE TABLE IF NOT EXISTS sessions (
            session_id UUID,
            day INT,
            hour INT,
            week INT,
            month INT,
            session_start TIMESTAMP,
            session_end TIMESTAMP,
            user_id UUID,
            events MAP<TEXT, TEXT>,
            PRIMARY KEY ((session_id, day, hour), event_timestamp)
        ) WITH CLUSTERING ORDER BY (event_timestamp DESC);
        
        ```
        
        ```json
        {
          "session_id": "abc123",
          "user_id": "user123",
          "start_time": "2024-05-10T09:00:00",
          "end_time": "2024-05-10T09:30:00",
          "events": [
            {
              "event_id": "login",
              "timestamp": "2024-05-10T09:01:00",
              "location": {
                "latitude": 37.7749,
                "longitude": -122.4194
              },
              "device": "iPhone"
            },
            {
              "event_id": "browse",
              "timestamp": "2024-05-10T09:05:00",
              "page": "Home"
            },
            {
              "event_id": "search",
              "timestamp": "2024-05-10T09:10:00",
              "query": "electronics"
            },
            {
              "event_id": "add_to_cart",
              "timestamp": "2024-05-10T09:15:00",
              "product_id": "prod123",
              "quantity": 1
            },
            {
              "event_id": "checkout",
              "timestamp": "2024-05-10T09:20:00",
              "total_amount": 100,
              "payment_method": "credit_card"
            }
          ]
        }
        
        ```
        
    - **S3**
        
        We can write scheduled spark jobs on AWS EMR to perform transformations on our NoSQL data and convert it to Relational models. We can also use this as a medium storage for ad hoc queries. Data after the retention period shall be moved to cold storage for archiving so as to reduce cost.
        We can store sessions data in Amazon S3 partitioned by session day, week, and month, we can use a file format like Parquet or ORC for efficient storage and query performance.
        
        ```sql
        s3://your-bucket/sessions_data/
           └── year=2024/
               ├── month=05/
               │   ├── day=01/
               │   │   ├── session_data_2024-05-01.parquet
               │   │   └── ...
               │   └── ...
               └── ...
        ```
        
        Here's an example SQL query using Athena to retrieve session data for a specific day:
        
        ```sql
        SELECT *
        FROM sessions_data
        WHERE year = 2024 AND month = 05 AND day = 01
        ```
        
        By partitioning the data in S3 and using efficient file formats, we can optimize storage, reduce query costs, and achieve high query performance when querying session data in AWS.
        
    
    To maximize scalability of Cassandra clusters (hot storage) and reduce storage costs, TTL will be applied. Daily data in Cassandra will be consolidated and aggregated to derive key metrics and rolled over to S3 buckets (Cold/Medium storage) for reporting, analysis, Machine learning and dashboards on CEP platform.
    

A similar system has been designed by Netflix to process streaming events data that is able to handle 7million events/second

# 🛫 KEY Features

1. **Asynchronous Processing:** By leveraging asynchronous processing with tools like Apache Flink or AWS Lambda, our pipelines can handle large volumes of events without blocking or slowing down. This allows for parallel processing of events, leading to better scalability.
2. **Event Streaming Platforms:** Using event streaming platforms like **Apache Kafka or AWS Kinesis** enables our pipelines to ingest, process, and distribute events in real-time. These platforms are inherently scalable, allowing us to scale out horizontally by adding more processing nodes as the volume of events increases.
3. **Distributed Computing:** Our pipelines are designed using distributed computing principles, where tasks are divided and processed across multiple nodes in a cluster. This distributed architecture of **Apache Flink, S3, Cassandra** allows for seamless scalability by adding more nodes to the cluster as needed.
4. **Auto-scaling:** Cloud-based services like **AWS Lambda and Kubernetes (Flink) provide auto-scaling** capabilities, automatically adjusting the number of compute resources based on the workload. This ensures that our pipelines can scale up or down dynamically in response to changes in event volume or processing requirements.
5. **Partitioning and Sharding:** Data **partitioning and sharding** strategies are employed to distribute the workload evenly across multiple processing nodes. This ensures that no single node becomes a bottleneck and enables linear scalability as the workload grows.
6. **Fault Tolerance:** Our pipelines are designed with fault tolerance in mind, using techniques like **replication, checkpointing, and data backups t**o ensure data integrity and availability even in the event of node failures or network issues.
7. **Simple APIs**: To ensure quick access to data from our databases, we'll implement simple APIs that **return results promptly and can be easily parameterized.** These APIs will serve as convenient entry points for accessing relevant data without the need for complex queries or processing. These APIs can be seamlessly integrated into existing systems or applications, facilitating data access and analysis.
8. **Real-time session tracking :** User session tracking is a crucial feature that enables businesses to monitor and analyze user interactions within their applications or websites in real time with 1s latency.

# 🛫 TO-DO’s

1. Store user’s session data in Graph Database (for example Neo4J) to explore more use cases.
2. Research upon databases in depth to store data based on use cases.
3. Batch data pipelines - Convert data from NoSQL in Cassandra into Dimensional Data Models and store them in S3(Redshift)/Snowflake/Bigquery based on entities like sessions, users, events.
