let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
}

(function () {
    const URL = "https://execute-api.us-east-1.amazonaws.com/stage/resource";


    const form = document.getElementById('contactForm');
        if (!form) {
               console.error("contact-form not found in DOM");
               return;
           }


    form.addEventListener('submit', async function (e) {
        e.preventDefault();


        const name = document.getElementById('senderName')?.value || "";
        const email = document.getElementById('senderEmail')?.value || "";
        const subject = document.getElementById('subject')?.value || "";
        const messageEl = document.getElementById('message'); 
        const message = messageEl ? messageEl.value : "";
        const cfToken = document.querySelector('[name="cf-turnstile-response"]')?.value || "";
        if (!cfToken) {
            alert("Please complete the captcha before sending.");
            return;
        }


        try {
            const resp = await fetch(URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify({ 
                    'name': name, 
                    'email': email, 
                    'subject': subject, 
                    'message': message,
                    'cfToken': cfToken
                }),
                    mode: 'cors' // not required, but harmless if you want to make it explicit
                });


            const contentType = resp.headers.get('content-type') || '';
                let bodyText = '';
            try { bodyText = await resp.text(); } catch { }


                console.log('API status:', resp.status);
                console.log('API headers:', Object.fromEntries(resp.headers.entries()));
                console.log('API body:', bodyText);


                if (!resp.ok) {
                   throw new Error(`HTTP ${resp.status} - ${bodyText || 'No body'}`);
                }


                alert("✅ Thanks for contacting us, we will get back to you soon!");
                this.reset();

            } catch (err) {
                console.error("Request failed:", err);
                alert("❌ Something went wrong. Please try again.");
            } finally {
                form.reset();
                turnstile.reset();
            }
    });
})();
