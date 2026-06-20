<?php
// Note: If we wish to bypass this email sending logic and instead use Google Forms,
// we can redirect or link directly to the following Google Forms:
// - English: https://docs.google.com/forms/d/e/1FAIpQLScr2p4hvlgZebJeIhwEpOIGK_-44UZav6y90GKUXWgCObKz1w/viewform?usp=sharing&ouid=107107612521996613936
// - Korean: https://docs.google.com/forms/d/e/1FAIpQLSeVs0jefFqJyWl9xuOD8ssEzsPXlwRdk-YLtdUouE7Sc7PDJA/viewform?usp=header

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Detect which version of the form was visible during submission
    $sub_lang = $_POST["submission_lang"] ?? "en";
    
    if ($sub_lang === "kr") {
        $language = "Korean";
        $email = filter_var($_POST["email_kr"] ?? "", FILTER_SANITIZE_EMAIL);
        $rating = strip_tags($_POST["rating_kr"] ?? "Not specified");
        $price = strip_tags($_POST["price_willing_to_pay_kr"] ?? "Not specified");
        $comments = strip_tags($_POST["comments_kr"] ?? "");
    } else {
        $language = "English";
        $email = filter_var($_POST["email"] ?? "", FILTER_SANITIZE_EMAIL);
        $rating = strip_tags($_POST["rating_en"] ?? "Not specified");
        $price = strip_tags($_POST["price_willing_to_pay_en"] ?? "Not specified");
        $comments = strip_tags($_POST["comments_en"] ?? "");
    }

    if (empty($email)) {
        $email = "Anonymous Listener";
    }
    if (empty($comments)) {
        $comments = "(No comments provided)";
    }

    // 2. Email details
    $to = "tkprof.ai@gmail.com";
    $subject = "Secret Garden Pilot Feedback [" . strtoupper($language) . "]";
    
    // Use UTF-8 for Subject line encoding
    $encoded_subject = "=?UTF-8?B?" . base64_encode($subject) . "?=";
    
    $message = "You have received new feedback for The Secret Garden (Chapter 1):\n\n";
    $message .= "Email: " . $email . "\n";
    $message .= "Language Edition: " . $language . "\n";
    $message .= "Rating/Satisfaction: " . $rating . "\n";
    $message .= "Willingness to Pay: " . $price . "\n\n";
    $message .= "User Comments:\n" . $comments . "\n";
    
    // 3. Sender Headers with UTF-8 format to reduce spam score
    $headers = "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $headers .= "From: feedback@jigsawpuzzlehelper.com\r\n";
    if ($email !== "Anonymous Listener") {
        $headers .= "Reply-To: " . $email . "\r\n";
    }
    $headers .= "X-Mailer: PHP/" . phpversion();

    // 4. Send email
    mail($to, $encoded_subject, $message, $headers);
    
    // 5. Redirect back to the landing page with ?submitted=true and language choice
    header("Location: https://jigsawpuzzlehelper.com/secret_garden/?submitted=true&lang=" . ($sub_lang === "kr" ? "kr" : "en"));
    exit;
} else {
    header("Location: https://jigsawpuzzlehelper.com/secret_garden/");
    exit;
}
?>
