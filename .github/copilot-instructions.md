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

# Workflow Rules

The .csv files described above are the input for analysis. They are located in the `data/` folder.

**Data Analysis Process:**
1.  **Script Generation:** When analysis is requested, write Python scripts and save them in the `scripts/` folder.
2.  **Output Generation:** Save the outputs of these scripts (text logs, summaries, CSVs) in the `outputs/` folder in .md or .csv format.
3.  **Visualizations:** If visualization is requested, create plots using `matplotlib`, `plotly` or `seaborn` and **SAVE** them to `outputs/`. **NEVER** use `plt.show()` or interactive display commands, as they will freeze the headless environment.
4.  **Refinement Loop:** Use the outputs from the `outputs/` folder to check your results. If the results are incomplete or the script fails, read the error log or output, refine the script in `scripts/`, and run it again.
5.  **Finalization:** Once the analysis or visualization is complete and answers the question, document the purpose of each script with short descriptions in the `scripts/README.md` file. Keep this file well-organized so that future team members can easily understand each script's purpose. Then copy the final, working code from the script into new cells in the `EDA.py` file located in the root directory. Edit or consolidate existing cells as needed.
6.  **Formatting:** Ensure that the code added to `EDA.py` follows the **Jupytext percent format** (using `# %%` separators). All comments and outputs should be in German.