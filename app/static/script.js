document.addEventListener("DOMContentLoaded", () => {
  console.log("Script loaded and DOM fully parsed");

  // Handle form submissions with feedback
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", (event) => {
      console.log(`Form with action ${form.action} submitted`);
    });
  });

  // Handle image preview for content submission
  const imageInput = document.querySelector('input[type="file"]');
  const imagePreview = document.createElement("img");
  if (imageInput) {
    imageInput.addEventListener("change", (event) => {
      const file = event.target.files[0];
      if (file && file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (e) => {
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
  flashMessages.forEach((msg) => {
    setTimeout(() => msg.remove(), 3000);
  });

  // Symptom Checker Logic
  const symptomForm = document.getElementById("symptom-checker-form");
  if (symptomForm) {
    symptomForm.addEventListener("submit", (event) => {
      event.preventDefault();
      console.log("Symptom Checker submitted");

      const symptoms = Array.from(
        symptomForm.querySelectorAll("input[type='checkbox']:checked")
      ).map((input) => input.value);

      const symptomOutput = document.getElementById("symptom-checker-output");

      if (symptoms.length === 0) {
        symptomOutput.textContent =
          "Please select at least one symptom to continue.";
        symptomOutput.style.color = "red";
      } else {
        // Basic analysis (could be expanded for more advanced checks)
        const warningSymptoms = [
          "frequent urination",
          "weak urine flow",
          "blood in urine",
        ];
        const highRisk = symptoms.some((symptom) =>
          warningSymptoms.includes(symptom)
        );

        symptomOutput.style.color = highRisk ? "red" : "green";
        symptomOutput.textContent = highRisk
          ? "Your symptoms suggest a need for further medical evaluation. Please consult a specialist."
          : "Your symptoms do not indicate immediate concern, but monitoring is recommended.";
      }
    });
  }

  //Format created at time for posts
  let elArr = document.querySelectorAll("#createdAt");

  function formatDate(el) {
    let currDate = new Date();
    let postDate = new Date(el.innerText);
    console.log(postDate);
    let text;

    let diff = currDate - postDate; // in ms
    // ms to seconds
    let seconds = Math.floor(diff / 1000);
    // seconds to minutes
    let minutes = Math.floor(seconds / 60);
    // minutes to hours
    let hours = Math.floor(minutes / 60);
    // hours to days
    let days = Math.floor(hours / 24);

    if (seconds < 60) {
      text = "Just Now";
    } else if (minutes < 2) {
      text = `${minutes} minute ago`;
    } else if (minutes < 60) {
      text = `${minutes} minutes ago`;
    } else if (hours < 2) {
      text = `${hours} hour ago`;
    } else if (hours < 24) {
      text = `${hours} hours ago`;
    } else if (days < 2) {
      text = `${days} day ago`;
    } else if (days < 7) {
      text = `${days} days ago`;
    } else {
      text = `${postDate.getDate()} ${postDate.toLocaleString("default", {
        month: "short",
      })} ${postDate.getFullYear()}`;
    }

    el.innerHTML = text;
  }

  if (elArr) {
    elArr.forEach((el) => {
      formatDate(el);
    });
  }

  //Insert user initials into avatar

  function getInitials(name) {
    return name
      .split(" ")
      .map((n) => n[0].toUpperCase())
      .join("");
  }

  let namesArr = document.querySelectorAll("#authorName");
  if (namesArr) {
    namesArr.forEach((_name) => {
      let initials = getInitials(_name.innerText);
      let avatar = _name.previousElementSibling;
      avatar.innerText = initials;
    });
  }
});
