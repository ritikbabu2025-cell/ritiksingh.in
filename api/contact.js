export default async function handler(req, res) {

  if (req.method !== "POST") {
    return res.status(405).json({
      error: "Method not allowed"
    });
  }

  try {

    const {
      name,
      email,
      phone,
      subject,
      message
    } = req.body || {};

    if (!name || !email || !subject || !message) {
      return res.status(400).json({
        error: "Please fill all required fields."
      });
    }

    const apiKey = process.env.RESEND_API_KEY;

    if (!apiKey) {
      return res.status(500).json({
        error: "Email service is not configured."
      });
    }

    const emailResponse = await fetch(
      "https://api.resend.com/emails",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`
        },

        body: JSON.stringify({

          from: "Portfolio Contact <onboarding@resend.dev>",

          to: ["ritikbabu2025@gmail.com"],

          reply_to: email,

          subject: `Portfolio Contact: ${subject}`,

          html: `
            <div style="font-family: Arial, sans-serif; line-height: 1.6;">

              <h2>New Contact Form Message</h2>

              <p>
                <strong>Name:</strong> ${escapeHtml(name)}
              </p>

              <p>
                <strong>Email:</strong> ${escapeHtml(email)}
              </p>

              <p>
                <strong>Phone:</strong> ${escapeHtml(phone || "Not provided")}
              </p>

              <p>
                <strong>Subject:</strong> ${escapeHtml(subject)}
              </p>

              <hr>

              <p>
                <strong>Message:</strong>
              </p>

              <p>
                ${escapeHtml(message).replace(/\n/g, "<br>")}
              </p>

            </div>
          `
        })
      }
    );

    const data = await emailResponse.json();

    if (!emailResponse.ok) {
      console.error(data);

      return res.status(500).json({
        error: "Email could not be sent."
      });
    }

    return res.status(200).json({
      success: true,
      message: "Email sent successfully."
    });

  } catch (error) {

    console.error(error);

    return res.status(500).json({
      error: "Something went wrong."
    });
  }
}


function escapeHtml(value) {

  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
