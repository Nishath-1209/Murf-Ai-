// ----- Generate Audio -----
function generateAudio() {
    const text = document.getElementById("textInput").value;
    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text }),
    })
    .then(res => res.json())
    .then(data => {
        const audioPlayer = document.getElementById("audioPlayer");
        audioPlayer.src = data.audio_url;
        audioPlayer.play();
    })
    .catch(err => console.error("❌ Generate Audio Failed:", err));
}

// ----- Echo Bot -----
let mediaRecorder;
let audioChunks = [];
const startButton = document.getElementById("startRecording");
const stopButton = document.getElementById("stopRecording");
const echoAudio = document.getElementById("echoAudio");
const statusMessage = document.getElementById("uploadStatus");

startButton.addEventListener("click", async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", event => audioChunks.push(event.data));
    mediaRecorder.addEventListener("stop", () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("file", audioBlob, `recording_${Date.now()}.webm`);

        statusMessage.innerText = "Uploading...";
        fetch("/tts/echo", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            statusMessage.innerText = "✅ Playing back in Murf voice";
            echoAudio.src = data.audio_url;
            echoAudio.play();
        })
        .catch(err => {
            statusMessage.innerText = "❌ Echo failed";
            console.error(err);
        });
    });

    mediaRecorder.start();
    startButton.disabled = true;
    stopButton.disabled = false;
});

stopButton.addEventListener("click", () => {
    mediaRecorder.stop();
    startButton.disabled = false;
    stopButton.disabled = true;
});

// ----- LLM Conversation -----
let llmRecorder;
let llmChunks = [];
const llmStart = document.getElementById("startLLM");
const llmStop = document.getElementById("stopLLM");
const llmAudio = document.getElementById("llmAudio");
const llmStatus = document.getElementById("llmStatus");

llmStart.addEventListener("click", async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    llmRecorder = new MediaRecorder(stream);
    llmChunks = [];

    llmRecorder.addEventListener("dataavailable", event => llmChunks.push(event.data));
    llmRecorder.addEventListener("stop", () => {
        const audioBlob = new Blob(llmChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("file", audioBlob, `llm_recording_${Date.now()}.webm`);

        llmStatus.innerText = "🎙 Uploading to LLM...";
        fetch("/llm/query", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            llmStatus.innerText = "✅ Playing LLM response";
            llmAudio.src = data.audio_url;
            llmAudio.play();
        })
        .catch(err => {
            llmStatus.innerText = "❌ LLM query failed";
            console.error(err);
        });
    });

    llmRecorder.start();
    llmStart.disabled = true;
    llmStop.disabled = false;
});

llmStop.addEventListener("click", () => {
    llmRecorder.stop();
    llmStart.disabled = false;
    llmStop.disabled = true;
});
