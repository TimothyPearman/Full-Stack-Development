const API_URL = 'http://127.0.0.1:8000';

// ── Application state
const state = {
    // Data
    notices: [], // cached list of traffic correction notices
    //books: [], // cached book list
    //myBooks: [], // cached current user's books
    //currentBookId: null, // id of book currently in detail view

    // Auth (used in Assessment 3)
    token: null, // JWT string once logged in
    currentUser: null, // user object { id, username, role }
    clearance: null, // user clearance level (Officer or Civilian)

    // UI
    isLoading: false, // true while any fetch is in progress
    lastError: null // last error message string
};

window.state = state;

// ── Utility functions
/**
 * showToast(message, duration) – displays a temporary toast notification
 * @param {string} message – the notification text
 * @param {number} duration – how long to show in milliseconds
 */
function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    // allow pointer events while visible
    toast.style.pointerEvents = 'auto';

    setTimeout(function() {
        toast.classList.remove('show');
        toast.style.pointerEvents = 'none';
    }, duration);
}

function setBreadcrumb(crumbs) {
    // crumbs: array of {label, route, params} objects
    // Last crumb is current page (not a link)
    const bc = document.getElementById('breadcrumb');
    if (!bc) {
        return;
    }

    bc.innerHTML = crumbs.map((crumb, i) => {
        if (i === crumbs.length - 1) {
            return '<span>' + crumb.label + '</span>'; // current page
        }
        const route = crumb.route || 'list';
        const params = crumb.params ? JSON.stringify(crumb.params).replace(/"/g, '&quot;') : '{}';
        return '<a href="#" onclick="navigateTo(\'' + route + '\', ' + params + ')">' +
            crumb.label + '</a>';
    }).join('<span class="crumb-sep">&rsaquo;</span>');
}

// ── View management
/**
 * showView(viewId) – hides all views, then reveals the one requested.
 * @param {string} viewId – the id of the <section> to show, e.g. 'view-list'
 */
function showView(viewId) {
    // 1. Remove 'active' from every view
    document.querySelectorAll('.view').forEach(section => {
        section.classList.remove('active');
    });

    // 2. Add 'active' to the requested view
    const target = document.getElementById(viewId);
    if (target) {
        target.classList.add('active');
    } else {
        console.warn('showView: unknown view id "' + viewId + '"');
    }
}

/**
 * canAccess(route) – returns true if the current state allows
 * the user to access the given route.
 */
function canAccess(route) {
    // Public routes: accessible without a token
    const publicRoutes = ['info', 'login', 'register', 'user-login', 'admin-login'];
    if (publicRoutes.includes(route)) {
        return true;
    }

    // All other routes require a logged-in user
    if (!state.token || !state.currentUser) {
        showToast('Please log in to access this page.', 3000);
        navigateTo('info');
        return false;
    }

    // Officer-only routes
    const officerRoutes = ['admin-dash', 'admin-management'];
    if (officerRoutes.includes(route) && !hasOfficerClearance()) {
        showToast('You do not have permission to access this page.', 3000);
        navigateTo('user-dash');
        return false;
    }

    // Civilian-only routes
    const civilianRoutes = ['user-dash', 'user-profile'];
    if (civilianRoutes.includes(route) && !hasCivilianClearance()) {
        showToast('You do not have permission to access this page.', 3000);
        navigateTo('admin-dash');
        return false;
    }

    return true;
}

/**
 * hasOfficerClearance() – returns true if user has Officer clearance
 */
function hasOfficerClearance() {
    return state.clearance === 'Officer';
}

/**
 * hasCivilianClearance() – returns true if user has Civilian clearance
 */
function hasCivilianClearance() {
    return state.clearance === 'Civilian';
}

// ── Router
/**
 * navigateTo(route, params) – central router for the SPA.
 * @param {string} route – one of: 'list', 'detail', 'about'
 * @param {object} params – optional extra data, e.g. { id: 3 }
 */
function navigateTo(route, params = {}) {
    if (!canAccess(route)) {
        return;
    }

    // Update URL hash (keeps hash routing compatible)
    const hashRoute = route === 'detail' && params.id
        ? '#detail/' + params.id
        : '#' + route;

    if (window.location.hash !== hashRoute) {
        // pushState preserves hash routing while adding a history entry
        history.pushState({ route, params }, '', hashRoute);
    }

    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.dataset.view === route);
    });

    // Route to the correct view
    const viewId = ROUTE_TO_VIEW[route] || 'view-info';
    switch (route) {
        // ! could map breadcrumbs like in the ROUTE_TO_VIEW object instead of hardcoding here
        // landing routes
        case 'info':
            setBreadcrumb([{ label: 'Home' }, { label: 'Info' }]);
            break;
        case 'register':
            setBreadcrumb([{ label: 'Home' }, { label: 'Register' }]);
            break;
        case 'login':
            setBreadcrumb([{ label: 'Home' }, { label: 'Login' }]);
            break;

        // login routes
        case 'user-login':
            setBreadcrumb([{ label: 'Home' }, { label: 'User Login' }]);
            break;
        case 'admin-login':
            setBreadcrumb([{ label: 'Home' }, { label: 'Admin Login' }]);
            break;

        // user routes
        case 'user-dash':
            setBreadcrumb([{ label: 'User' }, { label: 'Dashboard' }]);
            loadUserNotices();
            break;
        case 'user-profile':
            setBreadcrumb([{ label: 'User' }, { label: 'Profile' }]);
            loadUserProfile();
            break;

        // admin routes
        case 'admin-dash':
            setBreadcrumb([{ label: 'Admin' }, { label: 'Dashboard' }]);
            break;
        case 'admin-management':
            setBreadcrumb([{ label: 'Admin' }, { label: 'Management' }]);
            break;
            
        default:
            setBreadcrumb([{ label: 'Home' }]);
    }

    showView(viewId);
    updateActiveNav(route);

    if (route === 'info' || route === 'register' || route === 'logout') {
        setVisibleNav('main-nav');
        return;
    }

    if (route === 'login' || route === 'user-login' || route === 'admin-login') {
        setVisibleNav(['main-nav', 'login-nav']);
        return;
    }

    if (route === 'user-dash' || route === 'user-profile') {
        setVisibleNav('user-nav');
        return;
    }

    if (route === 'admin-dash' || route === 'admin-management') {
        setVisibleNav('admin-nav');
    }
}

