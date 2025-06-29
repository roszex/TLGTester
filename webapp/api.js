// Railway API configuration
const RAILWAY_API_URL = 'https://emelyanovtgbot-webapp-production.up.railway.app';

// API functions
const api = {
    // Save progress
    saveProgress: async (userId, currentPage, formData = null) => {
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
            return await response.json();
        } catch (error) {
            console.error('Error saving progress:', error);
            return { error: 'Failed to save progress' };
        }
    },

    // Get progress
    getProgress: async (userId) => {
        try {
            const response = await fetch(`${RAILWAY_API_URL}/api/get_progress/${userId}`);
            return await response.json();
        } catch (error) {
            console.error('Error getting progress:', error);
            return { error: 'Failed to get progress' };
        }
    },

    // Update user data
    updateUser: async (userId, data) => {
        try {
            const response = await fetch(`${RAILWAY_API_URL}/api/user/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('Error updating user:', error);
            return { error: 'Failed to update user' };
        }
    }
};

// Get user ID from Telegram WebApp or generate temporary one
function getUserId() {
    if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.initDataUnsafe && window.Telegram.WebApp.initDataUnsafe.user) {
        return window.Telegram.WebApp.initDataUnsafe.user.id.toString();
    }
    // Fallback to localStorage or generate temporary ID
    let userId = localStorage.getItem('temp_user_id');
    if (!userId) {
        userId = 'temp_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('temp_user_id', userId);
    }
    return userId;
}

// Initialize Telegram WebApp
function initTelegramWebApp() {
    if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();
    }
} 