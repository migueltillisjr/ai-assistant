<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E3</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.3.1/jspdf.umd.min.js"></script>
    <style>
        body {
            background: linear-gradient(135deg, rgba(244, 67, 54, 0.8), rgba(153, 128, 5, 0.8));
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }

        /* Style for the help button */
        .help-button {
          position: fixed;
          top: 20px;
          right: 20px;
          padding: 10px 20px;
          background-color: #f0f0f0; /* Neutral color */
          color: #333; /* Neutral color */
          border: none;
          border-radius: 5px;
          font-size: 16px;
          font-weight: bold;
          cursor: pointer;
          transition: background-color 0.3s, color 0.3s;
        }

        /* Style for hover effect */
        .help-button:hover {
          background-color: #ccc; /* Lighter neutral color on hover */
          color: #222; /* Darker neutral color on hover */
        }

        #chatContainer {
            width: 90%;
            max-width: 1000px;
            height: 80%;
            background-color: #fff; /* white background for the chat area */
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.16);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        #chatOutput {
            flex-grow: 1;
            overflow-y: auto;
            padding: 20px;
            background-color: #f8f9fa;
        }

        #chatForm {
            padding: 10px;
            background-color: #f5e79f; /* gold background for input area */
            /*background-color: #ffd700; gold background for input area */
            border-top: 1px solid #dee2e6;
        }

        .chat-message {
            white-space: pre-line;
            display: flex;
            align-items: center;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 8px;
            background-color: #e9ecef;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .user-message {
            background-color: #ab3402; /* red background for user messages */
            color: white;
        }

        .message-icon {
            width: 24px;
            height: 24px;
            margin-right: 10px;
            border-radius: 50%; /* Makes the icon round */
        }

        #spinner {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 100;
        }

        #spinner.active {
            position: fixed;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.4); /* Semi-transparent white background */
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Custom Scrollbar */
        #chatOutput::-webkit-scrollbar {
            width: 8px;
        }

        #chatOutput::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 20px;
        }

        #chatOutput::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 20px;
        }

        #chatOutput::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
    </style>
</head>
<body>
<a href="https://docs.google.com/document/d/1QcIH4mEJRK87UNsuDTYnFaVEkM-WV1T2Y-lvxCHCAnU/edit?usp=sharing" target="_blank"><button class="help-button">?</button></a>
<div style="background: white;"><img src="imgs/logo.png" style="width: 170px; backgroun-color: white;position: absolute; top: 0;margin: 5px;"/></div>
<div id="chatContainer">
    <div id="chatOutput">
    </div>

    <div id="spinner" class="d-none">
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>

    <div id="chatForm">
        <form>
            <div class="input-group mb-3">
                <!-- Hidden file input for actual file selection -->
                <input type="file" class="form-control d-none" id="fileInput">
                <!-- Visible button to trigger file input -->
                <button class="btn btn-primary" type="button" onclick="document.getElementById('fileInput').click();" style="padding: 0;margin: 0;background-color: white;">
                    <img src="imgs/paperclip_icon.jpg" alt="Paperclip" style="height: 30px;padding: 0; margin: 0;">
                </button>

                <input type="text" class="form-control" placeholder="Type your message here..." id="chatInput">
                <button class="btn btn-primary" type="button" id="submitChat">Go</button>
            </div>
        </form>
    </div>

