// کد جاوااسکریپت برای نمایش افکت‌ها
document.addEventListener('DOMContentLoaded', function () {
    // اضافه کردن افکت به باکس‌ها در هنگام هاور
    const assetBoxes = document.querySelectorAll('.asset-box');
    assetBoxes.forEach(box => {
        box.addEventListener('mouseenter', function () {
            this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
        });

        box.addEventListener('mouseleave', function () {
            this.style.boxShadow = 'none';
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const errorClose = document.querySelector('.error-close');
    if (errorClose) {
        errorClose.addEventListener('click', function () {
            this.closest('.error-alert').style.display = 'none';
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const closeBtn = document.querySelector('.close-btn');
    const cancelBtn = document.querySelector('.cancel-btn');
    const modalOverlay = document.querySelector('.modal-overlay');

    // بستن مودال
    const closeModal = function () {
        modalOverlay.style.display = 'none';
    };

    // نمایش مودال
    const openModal = function () {
        modalOverlay.style.display = 'flex';
    };

    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);

    // دکمه افزودن دارایی جدید
    const addAssetBtn = document.querySelector('.add-insured-btn'); // نام کلاس دکمه مورد نظر
    if (addAssetBtn) {
        addAssetBtn.addEventListener('click', openModal);
    }

    // کلیک خارج از مودال برای بستن
    modalOverlay.addEventListener('click', function (e) {
        if (e.target === modalOverlay) {
            closeModal();
        }
    });

    // // جلوگیری از بستن مودال هنگام ارسال فرم
    // document.querySelector('form').addEventListener('submit', function(e) {
    //     e.preventDefault();
    //     // کد ذخیره‌سازی اطلاعات فرم اینجا قرار می‌گیرد
    //     alert('دارایی جدید با موفقیت ثبت شد.');
    //     closeModal();
    // });
});

// اضافه کردن این کد به بخش جاوااسکریپت
document.addEventListener('DOMContentLoaded', function () {
    // کدهای قبلی

    // عملکرد افزودن ویژگی جدید
    const addPropertyBtn = document.getElementById('add-property-btn');
    const propertiesContainer = document.getElementById('custom-properties-container');
    let propertyCounter = 0;

    addPropertyBtn.addEventListener('click', function () {
        addNewPropertyFields();
    });

    function addNewPropertyFields() {
        propertyCounter++;

        const propertyRow = document.createElement('div');
        propertyRow.className = 'custom-property-row';
        propertyRow.innerHTML = `
            <div class="form-group">
                <label class="form-label" for="property-title-${propertyCounter}">عنوان ویژگی</label>
                <input type="text" id="property-title-${propertyCounter}" name="property-title-${propertyCounter}" class="form-input" placeholder="مثال: رنگ" required>
            </div>

            <div class="form-group">
                <label class="form-label" for="property-value-${propertyCounter}">مقدار ویژگی</label>
                <input type="text" id="property-value-${propertyCounter}" name="property-value-${propertyCounter}" class="form-input" placeholder="مثال: سفید" required>
            </div>

            <button type="button" class="remove-property-btn">&times;</button>
        `;

        propertiesContainer.appendChild(propertyRow);

        // اضافه کردن عملکرد حذف ویژگی
        const removeBtn = propertyRow.querySelector('.remove-property-btn');
        removeBtn.addEventListener('click', function () {
            propertyRow.remove();
        });
    }
});