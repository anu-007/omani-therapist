# Omani Therapist - Mental Health Chatbot

## Overview

The Omani Therapist is a voice-based mental health chatbot designed to provide culturally sensitive and empathetic support in the Omani Arabic dialect. It leverages a dual-model approach to ensure high-quality, safe, and therapeutically sound responses. The application is built with FastAPI and utilizes advanced AI models for speech-to-text, language understanding, and text-to-speech functionalities.

---

## Architecture Diagram
![Architecture Diagram](https://github.com/user-attachments/assets/3874b979-01a2-4ff3-a48d-0e2df361058d)

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
    * **Multiple Specialized Agents:** Different AI models optimized for various tasks (general assistance, domain-specific knowledge, etc.).
    * **Crisis Detection Handler:** Uses NLP techniques to identify potential emergency situations.

5.  **Data Management Layer**
    * **Encrypted Logs:** Secure storage of conversation data with user consent.
    * **Session Manager:** Maintains conversation context and user state.

6.  **Response Generation**
    * **Text to Speech (ElevenLabs):** Converts AI responses back into natural-sounding voice output.
    * Handles response formatting and delivery optimization.

---

## Flow Diagram
![Flow diagram](https://github.com/user-attachments/assets/a8b2b8f-c0f5-4143-84c8-78d0cf4c92d4)

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
    * **Keyword-Based:** Once the user query is translated to text, this system checks for common crisis keywords and provides an emergency contact number.
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
    ```
5.  **Create encryption key:**
    Run `generate_key.py` using:
    ```bash
    python generate_key.py
    ```
6.  **Run the application:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
7.  Open your browser and navigate to `http://localhost:8000`.

---

## Comparative Analysis for Dual Model Approach

The dual-model approach was chosen to leverage the strengths of different AI models and create a robust safety net.

| Model                       | Role                        | Strengths                                                                     | Weaknesses                                                              |
| :-------------------------- | :-------------------------- | :---------------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| **GPT-4o (Primary)** | Initial Response Generation | - High-quality, creative, and empathetic responses<br>- Strong language generation capabilities | - Can sometimes be too verbose or miss subtle safety cues               |
| **Claude-Opus-4 (Fallback)** | Validation and Refinement   | - Excellent at following instructions and adhering to safety guidelines<br>- Strong analytical and reasoning skills | - Can be more conservative and less creative in its responses           |

This combination allows for a system that is both therapeutically effective and highly secure.

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

* **Latency:** The end-to-end latency (from user speaking to receiving a response) is expected to be between 9-15 seconds, depending on the length of the audio and the complexity of the query.
* **Accuracy:**
    * **Speech-to-Text:** Whisper's accuracy for Arabic is generally high, but can be affected by background noise and speaker accent.
    * **Therapeutic Response:** The dual-model approach aims for a high degree of therapeutic accuracy, with the Fallback agent ensuring that all responses are safe and appropriate.

---

## Future Roadmap

* **Enhanced Crisis Detection:** Implement a more sophisticated crisis detection system by including audio cues from user input voice queries.
* **Audio Record Logs:** Implement recording of audio from a session based on user consent.
* **Data Storage:** Migrate to document storage for scaling this application to handle more data.
* **User Profiles:** Allow users to create profiles to track their progress and personalize their experience.
* **Better UX:** Implement a better UI for a better user experience by removing unwanted elements from the UI.
* **Multi-modal Support:** Introduce text-based chat and video sessions.
* **Integration with Healthcare Providers:** Develop a system for users to connect with human therapists if needed.
* **Crisis Dashboard:** Create a crisis-handling dashboard from crisis logs, which is handled by a professional therapist.