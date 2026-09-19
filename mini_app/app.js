const tg = window.Telegram?.WebApp;
if (tg) {
    tg.ready();
    tg.expand();
    tg.setHeaderColor('#000000');
    tg.setBackgroundColor('#000000');
}

if (tg?.initDataUnsafe?.user) {
    const u = tg.initDataUnsafe.user;
    const fullName = `${u.first_name || ''} ${u.last_name || ''}`.trim() || 'Пользователь';
    const username = u.username ? '@' + u.username : 'id' + u.id;
    document.getElementById('userName').textContent = fullName;
    document.getElementById('userUsername').textContent = username;
}

document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
        tg?.HapticFeedback?.impactOccurred('light');
    });
});

let selectedTariff = null;
let selectedTariffTitle = '';
let selectedAging = null;

const TARIFF_TITLES = { fast: 'Срочный', std: 'Стандарт', care: 'С проверкой' };

function selectTariff(key) {
    selectedTariff = key;
    selectedTariffTitle = TARIFF_TITLES[key];
    document.getElementById('modalTitle').textContent = selectedTariffTitle + ' — оформление';
    document.getElementById('orderModal').classList.add('active');
    tg?.HapticFeedback?.impactOccurred('medium');
}

function closeModal() {
    document.getElementById('orderModal').classList.remove('active');
    document.querySelectorAll('.aging-btn').forEach(b => b.classList.remove('active'));
    selectedAging = null;
}

function selectAging(btn) {
    document.querySelectorAll('.aging-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    selectedAging = btn.dataset.aging;
    tg?.HapticFeedback?.selectionChanged();
}

function submitOrder() {
    if (!selectedTariff) return showToast('Выберите тариф', 'info');
    if (!selectedAging) return showToast('Выберите отлегу', 'info');

    const country = document.getElementById('countryValue').textContent;

    const order = {
        id: 'RC' + Math.random().toString(36).substring(2, 7).toUpperCase(),
        tariff: selectedTariffTitle,
        aging: selectedAging,
        country: country,
        date: new Date().toISOString(),
        status: 'Новая',
    };

    // Сохраняем в localStorage
    saveOrder(order);

    // Если в Telegram — отправляем боту
    const inTelegram = tg && tg.initData && tg.initData.length > 0;
    if (inTelegram) {
        try {
            tg.sendData(JSON.stringify({ action: 'create_order', ...order }));
            tg.HapticFeedback?.notificationOccurred('success');
        } catch (e) {
            console.warn('sendData error', e);
        }
    }

    showToast('Заявка ' + order.id + ' создана', 'success');

    // Закрываем модалку
    closeModal();

    // Переключаемся в кабинет
    setTimeout(() => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        document.querySelector('.tab[data-tab="profile"]').classList.add('active');
        document.getElementById('tab-profile').classList.add('active');

        renderOrders();
        updateStats();
    }, 500);
}

function contactManager() {
    if (tg) {
        tg.openTelegramLink('https://t.me/vehaus');
        tg.HapticFeedback?.impactOccurred('medium');
    } else {
        window.open('https://t.me/vehaus', '_blank');
    }
}

function toggleCountry(e) {
    if (e) e.stopPropagation();
    const trigger = document.querySelector('#countrySelect .select-trigger');
    const options = document.getElementById('countryOptions');
    trigger.classList.toggle('open');
    options.classList.toggle('open');
    tg?.HapticFeedback?.selectionChanged();
}

function pickCountry(value) {
    document.getElementById('countryValue').textContent = value;
    document.querySelectorAll('#countryOptions .select-option').forEach(el => {
        el.classList.toggle('selected', el.dataset.value === value);
    });
    document.querySelector('#countrySelect .select-trigger').classList.remove('open');
    document.getElementById('countryOptions').classList.remove('open');
    tg?.HapticFeedback?.impactOccurred('light');
}

document.addEventListener('click', (e) => {
    if (!e.target.closest('#countrySelect')) {
        document.querySelector('#countrySelect .select-trigger')?.classList.remove('open');
        document.getElementById('countryOptions')?.classList.remove('open');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const el = document.querySelector('#countryOptions .select-option[data-value="Россия"]');
    if (el) el.classList.add('selected');
});

const TOAST_ICONS = {
    success: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
};

let toastTimeout = null;

function showToast(text, type = 'success') {
    const toast = document.getElementById('toast');
    const icon = document.getElementById('toastIcon');
    const txt = document.getElementById('toastText');
    toast.className = 'toast toast-' + type;
    icon.innerHTML = TOAST_ICONS[type] || TOAST_ICONS.success;
    txt.textContent = text;
    void toast.offsetWidth;
    toast.classList.add('show');
    if (toastTimeout) clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => toast.classList.remove('show'), 2600);
}


// ===== Управление заявками =====
function getOrders() {
    try {
        return JSON.parse(localStorage.getItem('rellion_orders') || '[]');
    } catch (e) {
        return [];
    }
}

function saveOrder(order) {
    const orders = getOrders();
    orders.unshift(order);
    localStorage.setItem('rellion_orders', JSON.stringify(orders.slice(0, 50)));
}

function renderOrders() {
    const list = document.getElementById('ordersList');
    if (!list) return;

    const orders = getOrders();

    if (!orders.length) {
        list.innerHTML = '<div class="empty">У вас пока нет заявок</div>';
        return;
    }

    list.innerHTML = orders.map(o => `
        <div class="order-item">
            <div class="order-head">
                <span class="order-id">${o.id}</span>
                <span class="order-status">${o.status}</span>
            </div>
            <div class="order-body">
                <div class="order-row">
                    <span class="order-label">Тариф</span>
                    <span class="order-value">${o.tariff}</span>
                </div>
                <div class="order-row">
                    <span class="order-label">Отлега</span>
                    <span class="order-value">${o.aging}</span>
                </div>
                <div class="order-row">
                    <span class="order-label">Страна</span>
                    <span class="order-value">${o.country}</span>
                </div>
                <div class="order-row">
                    <span class="order-label">Дата</span>
                    <span class="order-value">${formatDate(o.date)}</span>
                </div>
            </div>
        </div>
    `).join('');
}

function formatDate(iso) {
    try {
        const d = new Date(iso);
        const pad = n => String(n).padStart(2, '0');
        return `${pad(d.getDate())}.${pad(d.getMonth() + 1)}.${d.getFullYear()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
    } catch (e) {
        return iso;
    }
}

function updateStats() {
    const orders = getOrders();
    document.getElementById('statOrders').textContent = orders.length;

    // Средняя отлега
    if (orders.length) {
        const years = orders
            .map(o => parseInt(o.aging))
            .filter(n => !isNaN(n));
        if (years.length) {
            const avg = (years.reduce((a, b) => a + b, 0) / years.length).toFixed(1);
            document.getElementById('statAging').textContent = avg + ' лет';
        }
    } else {
        document.getElementById('statAging').textContent = '—';
    }
}

// Рендер при загрузке
document.addEventListener('DOMContentLoaded', () => {
    renderOrders();
    updateStats();
});

// Рендер при переключении на кабинет
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        if (tab.dataset.tab === 'profile') {
            renderOrders();
            updateStats();
        }
    });
});