// Map of route names to view IDs
const ROUTE_TO_VIEW = {
	// landing page views
    'info': 'view-info',
	'register': 'view-register',
    'login': 'view-login',
    //'login': 'view-user-login', // default login view

    // login views
    'user-login': 'view-user-login',
    'admin-login': 'view-admin-login',

    // user views
    'user-dash': 'view-user-dashboard',
    'user-profile': 'view-user-profile',
    'user-logout': 'view-user-logout',

    // admin views
    'admin-dash': 'view-admin-dashboard',
    'admin-management': 'view-admin-management',
    'admin-logout': 'view-admin-logout',

	'logout': 'view-logout'
};

// ── Hash-based routing
/**
 * Reads the URL hash and navigates to the matching route.
 * Supported hash formats: #list | #about | #detail/3
 */
function routeFromHash() {
    const hash = window.location.hash.slice(1); // remove leading '#'
    if (!hash) {
        navigateTo('info');
        return;
    }

    const parts = hash.split('/'); // e.g. ['detail', '3']
    const route = parts[0];
    const id = parts[1] ? parseInt(parts[1], 10) : null;

    navigateTo(route, { id });
}

// Listen for hash changes (browser back / forward, or manual URL edits)
window.addEventListener('hashchange', routeFromHash);

// Handle browser back / forward buttons
window.addEventListener('popstate', function(event) {
    if (event.state && event.state.route) {
        navigateTo(event.state.route, event.state.params || {});
    } else {
        routeFromHash();
    }
});

// Sets visibility of nav bars based on current route
function setVisibleNav(navIds) {
    const visibleNavs = Array.isArray(navIds) ? navIds : [navIds];

    // Show selected nav bars, hide the others
    ['main-nav', 'login-nav', 'user-nav', 'admin-nav'].forEach(id => {
        const nav = document.getElementById(id);
        if (nav) {
            nav.style.display = visibleNavs.includes(id) ? 'flex' : 'none';
        }
    });
}

