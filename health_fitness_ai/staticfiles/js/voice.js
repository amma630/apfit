function speakText(text) {
    if ('speechSynthesis' in window) {
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = "en-US";
        msg.pitch = 1.2;
        msg.rate = 1;
        msg.volume = 1;
        msg.voice = speechSynthesis.getVoices().find(voice => voice.name.includes("Google") || voice.name.includes("Microsoft")) || null;
        speechSynthesis.speak(msg);
    } else {
        alert("Voice synthesis not supported in your browser.");
    }
}

function speakRecommendationFromPage() {
    const recommendationText = document.getElementById("recommendation-voice").innerText;
    speakText(recommendationText);
}
