document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.taskbar-button').forEach(taskbarButton => {
        taskbarButton.addEventListener('click', () => {
            if (!taskbarButton.classList.contains('selected')) {
                taskbarButton.classList.toggle('selected');
                if (taskbarButton.id == 'payment-button') {
                    document.getElementById('home-button').classList.remove('selected');
                    document.getElementById('calendar-button').classList.remove('selected');
                    window.location.href = '/payment-screen';
                } else if (taskbarButton.id == 'home-button') {
                    document.getElementById('payment-button').classList.remove('selected');
                    document.getElementById('calendar-button').classList.remove('selected');
                    window.location.href = '/homepage';
                } else if (taskbarButton.id == 'calendar-button') {
                    document.getElementById('payment-button').classList.remove('selected');
                    document.getElementById('home-button').classList.remove('selected');
                    window.location.href = '/schedule-payments-screen';
                }
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const infoIcon = document.querySelector('.info-icon');
    const infoBox = document.querySelector('.info-box');

    infoIcon.addEventListener('click', () => {
        infoBox.style.display = infoBox.style.display === 'block' ? 'none' : 'block';
    });
});
