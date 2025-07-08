# 🧪 Test Guide for KHTRM System

## Quick Test Steps

### 1. Start the Application

```bash
# Terminal 1: Start backend
uv run uvicorn backend.app.main:app --reload

# Terminal 2: Start frontend
npm run dev
```

### 2. Access the Application

- Open: http://localhost:3000
- You should see the login form

### 3. Test Each User Profile

Try logging in with each of the 5 test users:

| Username | Password | Expected Role Display |
|----------|----------|----------------------|
| `nar` | `nar` | Привіт, Нарядчик! |
| `taba` | `taba` | Привіт, Табельник A! |
| `tabb` | `tabb` | Привіт, Табельник B! |
| `dys` | `dys` | Привіт, Диспетчер! |
| `buc` | `buc` | Привіт, Бухгалтер з палива! |

### 4. Expected Behavior

After successful login, you should see:
- ✅ Welcome message with role name in Ukrainian
- ✅ User info showing username and email
- ✅ Simple logout button in the navigation
- ✅ Responsive design that works on mobile and desktop

### 5. Test Logout

- Click the "Вихід" button
- Should redirect to login page
- Should show success notification

### 6. Test Invalid Login

- Try wrong username/password
- Should show error message
- Should not redirect

## Expected File Structure

```
khtrm/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── user.py     ✅ User and Role models
│   │   │   └── base.py     ✅ Base model
│   │   ├── schemas/
│   │   │   └── user.py     ✅ Validation schemas
│   │   ├── config.py       ✅ App configuration
│   │   └── main.py         ✅ FastAPI app
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── App.vue             ✅ Main app component
│   │   │   ├── LoginForm.vue       ✅ Login form with 5 users
│   │   │   ├── Dashboard.vue       ✅ Simple greeting
│   │   │   └── [other].vue         ✅ Stub components
│   │   ├── composables/
│   │   │   ├── useAuth.js          ✅ Auth with 5 users
│   │   │   └── useNotifications.js ✅ Toast notifications
│   │   └── main.js                 ✅ Vue app setup
└── README.md                       ✅ Updated documentation
```

## Troubleshooting

### Backend Issues
- Check if backend is running on port 8000
- Verify database connection
- Check console for errors

### Frontend Issues
- Ensure npm dependencies are installed
- Check if frontend is running on port 3000
- Verify Vue app is loaded correctly

### Login Issues
- Use exact usernames/passwords from the table
- Check browser console for errors
- Verify backend API is responding

## Next Development Steps

1. Connect to real database instead of mock users
2. Add JWT token validation
3. Implement proper session management
4. Add user management interface
5. Build actual business logic for each role 