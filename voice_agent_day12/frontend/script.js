let isRecording = false;
let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById('recordBtn');
const userText = document.getElementById('userText');
const aiText = document.getElementById('aiText');

recordBtn.addEventListener('click', () => {
    if (!isRecording) {
        startRecording();
    } else {
        stopRecording();
    }
});

async function startRecording() {
    isRecording = true;
    audioChunks = [];
    recordBtn.textContent = "⏹ Stop Recording";

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        recordBtn.textContent = "Processing...";
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append("audio", audioBlob, "recording.wav");

        try {
            const res = await fetch("http://127.0.0.1:5000/process-audio", {
                method: "POST",
                body: formData
            });

            if (!res.ok) throw new Error("Server error");

            const data = await res.json();

            userText.textContent = data.user_transcript || "[No speech detected]";
            aiText.textContent = data.ai_reply || "[No AI reply]";

            if (data.audio_url) {
                const audio = new Audio("http://127.0.0.1:5000" + data.audio_url);
                audio.play();
            }

        } catch (err) {
            console.error(err);
            aiText.textContent = "Error getting AI reply.";
        } finally {
            recordBtn.textContent = "🎤 Start Recording";
            isRecording = false;
        }
    };
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
    }
}
