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

/**
 * canAccess(route) – returns true if the current state allows
 * the user to access the given route.
 */
function canAccess(route) {
    // Public routes: accessible without a token
    const publicRoutes = ['info', 'user-login', 'admin-login'];
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
        case 'info':
            setBreadcrumb([{ label: 'Home' }, { label: 'Info' }]);
            break;
        case 'user-login':
            setBreadcrumb([{ label: 'Home' }, { label: 'User Login' }]);
            break;
        case 'admin-login':
            setBreadcrumb([{ label: 'Home' }, { label: 'Admin Login' }]);
            break;

        case 'user-dash':
            setBreadcrumb([{ label: 'User' }, { label: 'Dashboard' }]);
            break;
        case 'user-profile':
            setBreadcrumb([{ label: 'User' }, { label: 'Profile' }]);
            break;

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

    if (route === 'info' || route === 'user-login' || route === 'admin-login' || route === 'logout') {
        setVisibleNav('main-nav');
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
function setVisibleNav(navId) {
    // Show the nav bar matching navId, hide the others
    ['main-nav', 'user-nav', 'admin-nav'].forEach(id => {
        const nav = document.getElementById(id);
        if (nav) {
            nav.style.display = id === navId ? 'flex' : 'none';
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

// Map of route names to view IDs
const ROUTE_TO_VIEW = {
	'info': 'view-info',
	
    //landing page views
    'user-login': 'view-user-login',
    'admin-login': 'view-admin-login',

    //user views
    'user-dash': 'view-user-dashboard',
    'user-profile': 'view-user-profile',
    'user-logout': 'view-user-logout',

    //admin views
    'admin-dash': 'view-admin-dashboard',
    'admin-management': 'view-admin-management',
    'admin-logout': 'view-admin-logout',

	'logout': 'view-logout'
};

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

    // get clearance of account (send credentials via query string for GET)
        const clearanceUrl = API_URL + '/user/clearance?username=' + encodeURIComponent(username)
            + '&password=' + encodeURIComponent(password);

        // Sequence: get clearance -> verify role -> request token
        fetch(clearanceUrl)
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

            // check clearance matches login role
            if (loginRole === 'admin' && state.clearance !== 'Officer') {
                throw new Error('Account does not have admin clearance');
            }
            if (loginRole === 'user' && state.clearance !== 'Civilian') {
                throw new Error('Account does not have user clearance');
            }

            // Attempt login via API
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
        .then(function(response) {
            return response.json().then(function(data) {
                if (!response.ok) {
                    throw new Error(data.detail || 'Login failed');
                }
                return data;
            });
        })
        .then(function(data) {
            state.token = data.access_token;
            state.currentUser = {
                username: username,
                clearance: data.clearance
            };

            // logged in message
            showToast('You have been logged in successfully.');

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
            state.myBooks = [];
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