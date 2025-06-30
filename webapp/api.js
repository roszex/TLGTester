// Railway API configuration
const RAILWAY_API_URL = 'https://emelyanovtgbot-webapp-production.up.railway.app';

// API functions
const api = {
    // Save progress
    saveProgress: async (userId, currentPage, formData = null) => {
        console.log('Saving progress for user:', userId, 'page:', currentPage);
        try {
            const response = await fetch(`${RAILWAY_API_URL}/api/save_progress`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    current_page: currentPage,
                    form_data: formData
                })
            });
            const result = await response.json();
            console.log('Save progress result:', result);
            return result;
        } catch (error) {
            console.error('Error saving progress:', error);
            return { error: 'Failed to save progress' };
        }
    },

    // Get progress
    getProgress: async (userId) => {
        console.log('Getting progress for user:', userId);
        try {
            const response = await fetch(`${RAILWAY_API_URL}/api/get_progress/${userId}`);
            const result = await response.json();
            console.log('Get progress result:', result);
            return result;
        } catch (error) {
            console.error('Error getting progress:', error);
            return { error: 'Failed to get progress' };
        }
    },

    // Update user data
    updateUser: async (userId, data) => {
        console.log('Updating user data for:', userId, 'data:', data);
        try {
            const response = await fetch(`${RAILWAY_API_URL}/api/user/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            console.log('Update user result:', result);
            return result;
        } catch (error) {
            console.error('Error updating user:', error);
            return { error: 'Failed to update user' };
        }
    }
};

// Get user ID from Telegram WebApp or generate temporary one
function getUserId() {
    console.log('Getting user ID...');
    console.log('Telegram object:', window.Telegram);
    console.log('WebApp object:', window.Telegram?.WebApp);
    console.log('initDataUnsafe:', window.Telegram?.WebApp?.initDataUnsafe);
    
    // Try to get from Telegram WebApp
    if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.initDataUnsafe && window.Telegram.WebApp.initDataUnsafe.user) {
        const userId = window.Telegram.WebApp.initDataUnsafe.user.id.toString();
        console.log('Got user ID from Telegram:', userId);
        return userId;
    }
    
    // Try to get from URL parameters (fallback)
    const urlParams = new URLSearchParams(window.location.search);
    const userIdFromUrl = urlParams.get('user_id');
    if (userIdFromUrl) {
        console.log('Got user ID from URL:', userIdFromUrl);
        return userIdFromUrl;
    }
    
    // Fallback to localStorage or generate temporary ID
    let userId = localStorage.getItem('temp_user_id');
    if (!userId) {
        userId = 'temp_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('temp_user_id', userId);
        console.log('Generated temporary user ID:', userId);
    } else {
        console.log('Got user ID from localStorage:', userId);
    }
    return userId;
}

// Initialize Telegram WebApp
function initTelegramWebApp() {
    console.log('Initializing Telegram WebApp...');
    if (window.Telegram && window.Telegram.WebApp) {
        try {
            window.Telegram.WebApp.ready();
            window.Telegram.WebApp.expand();
            console.log('Telegram WebApp initialized successfully');
        } catch (error) {
            console.error('Error initializing Telegram WebApp:', error);
        }
    } else {
        console.log('Telegram WebApp not available');
    }
} 