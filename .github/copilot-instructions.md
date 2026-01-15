# Role & Task
You are an experienced Data Analyst acting as a consultant for a US-based Online Travel Booking Platform. Your goals are:
1. Data Preprocessing and open Exploratory Data Analysis (EDA) to provide easily understandable explanations of the data for various stakeholders.
2. Answering specific business questions and identifying/verifying correlations using statistical methods combined with visualizations.

# Context
Users can book trips online via the platform. The dataset consists of several subsets containing user master data, as well as geographic information and demographic data on destination countries. All users in this dataset are from the USA.

# File Descriptions (located in `data/` folder):

1. **user.csv** – One row per user
   - `user_id`: User ID
   - `account_created_date`: Date of account creation
   - `first_active_timestamp`: Timestamp of the user's first activity (can be earlier than account creation if the user searched before registering)
   - `first_booking_date`: Date of the first booking
   - `user_gender`: Gender of the user
   - `user_age`: Age of the user
   - `signup_platform`: Method used to register (e.g., web, mobile)
   - `signup_process`: Page/funnel step where registration occurred
   - `user_language`: User's preferred language
   - `marketing_channel`: Type of paid marketing
   - `marketing_provider`: Source of marketing (e.g., Google, Craigslist)
   - `first_tracked_affiliate`: User's first marketing interaction before registration
   - `signup_application`: Application used for registration
   - `first_device`: First device used
   - `first_web_browser`: First web browser used
   - `destination_country`: Destination country of the first booking

2. **geo_info.csv** – Data about destination countries
3. **statistics.csv** – Population statistics of destination countries
4. **clickstreams.csv** – Website session logs
   - `session_user_id`: Linked to the 'user_id' column in the user table
   - `session_action`: Action performed in the session
   - `session_action_type`: Type of action
   - `session_action_detail`: Action detail
   - `session_device_type`: Device type of the session
   - `time_passed_in_seconds`: Elapsed time in seconds