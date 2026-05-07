const API_URL = 'http://127.0.0.1:8000';

// ── Application state
const state = {
    // Data
    books: [], // cached book list
    myBooks: [], // cached current user's books
    currentBookId: null, // id of book currently in detail view

    // Auth (used in Assessment 3)
    token: null, // JWT string once logged in
    currentUser: null, // user object { id, username, role }

    // UI
    isLoading: false, // true while any fetch is in progress
    lastError: null // last error message string
};

window.state = state;

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

    return true;
}

function updateNav() {
    const logoutBtn = document.getElementById('logout-btn');
    const loginLink = document.querySelector('[data-view="login"]');
    if (!logoutBtn) {
        return;
    }

    if (state.currentUser) {
        logoutBtn.style.display = 'inline-block';
        if (loginLink) {
            loginLink.style.display = 'none';
        }
    } else {
        logoutBtn.style.display = 'none';
        if (loginLink) {
            loginLink.style.display = 'inline-block';
        }
    }
}

function handleLogout() {
    confirmAction(
        'Are you sure you want to log out?',
        function() {
            state.token = null;
            state.currentUser = null;
            state.myBooks = [];
            showToast('You have been logged out.');
            navigateTo('info');
        }
    );
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
    switch (route) {
		// landing page view
        case 'info':
            setBreadcrumb([{ label: 'Home' }, { label: 'Info' }]);
            showView('view-list');
            loadBookList(); // defined in Task 10
            break;
        case 'user-login':
            setBreadcrumb([{ label: 'Home' }, { label: 'User Login' }]);
            showView('view-my-books');
            loadMyBooks();
            break;
        case 'admin-login':
            setBreadcrumb([{ label: 'Home' }, { label: 'Admin Login' }]);
            showView('view-dashboard');
            loadDashboard();
            break;

		// user views
        case 'user-dash':
            setBreadcrumb([{ label: 'User' },{ label: 'Dashboard' }
            ]);
            showView('view-user-dash');
            break;
        case 'user-profile':
            setBreadcrumb([{ label: 'User' },{ label: 'Profile' }
            ]);
            showView('view-user-profile');
            //loadBookDetail(params.id); // defined in Task 12
            break;

		// admin views
        case 'admin-dash':
            setBreadcrumb([{ label: 'Admin' }, { label: 'Dashboard' }]);
            showView('view-admin-dash');
            break;
        case 'admin-management':
            setBreadcrumb([{ label: 'Admin' }, { label: 'Management' }]);
            showView('view-admin-management');
            break;


        default:
            console.warn('navigateTo: unknown route "' + route + '"');
            navigateTo('info'); // fallback
    }

    updateNav();
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

// Boot the SPA
const ROUTE_TO_VIEW = {
	'info': 'view-info',
	
    //landing page views
    'user-login': 'view-user-login',
    'admin-login': 'view-admin-login',

    //user views
    'user-dash': 'view-user-dashboard',
    'user-profile': 'view-user-profile',
	
	//admin views
	'admin-dash': 'view-admin-dashboard',
	'admin-management': 'view-admin-management',

	'logout': 'view-logout'
};

function setVisibleNav(navId) {
    ['main-nav', 'user-nav', 'admin-nav'].forEach(id => {
        const nav = document.getElementById(id);
        if (nav) {
            nav.style.display = id === navId ? 'flex' : 'none';
        }
    });
}

function updateActiveNav(route) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.dataset.view === route);
    });
}

function navigateTo(route) {
    const viewId = ROUTE_TO_VIEW[route] || 'view-info';
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

function routeFromHash() {
    const route = window.location.hash.slice(1) || 'info';
    navigateTo(route);
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            window.location.hash = this.dataset.view || 'info';
        });
    });

    const userLoginBtn = document.getElementById('user-login-btn');
    if (userLoginBtn) {
        userLoginBtn.addEventListener('click', function() {
			handleLogin('user');
            //navigateTo('user-login');
        });
    }

    const adminLoginBtn = document.getElementById('admin-login-btn');
    if (adminLoginBtn) {
        adminLoginBtn.addEventListener('click', function() {
			handleLogin('admin');
            //navigateTo('admin-login');
        });
    }

    window.addEventListener('hashchange', routeFromHash);
    setVisibleNav('main-nav');
    routeFromHash();
});

function handleLogin(role) {
	if (role === 'user') {
		setVisibleNav('user-nav');
		navigateTo('user-dash');
		return;
	}

	if (role === 'admin') {
		setVisibleNav('admin-nav');
		navigateTo('admin-dash');
	}
}