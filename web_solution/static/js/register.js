// Select the HTML element with the ID "userField" and assign it to the variable userField
const userField = document.querySelector("#userField");
const feedbackUser = document.querySelector(".invalid_feedback_user");
const feedbackEmail = document.querySelector(".invalid_feedback_email");
const emailField = document.querySelector("#emailField");
const usernameSuccess = document.querySelector(".usernameSuccess");
const passwordField = document.querySelector("#passwordField");
const emailSuccess = document.querySelector(".emailSuccess");
const show = document.querySelector(".show");
const submit = document.querySelector(".submit-btn");

const handleToggleInput = (e) => {
    if(show.textContent == "SHOW") 
    {
        show.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    }

    else
    {
        show.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }   
};

show.addEventListener('click', handleToggleInput);

// Add an event listener to the userField element for the "keyup" event
userField.addEventListener("keyup", (e) => {
    // Inside the event listener function, get the value of the userField input
    const userVal = e.target.value;
    usernameSuccess.textContent = `Checking ${userVal}`;
    
    // Check if the length of the entered value is greater than 0
    if(userVal.length > 0)
    {
        // If the condition is true, initiate a fetch request to the server endpoint '/authentication/validate-username'
        fetch('/authentication/validate-username', {
            // Configure the request with a JSON body containing the entered username
            body: JSON.stringify({
                "username": userVal
            }),
            method: "POST",
        })
        // Once the fetch request is complete, convert the response to JSON
        .then((res) => res.json())
        // Process the JSON data returned from the server
        .then((data) => {
            usernameSuccess.style.display = "none";
            // Check if the server response contains a username_error property
            if(data.username_error)
            {
                // If true, add the CSS class 'is-invalid' to the userField element
                userField.classList.add('is-invalid');
                feedbackUser.style.display = "block";
                feedbackUser.innerHTML = `<p>${data.username_error}</p>`;
                submit.disabled = true;
            }

            else
            {
                submit.removeAttribute("disabled");
                userField.classList.remove('is-invalid');
                feedbackUser.style.display = "none";
                usernameSuccess.style.display = "block";
            }
        });
    }

    else 
    {
        // If the length of the entered value is 0, clear any previous error state
        userField.classList.remove('is-invalid');
        feedbackUser.style.display = "none";
        usernameSuccess.style.display = "none";
    }
});

emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;
    emailSuccess.textContent = `Checking ${emailVal}`;

    if(emailVal.length > 0)
    {
        fetch('/authentication/validate-email', {
            body: JSON.stringify({
                "email": emailVal
            }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            emailSuccess.style.display = "none";
            if(data.email_error)
            {
                submit.disabled = true;
                emailField.classList.add('is-invalid');
                feedbackEmail.style.display = "block";
                feedbackEmail.innerHTML = `<p>${data.email_error}</p>`;
            }

            else
            {
                submit.removeAttribute("disabled");
                emailField.classList.remove("is-invalid");
                feedbackEmail.style.display = "none";
                emailSuccess.style.display = "block";
            }
        })
    }

    else
    {
        emailField.classList.remove("is-invalid");
        feedbackEmail.style.display = "none";
        emailSuccess.style.display = "none";
    }
});
