# Spend Ruby

## Complaint Analysis Tool

**Spend Ruby** is a cutting-edge complaint analysis tool designed to handle and categorize customer complaints using a multimodal approach. Our system leverages advanced processing techniques to analyze various forms of input, including text, images, videos, and voice recordings.

### Key Features

- **Multimodal Processing:** 
  - **Text Analysis:** Extract and categorize information from written complaints.
  - **Image Analysis:** Identify and classify issues from image files.
  - **Video Analysis:** Process and categorize visual content from video recordings.
  - **Voice Analysis:** Transcribe and analyze audio content from voice recordings.

- **Centralized Aggregator:** 
  - A Flask-based service that consolidates data from all processing modules.
  - Performs final categorization and unifies insights to provide a comprehensive view of each complaint.

- **Advanced Categorization:**
  - Utilizes machine learning and natural language processing (NLP) techniques for accurate categorization.
  - Insights are categorized based on predefined criteria to ensure relevant and actionable outcomes.

- **Database Integration:**
  - **PostgreSQL:** Stores structured complaint data for detailed record-keeping.
  - **Elasticsearch:** Facilitates efficient search and retrieval of multimodal data.

### How It Works

1. **Data Collection:** 
   - Complaints are submitted in various formats (text, images, videos, voice).

2. **Processing Modules:** 
   - Each format is processed by its respective module (text, image, video, voice).
   - The modules operate autonomously to extract relevant insights.

3. **Central Aggregator:**
   - Aggregates insights from all processing modules.
   - Performs final categorization and stores results in the database.

4. **Unified View:**
   - Provides a complete view of each complaint, categorized by type and topic.