// Updates the 'active' class on nav links based on the current route
function updateActiveNav(route) {
    // Toggle 'active' class on nav links based on their data-view matching the current route
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.dataset.view === route);
    });
}

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    // attach click listeners to nav links
    document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function(event) {

                // Do not change the hash for logout links here
                if (this.id && this.id.includes('logout')) {
                    return;
                }

                // Prevent default link behavior that changes the hash immediately and bypasses the navigateTo logic
                event.preventDefault();
                // Update URL hash, which triggers routeFromHash and navigateTo
                // if data-view is not set, default to 'info'
                window.location.hash = this.dataset.view || 'info';
            });
    });

    const userLoginBtn = document.getElementById('user-login-btn');
    if (userLoginBtn) {
        userLoginBtn.addEventListener('click', function() {
			handleLogin('user');
        });
    }

    const adminLoginBtn = document.getElementById('admin-login-btn');
    if (adminLoginBtn) {
        adminLoginBtn.addEventListener('click', function() {
			handleLogin('admin');
        });
    }

    const userRegisterBtn = document.getElementById('user-register-btn');
    if (userRegisterBtn) {
        userRegisterBtn.addEventListener('click', function() {
            handleRegister();
        });
    }

    // Add logout button listeners
    const userLogoutBtn = document.querySelector('a[id="user-logout-btn"]');
    if (userLogoutBtn) {
        userLogoutBtn.addEventListener('click', function(event) {
            event.preventDefault();
            handleLogout();
        });
    }

    const adminLogoutBtn = document.querySelector('a[id="admin-logout-btn"]');
    if (adminLogoutBtn) {
        adminLogoutBtn.addEventListener('click', function(event) {
            event.preventDefault();
            handleLogout();
        });
    }

    const profileUpdateBtn = document.getElementById('profile-update-btn');
    if (profileUpdateBtn) {
        profileUpdateBtn.addEventListener('click', function() {
            handleUpdateUserContactInfo();
        });
    }

    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            loadUserNotices();
        });
    }

    const userDashboardNotices = document.getElementById('user-dashboard-notices');
    if (userDashboardNotices) {
        userDashboardNotices.addEventListener('click', function(event) {
            const button = event.target.closest('.notice-toggle');
            if (!button) {
                return;
            }
            toggleNoticeDetails(button);
        });
    }

    window.addEventListener('hashchange', routeFromHash);
    setVisibleNav('main-nav');
    routeFromHash();
});

// Authentication handlers
function handleLogin(loginRole) {
    // get the appropriate login view based on role
    const loginView = document.getElementById(loginRole === 'admin' ? 'view-admin-login' : 'view-user-login');
    if (!loginView) {
        return;
    }

    // Extract username and password from the login form
    const usernameInput = loginView.querySelector('#login-username');
    const passwordInput = loginView.querySelector('#login-password');
    const errorText = loginView.querySelector('#login-error');
    const username = usernameInput ? usernameInput.value.trim() : '';
    const password = passwordInput ? passwordInput.value : '';

    // Clear previous error message
    if (errorText) {
        errorText.textContent = '';
    }

    // check for empty fields
    if (!username || !password) {
        if (errorText) {
            errorText.textContent = 'Please enter both username and password.';
        }
        return;
    }

    // Sequence: get clearance -> verify role -> request token
    // get clearance of account 
    fetch(API_URL + '/user/clearance', {
        method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    username: username,
                    password: password
                })
            })
        // Handle response
        .then(function(response) {
            return response.json().then(function(data) {
                if (!response.ok) {
                    throw new Error(data.detail || 'Failed to get clearance');
                }
                return data;
            });
        })
        .then(function(clearanceData) {
            state.clearance = clearanceData.clearance;

            // verify clearance matches login role
            if (loginRole === 'admin' && state.clearance !== 'Officer') {
                throw new Error('Account does not have admin clearance');
            }
            if (loginRole === 'user' && state.clearance !== 'Civilian') {
                throw new Error('Account does not have user clearance');
            }

            // request login token
            return fetch(API_URL + '/user/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    username: username,
                    password: password
                })
            });
        })
        // Handle response
        .then(function(response) {
            return response.json().then(function(data) {
                if (!response.ok) {
                    throw new Error(data.detail || 'Login failed');
                }
                return data;
            });
        })
        // Store token and user info in state
        .then(function(data) {
            state.token = data.access_token;
            state.currentUser = {
                username: username,
                clearance: data.clearance
            };

            // logged in message
            showToast('You have successfully logged in.');

            // Navigate based on clearance level
            if (data.clearance === 'Officer') {
                setVisibleNav('admin-nav');
                navigateTo('admin-dash');
            } else if (data.clearance === 'Civilian') {
                setVisibleNav('user-nav');
                navigateTo('user-dash');
            } else {
                showToast('Unknown user role', 3000);
                navigateTo('info');
            }
        })
        .catch(function(error) {
            if (errorText) {
                errorText.textContent = error.message;
            }
            showToast(error.message, 3000);
        });
}

