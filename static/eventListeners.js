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
    if (infoIcon) {
        infoIcon.addEventListener('click', () => {
            infoBox.style.display = infoBox.style.display === 'block' ? 'none' : 'block';
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.money-input').forEach(moneyInput => {
        moneyInput.addEventListener('input', (event) => {
            const rawValue = event.target.value.replace(/[^0-9.]/g, '');
            const numericValue = parseFloat(rawValue);
            console.log(rawValue);

            if (!isNaN(numericValue)) {
                const formattedValue = numericValue.toLocaleString('en-US');
                const cursorPosition = event.target.selectionStart;
                event.target.value = `$${formattedValue}`;
                const diff = event.target.value.length - rawValue.length - 1;
                event.target.setSelectionRange(cursorPosition + diff, cursorPosition + diff);
            } else {
                event.target.value = '$';
            }
        });

        moneyInput.addEventListener('blur', () => {
            const rawValue = moneyInput.value.replace(/[^0-9.]/g, '');
            const numericValue = parseFloat(rawValue);

            if (!isNaN(numericValue)) {
                moneyInput.value = `$${numericValue.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
            } else {
                moneyInput.value = '$0.00';
            }
        });

        moneyInput.addEventListener('focus', () => {
            if (moneyInput.value === '') {
                moneyInput.value = '$';
            }
        });
    });
});