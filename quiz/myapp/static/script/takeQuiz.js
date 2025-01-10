document.addEventListener('DOMContentLoaded', () => {
  // Get the quiz end time (which is passed in UTC)
  const quizEndTime = new Date(document.querySelector('form').dataset.quizEndTime);
  const quizDurationTime = +document.querySelector('form').dataset.quizDurationTime;
  console.log('Quiz End Time (UTC):', quizEndTime, 'Duration:', quizDurationTime);

  // IST is UTC +5:30, so we subtract 5 hours and 30 minutes from the quizEndTime to convert it to IST
  const istOffset = 5.5 * 60; // 5.5 hours in minutes
  const quizEndTimeIST = new Date(quizEndTime.getTime() + (istOffset * 60 * 1000));
  console.log('Quiz End Time (IST):', quizEndTimeIST);

  // If you need to display the IST time in the UI
  const formattedISTTime = quizEndTimeIST.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
  console.log('Formatted IST Time:', formattedISTTime);

  if (isNaN(quizEndTimeIST)) {
      alert("Error: Invalid quiz end time. Please try again later.");
      return;
  }

  const timerDisplay = document.createElement('div');
  timerDisplay.id = 'timer-display';
  timerDisplay.style.fontSize = '18px';
  timerDisplay.style.color = '#333';
  timerDisplay.style.marginBottom = '20px';
  document.querySelector('.container').prepend(timerDisplay);

  const form = document.querySelector('form');

  var temp = new Date();

  if ( (quizEndTimeIST.getTime()-temp.getTime())> (quizDurationTime*60000)){
    temp = new Date(new Date().getTime() + quizDurationTime*60*1000);
  }else{
    temp = quizEndTimeIST;
  }
  const EndTime = temp;

  // Update the timer every second
  const timerInterval = setInterval(() => {
      const currentTime = new Date();
      console.log('Current Time:', currentTime); // Debugging output
      console.log('Time Left by access Time:', EndTime - currentTime); // Debugging output
      const timeLeft = EndTime - currentTime;

      if (timeLeft <= 0) {
          clearInterval(timerInterval);
          setTimeout(() => {
            form.submit(); // Auto-submit the form when time is up -- It will be executed after 1 second delay, But lines after this will be executed immediately
        }, 1000); // 1000 milliseconds = 1 seconds
          timerDisplay.textContent = "Time's up! Submitting your quiz...";
      } else {
          const minutes = Math.floor(timeLeft / 1000 / 60);
          const seconds = Math.floor((timeLeft / 1000) % 60);
          timerDisplay.textContent = `Time Left: ${minutes}m ${seconds}s`;
      }
  }, 1000);

  // Warn the user before the quiz ends
  const warningTime = Math.max((EndTime - new Date()) - 60000, 0);
  if (warningTime > 0) {
      setTimeout(() => {
          alert("You are running out of time! The quiz will auto-submit soon.");
      }, warningTime);
  }
});