// Logout handler
function handleLogout() {
    confirmAction(
        'Are you sure you want to log out?',
        function() {
            state.token = null;
            state.currentUser = null;
            state.clearance = null;
            state.notices = [];
            showToast('You have been logged out.');
            navigateTo('info');
            updateActiveNav('info');
        }
    );
}

/**
 * confirmAction(message, callback) – shows a confirmation dialog
 * @param {string} message – the confirmation message
 * @param {function} callback – function to call if user confirms
 */
function confirmAction(message, callback) {
    if (window.confirm(message)) {
        callback();
    }
}

// Registration handler
function handleRegister() {
    // get the registration view
    const registerView = document.getElementById('view-register');
    if (!registerView) {
        return;
    }

    // Extract fields from the registration form
    const usernameInput = registerView.querySelector('#register-username');
    const passwordInput = registerView.querySelector('#register-password');
    const passwordConfirmInput = registerView.querySelector('#register-password-confirm');
    // personal information fields
    const fullNameInput = registerView.querySelector('#register-full-name');
    const dateOfBirthInput = registerView.querySelector('#register-dob');
    const currentAddressInput = registerView.querySelector('#register-address');
    // drivers license details fields
    const driverLicenseNumberInput = registerView.querySelector('#register-license-number');
    const postcodeInput = registerView.querySelector('#register-license-postcode');
    const nationalInsuranceInput = registerView.querySelector('#register-ni-number');
    // vehicle registration details fields
    const vehicleRegNumberInput = registerView.querySelector('#register-vehicle-registration');
    // contact information fields
    const emailInput = registerView.querySelector('#register-email');
    const phoneInput = registerView.querySelector('#register-phone');


    const errorText = registerView.querySelector('#register-error');

    // Map input elements to field names
    const inputElements = {
        username: usernameInput,
        password: passwordInput,
        passwordConfirm: passwordConfirmInput,
        fullName: fullNameInput,
        dateOfBirth: dateOfBirthInput,
        currentAddress: currentAddressInput,
        driverLicenseNumber: driverLicenseNumberInput,
        postcode: postcodeInput,
        nationalInsurance: nationalInsuranceInput,
        vehicleRegNumber: vehicleRegNumberInput,
        email: emailInput,
        phone: phoneInput
    };

    // Fields that should be trimmed
    const fieldsToTrim = [
        'username', 'password', 'fullName', 'currentAddress',
        'driverLicenseNumber', 'postcode', 'nationalInsurance',
        'vehicleRegNumber', 'email', 'phone'
    ];

    // Extract and format all values
    const formData = {};
    Object.entries(inputElements).forEach(([key, element]) => {
        if (element) {
            formData[key] = fieldsToTrim.includes(key) ? element.value.trim() : element.value;
        } else {
            formData[key] = '';
        }
    });

    // Add defaults
    formData.clearance = 'Civilian';

    // Clear previous error message
    if (errorText) {
        errorText.textContent = '';
    }

    // check for empty required fields
    if (!formData.username || !formData.password || !formData.passwordConfirm) {
        if (errorText) {
            errorText.textContent = 'Please fill in all fields.';
        }
        return;
    }

    // check if passwords match
    if (formData.password !== formData.passwordConfirm) {
        if (errorText) {
            errorText.textContent = 'Passwords do not match.';
        }
        return;
    }

    // check password strength (at least 8 characters, with uppercase and lowercaseletters and numbers)
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
    if (!passwordRegex.test(formData.password)) {
        if (errorText) {
            errorText.textContent = 'Password must be at least 8 characters long and include uppercase, lowercase letters, and numbers.';
        }
        return;
    }

    // Submit registration form
    fetch(API_URL + '/user/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            username: formData.username,
            password: formData.password,
            clearance: formData.clearance,
            fullName: formData.fullName,
            dateOfBirth: formData.dateOfBirth,
            currentAddress: formData.currentAddress,
            driverLicenseNumber: formData.driverLicenseNumber,
            postcode: formData.postcode,
            nationalInsurance: formData.nationalInsurance,
            vehicleRegNumber: formData.vehicleRegNumber,
            email: formData.email,
            phone: formData.phone
        })
    })
    .then(function(response) {
        return response.json().then(function(data) {
            if (!response.ok) {
                throw new Error(data.detail || 'Registration failed');
            }
            return data;
        });
    })
    .then(function(data) {
        showToast('Registration successful! You can now log in.');
        navigateTo('login');
    })
    .catch(function(error) {
        if (errorText) {
            errorText.textContent = error.message;
        }
        showToast(error.message, 3000);
    });
}

