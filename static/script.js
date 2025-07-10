

const recordAudioButton = document.getElementById('record-audio');
const stopAudioButton = document.getElementById('stop-audio');
const audioPlayback = document.getElementById('audio-playback');

let mediaRecorder;
let audioChunks = [];



// Record audio
recordAudioButton.addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        audioPlayback.src = audioUrl;

        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');

        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        console.log(result);
        if (result.filename) {
            audioPlayback.src = `/uploads/${result.filename.split('/').pop()}`;
            audioPlayback.play();
        }

        audioChunks = [];
    };

    mediaRecorder.start();
    recordAudioButton.disabled = true;
    stopAudioButton.disabled = false;
});

// Stop recording
stopAudioButton.addEventListener('click', () => {
    mediaRecorder.stop();
    recordAudioButton.disabled = false;
    stopAudioButton.disabled = true;
});
