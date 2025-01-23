document.addEventListener("DOMContentLoaded", () => {
    console.log("Script loaded and DOM fully parsed");

    // Handle form submissions with feedback
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", event => {
            console.log(`Form with action ${form.action} submitted`);
        });
    });

    // Handle image preview for content submission
    const imageInput = document.querySelector('input[type="file"]');
    const imagePreview = document.createElement("img");
    if (imageInput) {
        imageInput.addEventListener("change", event => {
            const file = event.target.files[0];
            if (file && file.type.startsWith("image/")) {
                const reader = new FileReader();
                reader.onload = e => {
                    imagePreview.src = e.target.result;
                    imagePreview.style.maxWidth = "100%";
                    imageInput.insertAdjacentElement("afterend", imagePreview);
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Toggle visibility for flash messages
    const flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach(msg => {
        setTimeout(() => msg.remove(), 3000);
    });

    // Symptom Checker Logic
    const symptomForm = document.getElementById("symptom-checker-form");
    if (symptomForm) {
        symptomForm.addEventListener("submit", event => {
            event.preventDefault();
            console.log("Symptom Checker submitted");

            const symptoms = Array.from(symptomForm.querySelectorAll("input[type='checkbox']:checked"))
                .map(input => input.value);

            const symptomOutput = document.getElementById("symptom-checker-output");

            if (symptoms.length === 0) {
                symptomOutput.textContent = "Please select at least one symptom to continue.";
                symptomOutput.style.color = "red";
            } else {
                // Basic analysis (could be expanded for more advanced checks)
                const warningSymptoms = ["frequent urination", "weak urine flow", "blood in urine"];
                const highRisk = symptoms.some(symptom => warningSymptoms.includes(symptom));

                symptomOutput.style.color = highRisk ? "red" : "green";
                symptomOutput.textContent = highRisk
                    ? "Your symptoms suggest a need for further medical evaluation. Please consult a specialist."
                    : "Your symptoms do not indicate immediate concern, but monitoring is recommended.";
            }
        });
    }
});
