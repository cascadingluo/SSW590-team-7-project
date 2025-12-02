// document.addEventListener('DOMContentLoaded', function() {
//     // Function to fetch and display emotion analysis
//     function fetchEmotionAnalysis() {
//         fetch('/emotion_analysis')
//             .then(response => response.json())
//             .then(data => {
//                 const emotionCountsDiv = document.getElementById('emotion-counts');
//                 const dominantEmotionDiv = document.getElementById('dominant-emotion');
//                 const emotionTrendsDiv = document.getElementById('emotion-trends');
//                 if (emotionCountsDiv) emotionCountsDiv.innerHTML = 'Emotion Breakdown';
//                 if (dominantEmotionDiv) dominantEmotionDiv.innerHTML = 'Dominant Emotion';
//                 if (emotionTrendsDiv) emotionTrendsDiv.innerHTML = 'Emotion Trends';

//                 // Emotion Counts
//                 if (emotionCountsDiv && Object.keys(data.emotion_counts).length > 0) {
//                     let countsHtml = 'Emotion Breakdown\n';
//                     for (const [emotion, count] of Object.entries(data.emotion_counts)) {
//                         //Converting the first letter of each emotion to uppercase and appends its count.
//                         countsHtml += `${emotion.charAt(0).toUpperCase() + emotion.slice(1)}: ${count}\n`;
//                     }
//                     emotionCountsDiv.innerHTML = countsHtml;
//                 } else if (emotionCountsDiv) {
//                     emotionCountsDiv.innerHTML = 'No emotion data available';
//                 }

//                 // Dominant Emotion
//                 if (dominantEmotionDiv && data.overall_dominant_emotion) {
//                     dominantEmotionDiv.innerHTML = `Dominant Emotion\n${data.overall_dominant_emotion.charAt(0).toUpperCase() + data.overall_dominant_emotion.slice(1)}`;
//                 } else if (dominantEmotionDiv) {
//                     dominantEmotionDiv.innerHTML = 'No dominant emotion detected';
//                 }

//                 // Emotion Trends
//                 if (emotionTrendsDiv && data.emotion_trends.length > 0) {
//                     let trendsHtml = 'Emotion Trends\n';
//                     data.emotion_trends.slice(-5).forEach(trend => {
//                         trendsHtml += `
//                 Emotion: ${trend.emotion}
//                 Confidence: ${(trend.confidence * 100).toFixed(2)}%
//                 Timestamp: ${new Date(trend.timestamp).toLocaleString()}
//                     `;
//                     });
//                     emotionTrendsDiv.innerHTML = trendsHtml;
//                 } else if (emotionTrendsDiv) {
//                     emotionTrendsDiv.innerHTML = 'No emotion trends available';
//                 }
//                 console.log('Emotion Analysis:', data);
//             })
//             .catch(error => {
//                 console.error('Error fetching emotion analysis:', error);
//                 const errorDiv = document.getElementById('emotion-analysis-error');
//                 if (errorDiv) {
//                     errorDiv.innerHTML = 'Unable to retrieve emotion analysis. Please try again later.';
//                 }
//             });
//     }

//     // Modify chat submission to trigger emotion analysis
//     function setupChatFormSubmission() {
//         const chatForm = document.getElementById('chat-form');
//         if (chatForm) {
//             chatForm.addEventListener('submit', function(event) {
//                 event.preventDefault();
//                 const messageInput = chatForm.querySelector('input[type="text"]');
//                 const message = messageInput.value.trim();
//                 if (message) {
//                     fetch('/api/chat', {
//                         method: 'POST',
//                         headers: {
//                             'Content-Type': 'application/json'
//                         },
//                         body: JSON.stringify({ input: message })
//                     })
//                     .then(response => response.json())
//                     .then(data => {
//                         messageInput.value = '';
//                         fetchEmotionAnalysis();
//                     })
//                     .catch(error => {
//                         console.error('Error sending message:', error);
//                     });
//                 }
//             });
//         }
//     }

//     setupChatFormSubmission();
//     fetchEmotionAnalysis();
// });