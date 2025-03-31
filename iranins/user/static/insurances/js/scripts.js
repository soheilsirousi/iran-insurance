document.addEventListener('DOMContentLoaded', function () {
    // Handling installment panels toggle with proper positioning
    const installmentButtons = document.querySelectorAll('.btn-installments');

    installmentButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('data-toggle');
            const installmentsPanel = document.getElementById(targetId);
            const card = this.closest('.insurance-card');

            // Close all other open panels first
            document.querySelectorAll('.installments-panel').forEach(panel => {
                if (panel.id !== targetId && panel.style.display === 'block') {
                    panel.style.display = 'none';
                    panel.closest('.insurance-card').style.zIndex = '1';
                }
            });

            // Toggle the current panel
            if (installmentsPanel.style.display === 'block') {
                installmentsPanel.style.display = 'none';
                card.style.zIndex = '1';
            } else {
                // Position the panel correctly and show it
                installmentsPanel.style.display = 'block';
                card.style.zIndex = '100';
            }
        });
    });

    // Close installment panels when clicking outside
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.btn-installments') && !e.target.closest('.installments-panel')) {
            document.querySelectorAll('.installments-panel').forEach(panel => {
                if (panel.style.display === 'block') {
                    panel.style.display = 'none';
                    panel.closest('.insurance-card').style.zIndex = '1';
                }
            });
        }
    });

    // بهبود استایل برای جلوگیری از کشیده شدن باکس‌های دیگر
    const styleEl = document.createElement('style');
    styleEl.textContent = `
        .insurance-cards-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 20px;
            align-items: start; /* مهم - جلوگیری از کشیده شدن کارت‌ها */
        }

        .insurance-card {
            position: relative; /* مهم برای نمایش درست پنل اقساط */
        }

        .installments-panel {
            display: none;
            border-top: 1px solid #edf2f7;
            background-color: #f9fafb;
            padding: 20px;
            position: relative; /* مهم برای قرار گرفتن درست */
        }

        .btn-pay-installment {
            background-color: #3182ce;
            color: white;
            border: none;
            padding: 2px 5px;
            border-radius: 3px;
            font-size: 10px;
            cursor: pointer;
            margin-left: 5px;
            line-height: 1.2;
            height: 18px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 10%;
            height: 20px;
            margin-bottom: 20px;
            margin-left: 15px;
            margin-right: 15px;
        }

        .btn-pay-installment:hover {
            background-color: #2c5282;
        }
    `;
    document.head.appendChild(styleEl);

    // اضافه کردن دکمه پرداخت به اقساط پرداخت نشده
    const unpaidInstallments = document.querySelectorAll('.installment-item:not(.paid)');
    unpaidInstallments.forEach(item => {
        const badge = item.querySelector('.installment-badge.small');
        if (badge) {
            const payButton = document.createElement('button');
            payButton.className = 'btn-pay-installment';
            payButton.textContent = 'پرداخت';
            badge.parentNode.insertBefore(payButton, badge);
        }
    });

    // باز و بسته کردن مودال افزودن بیمه جدید
    const addInsuranceBtn = document.querySelector('.btn-add-insurance');
    const modalOverlay = document.getElementById('new-insurance-modal');

    if (addInsuranceBtn && modalOverlay) {
        const modalClose = document.querySelector('.modal-close');
        const cancelBtn = document.querySelector('.btn-cancel');

        addInsuranceBtn.addEventListener('click', function () {
            modalOverlay.style.display = 'flex';
        });

        if (modalClose) {
            modalClose.addEventListener('click', function () {
                modalOverlay.style.display = 'none';
            });
        }

        if (cancelBtn) {
            cancelBtn.addEventListener('click', function () {
                modalOverlay.style.display = 'none';
            });
        }

        // بستن مودال با کلیک بیرون از محتوا
        modalOverlay.addEventListener('click', function (e) {
            if (e.target === modalOverlay) {
                modalOverlay.style.display = 'none';
            }
        });
    }

    // نمایش/مخفی کردن گزینه‌های اقساط بر اساس نوع پرداخت
    const paymentTypeSelect = document.getElementById('payment-type');
    const installmentOptions = document.querySelector('.installment-options');

    if (paymentTypeSelect && installmentOptions) {
        paymentTypeSelect.addEventListener('change', function () {
            if (this.value === 'installment') {
                installmentOptions.style.display = 'block';
            } else {
                installmentOptions.style.display = 'none';
            }
        });
    }
});