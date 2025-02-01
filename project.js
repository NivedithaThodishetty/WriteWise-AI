function analyzeText() {
    let text = document.getElementById("essayInput").value;
    let feedbackDiv = document.getElementById("feedback");

    if (text.trim() === "") {
        feedbackDiv.innerHTML = "<p style='color: red;'>Please enter text to analyze.</p>";
        return;
    }

    // Simulated AI feedback (replace with actual NLP API call)
    let feedback = `
        <p><strong>Grammar:</strong> Your text is well-structured with minor grammatical errors.</p>
        <p><strong>Readability:</strong> Suitable for academic writing. Try using more varied sentence structures.</p>
        <p><strong>Vocabulary:</strong> Good word choices, but consider replacing repetitive words.</p>
    `;

    feedbackDiv.innerHTML = feedback;
}