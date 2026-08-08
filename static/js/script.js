document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("assessmentForm");
    const resultSection = document.getElementById("resultSection");
    const resultScore = document.getElementById("resultScore");
    const resultLevel = document.getElementById("resultLevel");
    const resultMessage = document.getElementById("resultMessage");
    const analyzeBtn = document.getElementById("analyzeBtn");

    if (!form) {
        console.error("Assessment form not found.");
        return;
    }

    form.addEventListener("submit", async (event) => {

        // IMPORTANT:
        // Prevent normal browser form submission
        event.preventDefault();

        analyzeBtn.disabled = true;

        const buttonText = analyzeBtn.querySelector("span");

        if (buttonText) {
            buttonText.textContent = "Analyzing...";
        }

        // Collect form data
        const formData = new FormData(form);

        // Convert FormData into normal object
        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        console.log("Sending data:", data);

        try {

            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            console.log("Backend response:", result);

            if (!response.ok) {
                throw new Error(result.error || "Prediction failed");
            }

            // Show result section
            resultSection.style.display = "block";

            // Update result
            resultScore.textContent =
                result.score ?? result.probability ?? "--";

            resultLevel.textContent =
                result.level ?? result.prediction ?? "Analysis Complete";

            resultMessage.textContent =
                result.message ??
                "Your responses have been analyzed by the MindMate machine-learning model.";

            // Scroll to result
            setTimeout(() => {
                resultSection.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }, 100);

        } catch (error) {

            console.error("Error:", error);

            alert(
                "Unable to analyze your responses. Please try again."
            );

        } finally {

            analyzeBtn.disabled = false;

            if (buttonText) {
                buttonText.textContent = "Analyze My Patterns";
            }
        }

    });

});