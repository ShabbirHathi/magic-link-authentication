from django.core.mail import EmailMessage
from MagicLink.settings  import DEFAULT_FROM_EMAIL

def email_setting():
    from_email = DEFAULT_FROM_EMAIL
    cc_list = ['']
    return from_email, cc_list

def send_mail(user, magic_url):
    from_email, cc_list = email_setting()
    
    recipient_list = [user]
    subject = f"Login Link!"
    
    email_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sign In to Dashboard</title>
        <style>
            /* Add some basic styling for your card */
            .card {{
                width: 300px;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
            }}

            /* Style your logo image */
            .logo {{
                max-width: 100px; /* Adjust the width to your preference */
            }}

            /* Style the button */
            .button {{
                display: inline-block;
                background-color: #007BFF; /* Adjust the button color */
                color: white !important; /* Set text color to white */
                padding: 10px 20px;
                border-radius: 5px;
                text-decoration: none;
                
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <!-- Your logo -->
            <!-- <img src="http://127.0.0.1:8000/static/img/logo/logo.png" alt="Logo" class="logo"> -->
            
            <!-- Heading -->
            <h2>Sign in to Dashboard</h2>
            
            <!-- Paragraph 1 -->
            <p>Click the button below to sign in to Dashboard. This link will expire in 60 minutes.</p>
            
            
            <!-- Sign-in button -->
            <a href="{magic_url}" class="button">Sign In</a>
            
            <!-- Paragraph 2 -->
            <p>If you are having trouble with the above button, <a href="#">click here</a>.</p>
        </div>
    </body>
    </html>
    """

    email = EmailMessage(
        subject=subject,
        body=email_content,
        from_email=from_email,
        to=recipient_list,
        cc=cc_list,
    )
    
    # Specify that the content is HTML
    email.content_subtype = "html"
    
    # Send the email
    email.send()
    print("Email sent successfully.")
    
    return True
   