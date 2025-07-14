# Omani Therapist - Mental Health Chatbot

## Overview

The Omani Therapist is a voice-based mental health chatbot designed to provide culturally sensitive and empathetic support in the Omani Arabic dialect. It leverages a dual-model approach to ensure high-quality, safe, and therapeutically sound responses. The application is built with FastAPI and utilizes advanced AI models for speech-to-text, language understanding, and text-to-speech functionalities.

---

## Demo video
[![Demo](https://img.youtube.com/vi/1jChc8BaOzo/mqdefault.jpg)](https://www.youtube.com/watch?v=1jChc8BaOzo)

---

## Flow Diagram
![Flow Diagram](https://github.com/user-attachments/assets/3874b979-01a2-4ff3-a48d-0e2df361058d)

1.  **User Interface Layer**
    * **Voice Input:** This is the entry point where users interact with the system through voice commands.
    * Handles audio capture and initial user interaction management.

2.  **Speech Processing Layer**
    * **Audio to Text (Whisper):** Converts voice input to text using OpenAI's Whisper ASR technology.
    * Provides the foundation for all downstream text-based processing.

3.  **Core Processing Engine**
    This is the brain of the system, with three key components:

    * **Crisis Detection Module:** Analyzes incoming text for crisis-related keywords and patterns.
    * Triggers immediate protocol activation when crisis indicators are detected.

    * **Consent Manager:** Handles user privacy preferences and consent for data logging.
    * Ensures compliance with privacy regulations.

4.  **AI Agents Layer**
    * **Multiple Specialized Agents:** Different AI models for generation and validation of response.
    * **Crisis Detection Handler:** Uses NLP techniques to identify potential emergency situations from the LLM model responses.

5.  **Data Management Layer**
    * **Encrypted Logs:** Secure storage of conversation data with user consent.
    * **Session Manager:** Maintains conversation context and user state and filter unwanted events to make execution faster.

6.  **Response Generation**
    * **Text to Speech (ElevenLabs):** Converts AI responses back into natural-sounding voice output.

---

## Architecture Diagram
![Architecture Diagram](https://github.com/user-attachments/assets/cb29a0ee-99b8-4e00-b764-f4be943804e6)

1.  **Core Flow**
    * The user records an audio message in the browser and clicks `Stop Recording`.
    * The frontend sends the audio file to the FastAPI backend.
    * The backend saves the audio file and transcribes it into text using `Whisper`.
    * The transcribed text is first checked for crisis keywords.
    * If no crisis is detected, the text is passed to the `run_conversation` function, which initiates the dual-model agent workflow.
    * The **Primary Therapist Agent (GPT-4o)** generates a response in Omani Arabic.
    * If the primary model detects any crisis in the user input, it flags it with `[CRISIS_DETECTED] <type>`.
    * An agent callback checks for these flagged responses and breaks the flow to return the crisis-handling response.
    * The backend records the encrypted user query in the `crisis_logs` database.
    * If the callback does not detect any crisis flag, it forwards the response to the Fallback model for validation.
    * The **Fallback/Validation Therapist Agent (Claude-Opus-4)** reviews and, if necessary, refines the response.
    * Another agent callback executes, again checking for crisis flags.
    * The final response is returned to the backend.
    * The backend converts the text response into an audio file using `ElevenLabs` text-to-speech.
    * The backend sends the audio file URL back to the frontend.
    * The backend deletes the input and output audio files.
    * The frontend plays the audio response to the user.

2.  **Crisis Management Protocol**
    * **Keyword-Based:** Once the user query is translated to text, this system checks for common crisis keywords and provides an static message and emergency contact number.
    * **NLP-Based:** Some queries are difficult to detect for any crisis. Therefore, another layer of LLM-based crisis detection is added where the model checks for user sentiment and flags the query as a crisis.
    * These protocols are enabled in three layers: once on user input and twice after the model's response.
    * Interaction logs are stored in an encrypted format for security and compliance in `crisis_logs.db`.
    * These logs can later be listed in a crisis-handling dashboard.

---

## System Design

The system is composed of the following key components:

1.  **Frontend:** A simple HTML/CSS/JavaScript interface that allows users to record audio, provide consent for session recording, and receive audio responses.
2.  **Backend (FastAPI):** A Python-based `FastAPI` backend that handles audio uploads, orchestrates the AI agent workflow using `google-adk`, and manages crisis situations.
3.  **Dual-Model AI (Agents):** A sophisticated agentic workflow that processes user input through two distinct AI models:
    * **Primary Therapist Agent (GPT-4o):** Generates the initial therapeutic response.
    * **Fallback/Validation Therapist Agent (Claude-Opus-4):** Reviews and refines the primary agent's response to ensure safety, cultural appropriateness, and therapeutic quality.
4.  **Speech-to-Text (Whisper):** Transcribes the user's Omani Arabic audio into text.
5.  **Text-to-Speech (ElevenLabs):** Converts the AI-generated text response back into natural-sounding Omani Arabic audio.
6.  **Crisis Detection:** A mix of keyword and NLP-based systems to identify and respond to crisis situations, such as suicidal ideation or harm to others.
7.  **Database (SQLite):** Logs crisis-related conversations for safety and review purposes.

---

## Set-up Instructions

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/omani-therapist.git](https://github.com/your-username/omani-therapist.git)
    cd omani-therapist
    ```
2.  **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add the following:
    ```
    OPENAI_API_KEY=your_openai_api_key
    ELEVENLABS_API_KEY=your_elevenlabs_api_key
    ANTHROPIC_API_KEY=your_anthropic_api_key
    ENCRYPTION_KEY=your_db_encryption_key (can be generated using generate_key.py)
    PORT=port_number_for_application
    ```
5.  **Run the application:**
    ```bash
    mkdir -p uploads && uvicorn main:app --host 0.0.0.0 --port $PORT
    ```
6.  Open your browser and navigate to `http://localhost:<port>`.

---

## Comparative Analysis for Dual Model Approach

## Overall Comparative Summary - Dual Model Approach
In summary, GPT-4o excels in speed and conciseness without compromising quality or cultural relevance, making it ideal for the primary user-facing role. Claude Opus 4, despite its higher latency and token usage, offers a strong and reliable validation or fallback mechanism, ensuring robust support. (These observations are based on same convertation but different primary and fallback models)


| Feature                 | GPT-4o (Primary)                                     | Claude Opus 4 (Fallback/Validation)                          | Claude Opus 4 (Primary)                                     | GPT-4o (Fallback/Validation)                          |
| :---------------------- | :--------------------------------------------------- | :----------------------------------------------------------- | :---------------------------------------------------------- | :---------------------------------------------------- |
| **Response Quality** | Empathetic, concise, practical, culturally sensitive. | Empathetic, practical, slightly more verbose/conversational. | Empathetic, probing, detailed, conversational.              | Concise validation of primary's quality and safety.   |
| **Cultural Fit (Omani)** | Excellent (prayer inclusion)                         | Excellent (prayer inclusion)                                 | Excellent (prayer inclusion, general cultural sensitivity) | Not directly applicable (validation role)             |
| **Speed (Latency)** | **Faster (Avg. 3.8s)** | Slower (Avg. 8.8s)                                           | **Much Slower (Avg. 13.8s)** | **Much Faster (Avg. 2.7s)** |
| **Token Usage** | **Lower (Avg. 77 tokens)** | Higher (Avg. 189 tokens)                                     | **Much Higher (Avg. 216 tokens)** | Lower (Avg. 56 tokens)                                |
| **Crisis Handling** | **Extremely fast and direct intervention.** | Fast and direct intervention.                                | Fast and direct intervention.                               | Extremely fast and clear crisis detection/validation. |
| **Overall Efficiency** | **High** | Moderate                                                     | Low                                                         | High                                                  |
| **Primary Suitability** | **High (efficient, effective, culturally aware)** | Moderate (good content, but high latency/verbosity)          | Moderate (good content, but high latency/verbosity)         | N/A (designed for primary use)                        |
| **Fallback Suitability**| N/A (designed for primary use)                       | **High (robust validation, good content)** | N/A (designed for primary use)                              | **High (rapid, clear validation)** |

---

## Sample convertation logs
Some sample logs can be found here. [Convertations](logs/sample_conv.md)

---

## Omani Arabic Details

The application is specifically designed to understand and generate the Omani Arabic dialect. This is achieved through:

* **Targeted Prompts:** The prompts for the AI models explicitly instruct them to use the Omani dialect.
* **Culturally Sensitive Training Data:** The models have been trained on a vast corpus of text that includes Arabic dialects, enabling them to generate culturally appropriate responses.
* **ElevenLabs Voice:** A specific Omani Arabic voice from ElevenLabs is used for the text-to-speech conversion, ensuring a natural and authentic user experience.

---

## Safety Protocol

The safety of users is the highest priority. The following protocols are in place:

1.  **Crisis Keyword Detection:** A predefined list of keywords in Arabic and English is used to detect potential crisis situations.
2.  **Dual-Model Validation:** The Fallback/Validation agent acts as a second layer of safety, reviewing all responses for harmful or inappropriate content.
3.  **Crisis Response Messages:** If a crisis is detected, the system provides a predefined, safe, and supportive message with emergency contact information.
4.  **Encrypted Logging:** All crisis-related conversations are encrypted and logged in a secure database for review by qualified professionals based on consent.

---

## Latency and Accuracy Metrics

* **Latency:** The end-to-end latency (from user speaking to receiving a response) is expected to be between 7-13 seconds, depending on the length of the audio and the complexity of the query.
* **Accuracy:**
    * **Speech-to-Text:** Whisper's accuracy for Arabic is generally high, but can be affected by background noise and speaker accent.
    * **Therapeutic Response:** The dual-model approach aims for a high degree of therapeutic accuracy, with the Fallback agent ensuring that all responses are safe and appropriate.

---

## Future Roadmap

### Standalone Crisis Detection Module
* **Professional Intervention:** Implement clear protocols and automated triggers for seamless handoff to human mental health professionals or emergency services when a crisis is detected.
* **Crisis Dashboard:** Develop a dedicated dashboard for supervisors to monitor real-time crisis alerts, review flagged conversations, and manage interventions efficiently.
* **Integration with Healthcare Providers:** Establish secure and compliant pathways for direct integration with local healthcare providers and emergency services, enabling swift and coordinated support during crises.

### Sentiment Analysis from Audio and Multi-Modal Support
* **Detect Sentiment from User Audio Input:** Integrate advanced audio emotion analysis (e.g., using technologies like iMentiv.ai's Audio Emotion Analysis) to detect subtle emotional cues directly from the user's voice. This sentiment data will then be passed to the LLM agents, allowing for more nuanced and empathetic responses.
* **Add Emotional Tags for Audio Delivery:** Utilize capabilities such as ElevenLabs' emotional deliveries with audio tags to generate natural-sounding voice outputs that reflect appropriate emotional tones, enhancing the perceived empathy and human-likeness of the chatbot.
* **Support for Text and Video:** Expand the system to support text and video inputs, integrating sentiment analysis for these modalities as well. This will create a more versatile and accessible platform for users who prefer different communication methods.

### Replace Database with Object Store
* **Record and Store Audio Conversations:** Implement functionality to securely record and store audio conversations, with strict encryption measures, only upon obtaining explicit user consent.
* **HIPAA Compliance:** Design and implement all data handling and storage processes to meet stringent healthcare data privacy standards, including HIPAA compliance.

### Better UI/UX
* **Improved User Interface (UI):** Enhance the visual design and layout of the chat interface for improved readability and ease of interaction.
* **Enhanced User Experience (UX):** Streamline the conversational flow, reduce friction points, and introduce features that make interactions feel more natural and supportive.

### Better Terms and Conditions and Usage Guides
* **Clearer Terms and Conditions:** Develop concise and transparent terms and conditions that clearly outline data privacy, AI limitations, and user responsibilities.
* **Comprehensive Usage Guides:** Create user-friendly guides that explain how to best interact with the chatbot, what to expect, and where to seek human help if needed.

### Tweak Prompts Based on Cultural Input for a Regional Therapist
* **Continuous Cultural Feedback Loop:** Establish an ongoing process for incorporating feedback from native Omani Arabic speakers and cultural experts to fine-tune agent prompts.
* **Enhanced Regional Nuance:** Iteratively adjust the prompts to deepen the chatbot's understanding and application of Omani cultural values, idioms, and specific socio-religious contexts in its therapeutic responses.