// Profile handler
function loadUserProfile() {
    // Check if user is authenticated
    if (!state.token) {
        showToast('Please log in to view your profile.', 3000);
        navigateTo('user-login');
        return;
    }

    const profileLoading = document.getElementById('profile-loading');
    const profileContent = document.getElementById('profile-content');
    const profileError = document.getElementById('profile-error');

    // Show loading state
    if (profileLoading) profileLoading.style.display = 'block';
    if (profileContent) profileContent.style.display = 'none';
    if (profileError) profileError.textContent = '';

    // Fetch user profile
    fetch(API_URL + '/user/get', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${state.token}`
        }
    })
    .then(function(response) {
        return response.json().then(function(data) {
            if (!response.ok) {
                throw new Error(data.detail || 'Failed to load profile');
            }
            return data;
        });
    })
    .then(function(data) {
        // Format date if it exists
        let dobDisplay = '-';
        if (data.DateOFBirth) {
            const dobDate = new Date(data.DateOFBirth);
            dobDisplay = dobDate.toLocaleDateString();
        }

        // Populate profile fields
        document.getElementById('profile-username').textContent = data.Username || '-';
        document.getElementById('profile-clearance').textContent = data.Clearance || '-';
        document.getElementById('profile-fullname').textContent = data.FullName || '-';
        document.getElementById('profile-dob').textContent = dobDisplay;
        document.getElementById('profile-address').textContent = data.CurrentAddress || '-';
        document.getElementById('profile-license-number').textContent = data.LicenseNumber || '-';
        document.getElementById('profile-license-postcode').textContent = data.licensePostcode || '-';
        document.getElementById('profile-ni-number').textContent = data.NationalInsuranceNumber || '-';
        document.getElementById('profile-registration-number').textContent = data.RegistrationNumber || '-';
        document.getElementById('profile-email').textContent = data.Email || '-';
        document.getElementById('profile-phone').textContent = data.PhoneNumber || '-';
        const profileEmailInput = document.getElementById('profile-email-input');
        const profilePhoneInput = document.getElementById('profile-phone-input');
        if (profileEmailInput) profileEmailInput.value = data.Email || '';
        if (profilePhoneInput) profilePhoneInput.value = data.PhoneNumber || '';

        // Show content, hide loading
        if (profileLoading) profileLoading.style.display = 'none';
        if (profileContent) profileContent.style.display = 'block';
    })
    .catch(function(error) {
        if (profileLoading) profileLoading.style.display = 'none';
        if (profileError) {
            profileError.textContent = error.message;
        }
        showToast(error.message, 3000);
    });
}

function handleUpdateUserContactInfo() {
    if (!state.token) {
        showToast('Please log in to update your profile.', 3000);
        navigateTo('user-login');
        return;
    }

    const profileError = document.getElementById('profile-error');
    const profileEmailInput = document.getElementById('profile-email-input');
    const profilePhoneInput = document.getElementById('profile-phone-input');
    const email = profileEmailInput ? profileEmailInput.value.trim() : '';
    const phone = profilePhoneInput ? profilePhoneInput.value.trim() : '';

    if (profileError) {
        profileError.textContent = '';
    }

    if (!email && !phone) {
        if (profileError) {
            profileError.textContent = 'Enter an email address or phone number to update.';
        }
        return;
    }

    const body = new URLSearchParams();
    if (email) {
        body.append('email', email);
    }
    if (phone) {
        body.append('phone', phone);
    }

    fetch(API_URL + '/user/update', {
        method: 'PUT',
        headers: {
            'Authorization': 'Bearer ' + state.token,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: body
    })
    .then(function(response) {
        return response.json().then(function(data) {
            if (!response.ok) {
                throw new Error(data.detail || 'Failed to update contact details');
            }
            return data;
        });
    })
    .then(function() {
        showToast('Contact details updated successfully.', 3000);
        loadUserProfile();
    })
    .catch(function(error) {
        if (profileError) {
            profileError.textContent = error.message;
        }
        showToast(error.message, 3000);
    });
}

function formatNoticeValue(key, value) {
    if (value === null || value === undefined || value === '') {
        return '-';
    }

    if (typeof value === 'string' && /date$/i.test(key)) {
        const parsedDate = new Date(value);
        if (!Number.isNaN(parsedDate.getTime())) {
            return parsedDate.toLocaleString();
        }
    }

    if (value instanceof Date && !Number.isNaN(value.getTime())) {
        return value.toLocaleString();
    }

    return String(value);
}

function toggleNoticeDetails(button) {
    // if button is null or doesn't have data-target attribute, do nothing
    if (!button) {
        return;
    }

    // get the id of the details panel from the button's data-target attribute
    const targetId = button.getAttribute('data-target');
    if (!targetId) {
        return;
    }

    // find the details panel element by id
    const detailsPanel = document.getElementById(targetId);
    if (!detailsPanel) {
        return;
    }

    // toggle the visibility of the details panel
    const isExpanded = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', String(!isExpanded));
    detailsPanel.hidden = isExpanded;
    button.querySelector('.notice-toggle-icon').textContent = isExpanded ? '+' : '−';
}

function buildNoticeFieldsHtml(notice) {
    return Object.entries(notice)
        .map(function([key, value]) {
            const displayValue = formatNoticeValue(key, value);
            return `<div class="notice-field">
                <strong>${key}:</strong>
                <span>${displayValue}</span>
            </div>`;
        })
        .join('');
}

function buildNoticeHeaderHtml(displayId, detailsId) {
    return `<button type="button" class="notice-toggle" data-target="${detailsId}" aria-expanded="false">
        <span class="notice-toggle-title">Citation ID: ${displayId}</span>
        <span class="notice-toggle-action">
            <span class="notice-toggle-icon">+</span>
            <span>Show details</span>
        </span>
    </button>`;
}

function buildNoticeArticleHtml(notice, displayId) {
    const noticeId = notice.NoticeID != null ? String(notice.NoticeID) : String(state.notices.indexOf(notice));
    const detailsId = 'notice-details-' + noticeId;
    const headerHtml = buildNoticeHeaderHtml(displayId, detailsId);
    const fieldsHtml = buildNoticeFieldsHtml(notice);
    
    return `<article class="notice-card">
        ${headerHtml}
        <div id="${detailsId}" class="notice-details" hidden>
            ${fieldsHtml}
        </div>
    </article>`;
}

function renderUserNotices() {
    const noticesContainer = document.getElementById('user-dashboard-notices');
    const statusElement = document.getElementById('user-dashboard-status');

    // ensure container exists before trying to render
    if (!noticesContainer) {
        return;
    }

    // clear existing notices
    noticesContainer.innerHTML = '';

    // if no notices, show message
    if (!state.notices.length) {
        if (statusElement) {
            statusElement.textContent = 'No citation notices found.';
        }
        noticesContainer.innerHTML = '<p>No citation notices are available for your account.</p>';
        return;
    }

    // show count of loaded notices
    if (statusElement) {
        statusElement.textContent = state.notices.length + ' citation notice' + (state.notices.length === 1 ? '' : 's') + ' loaded.';
    }

    // render each notice as a collapsible card
    noticesContainer.innerHTML = state.notices.map(function(notice, index) {
        return buildNoticeArticleHtml(notice, index + 1);
    }).join('');
}

function loadUserNotices() {
    // Check if user is authenticated
    if (!state.token) {
        showToast('Please log in to view your citation notices.', 3000);
        navigateTo('user-login');
        return;
    }

    const noticesContainer = document.getElementById('user-dashboard-notices');
    const statusElement = document.getElementById('user-dashboard-status');

    state.isLoading = true;
    state.lastError = null;

    if (statusElement) {
        statusElement.textContent = 'Loading citation notices...';
    }

    if (noticesContainer) {
        noticesContainer.innerHTML = '<p>Loading citation notices...</p>';
    }

    fetch(API_URL + '/notices/me', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + state.token
        }
    })
    .then(function(response) {
        return response.json().then(function(data) {
            if (!response.ok) {
                throw new Error(data.detail || 'Failed to load citation notices');
            }
            return data;
        });
    })
    .then(function(data) {
        state.notices = Array.isArray(data) ? data : [];
        state.isLoading = false;
        renderUserNotices();
    })
    .catch(function(error) {
        state.isLoading = false;
        state.lastError = error.message;
        state.notices = [];

        if (statusElement) {
            statusElement.textContent = error.message;
        }

        if (noticesContainer) {
            noticesContainer.innerHTML = '<p>' + error.message + '</p>';
        }

        showToast(error.message, 3000);
    });
}