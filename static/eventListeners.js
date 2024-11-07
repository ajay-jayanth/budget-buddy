document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.taskbar-button').forEach(taskbarButton => {
        taskbarButton.addEventListener('click', () => {
            if (!taskbarButton.classList.contains('selected')) {
                taskbarButton.classList.toggle('selected');
                if (taskbarButton.id == 'payment-button') {
                    document.getElementById('home-button').classList.remove('selected');
                    document.getElementById('calendar-button').classList.remove('selected');
                    window.location.href = '/payment-screen';
                    // fetch('/payment_screen', {
                    //     method: 'GET'
                    // })
                    // .then((response) => {
                    //     if (response.ok) {
                    //         window.location.href = '/payment-screen'
                    //     } else {
                    //         console.error('Error:', response);
                    //     }
                    // })
                    // .catch(error => {
                    //     console.error('Error loading payment screen:', error);
                    // });
                } else if (taskbarButton.id == 'home-button') {
                    document.getElementById('payment-button').classList.remove('selected');
                    document.getElementById('calendar-button').classList.remove('selected');
                    fetch('/homepage', {
                        method: 'GET'
                    });
                } else if (taskbarButton.id == 'calendar-button') {
                    document.getElementById('payment-button').classList.remove('selected');
                    document.getElementById('home-button').classList.remove('selected');
                    fetch('/schedule-payments-screen', {
                        method: 'GET'
                    });
                }
            }
        });
    });
});