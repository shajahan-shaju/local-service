
console.log("Booking JavaScript loaded!");

function playElectricSound() {
    const audio = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audio.createOscillator();
    const gain = audio.createGain();

    oscillator.type = "sawtooth";
    oscillator.frequency.setValueAtTime(1500, audio.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(
        180, audio.currentTime + 0.3
    );

    gain.gain.setValueAtTime(0.12, audio.currentTime);
    gain.gain.exponentialRampToValueAtTime(
        0.001, audio.currentTime + 0.3
    );

    oscillator.connect(gain);
    gain.connect(audio.destination);

    oscillator.start();
    oscillator.stop(audio.currentTime + 0.3);

    oscillator.onended = function () {
        audio.close();
    };
}

document.addEventListener("DOMContentLoaded", function () {
    const alertBox = document.getElementById("bookingAlert");

    // Booking success popup open aagumbodhu electric sound
    if (alertBox) {
        try {
            playElectricSound();
        } catch (error) {
            console.log("Browser sound permission blocked:", error);
        }
    }

    document.addEventListener("click", function (event) {
        const button = event.target.closest("#alertOk, #alertClose");

        if (button && alertBox) {
            alertBox.remove();
        }
    });
});