</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script>
    $(function() {
        // Function to automatically convert URLs within a specified element into hyperlinks
        function linkify(element) {
            var html = element.html();
            var urlRegex = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;

            // Replace plain text URLs with anchor tags
            var linkedHtml = html.replace(urlRegex, function(url) {
                return '<a href="' + url + '" target="_blank">' + url + '</a>';
            });

            // Update the element's HTML
            element.html(linkedHtml);
        }

        function appendMessage(content, isUser = false) {
            var messageDiv = $('<div style="position: relative; width: 100%;"></div>').addClass("chat-message");
            var messageIcon = $("<img>").addClass("message-icon");
            var messageText = $("<span></span>").html(content); // Use .html() to interpret markup
            var copyIcon = $('<img style="border-radius: 50%;width: 20px;position: absolute;right: 5px; border-color: white;" src="imgs/copy_icon.png" alt="Copy" class="copy-icon" style="cursor:pointer;">');

            if (isUser) {
                messageDiv.addClass("user-message");
                messageIcon.attr("src", "imgs/user_icon.png"); // User message icon
            } else {
                messageIcon.attr("src", "imgs/e3.logo.2.png"); // Response message icon
            }

            messageDiv.append(messageIcon);
            messageDiv.append(messageText);
            messageDiv.append(copyIcon); // Append the copy icon to the message
            $("#chatOutput").append(messageDiv);
            linkify(messageText); // Linkify the message text
            $("#chatOutput").scrollTop($("#chatOutput")[0].scrollHeight);

            copyIcon.click(function() { // Attach a click event to the copy icon
                copyToClipboard(messageText); // Call copyToClipboard function passing the messageText span
            });
        }

        function copyToClipboard(element) {
            // Check if the element contains 'li' items and handle accordingly
            var text = element.find('li').map(function() {
                return $(this).text(); // Get text of each 'li' element
            }).get().join('\n'); // Join all 'li' texts with a newline character

            if (!text) {
                text = element.text(); // Default to original text if no 'li' elements found
            }

            const tempElem = $('<textarea></textarea>'); // Create a temporary textarea element
            $('body').append(tempElem); // Append it to body to make it part of the DOM
            tempElem.val(text).select(); // Set its value to the text and select it
            document.execCommand("copy"); // Execute the copy command
            tempElem.remove(); // Remove the temporary element
            alert('Text copied successfully!'); // Optional: Alert user that text has been copied
        }

        function toggleSpinner(show) {
            if (show) {
                $("#spinner").removeClass("d-none").addClass("active");
            } else {
                $("#spinner").addClass("d-none").removeClass("active");
            }
        }

        $("#submitChat").click(function() {
            var chatInput = $("#chatInput").val();
            var fileInput = $("#fileInput")[0].files[0]; // Get the file object

            if (fileInput) {
                // Uploading file first
                var formData = new FormData();
                formData.append("file", fileInput);
                $.ajax({
                    url: "https://e3.ldmg.org/api/upload_contacts",
                    type: "POST",
                    data: formData,
                    contentType: false,
                    processData: false,
                    success: function(response) {
                        // File uploaded successfully, now send the chat input
                        sendChat(chatInput);
                    },
                    error: function() {
                        appendMessage("Failed to upload file");
                    }
                });
            } else {
                // If no file is selected, directly send the chat input
                sendChat(chatInput);
            }
        });

        function displayResponses() {
            var chatOutput = $("#chatOutput");
            responseData.message.forEach(function(message) {
                var responseItem = $("<div></div>").addClass("response-item").text(message);
                chatOutput.append(responseItem);
            });
        }


        // Function to send chat input
        function sendChat(chatInput) {
            if (chatInput.trim() !== "") {
                appendMessage(chatInput, true); // Display user message
                toggleSpinner(true); // Show spinner
                $.ajax({
                    url: "https://e3.ldmg.org/api/assistant", // Replace with your API endpoint
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({ message: chatInput }),
                    success: function(data) {
                        toggleSpinner(false); // Hide spinner after response
                        if (data.message) {
                            if (Array.isArray(data.message)) {
                                var responseList = $("<ul></ul>").addClass("response-list");
                                data.message.forEach(function(message) {
                                     var listItem = $("<li></li>").addClass("response-item").text(message); // Create list item
                                     responseList.append(listItem); // Append list item to the list
                                });
                                // Append the joined list to the chat output
                                appendMessage(responseList);
                            } else {
                                //var chatOutput = $("#chatOutput");
                                var responseItem = $("<div></div>").addClass("response-item").text(data.message); // Create a div for the message
                                appendMessage(responseItem); // Append the message to the chat output
                            }
                        } else {
                            appendMessage("No response data received");
                        }
                        $("#chatInput").val(""); // Clear input field after sending
                    },
                    error: function() {
                        appendMessage("Failed to retrieve data");
                        toggleSpinner(false); // Hide spinner even if request fails
                    }
                });
            }
        }

        // Append file name when a file is selected
        $("#fileInput").change(function() {

            var fileName = $(this).val().split("\\").pop(); // Get the file name
            var chatInput = $("#chatInput").val(); // Get the chat input value
            if (chatInput.trim() !== "") {
                chatInput += " " + fileName; // Append file name to chat input
            } else {
                chatInput = fileName; // Set chat input to file name if empty
            }
            $("#chatInput").val(chatInput); // Update chat input value
        });

        $("#chatInput").keypress(function(e) {
            if (e.which === 13) { // Enter key
                e.preventDefault(); // Prevent form submit
                $("#submitChat").click();
            }
        });
    });

//    $(function() {
//        // Update the message icon source
//        function appendMessage(content, isUser = false) {
//            var messageDiv = $("<div></div>").addClass("chat-message");
//            var messageIcon = $("<img>").addClass("message-icon");
//            var messageText = $("<span></span>").html(content);
//
//            if (isUser) {
//                messageDiv.addClass("user-message");
//                messageIcon.attr("src", "images/user_icon.png");
//            } else {
//                messageIcon.attr("src", "images/logo.png"); // Added custom logo
//            }
//
//            messageDiv.append(messageIcon);
//            messageDiv.append(messageText);
//            $("#chatOutput").append(messageDiv);
//        }
//
//        $("#submitChat").click(function() {
//            var chatInput = $("#chatInput").val();
//            appendMessage(chatInput, true); // Display user message
//            $("#chatInput").val(""); // Clear input field after sending
//        });
//
//        $("#fileInput").change(function() {
//            var fileName = $(this).val().split("\\").pop();
//            var chatInput = $("#chatInput").val();
//            $("#chatInput").val(fileName); // Update chat input value
//        });
//
//        $("#chatInput").keypress(function(e) {
//            if (e.which === 13) { // Enter key
//                e.preventDefault(); // Prevent form submit
//                $("#submitChat").click();
//            }
//        });
//    });
</script>


</body>
</html>
