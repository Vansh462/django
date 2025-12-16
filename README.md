# SignmeUp 

A django based doctor-patient signup and dashboard.

working video - https://www.loom.com/share/4888d0595785424eb8634df5a739bdf8

## Quick Start

### 1. Start the Development Server
```bash
python manage.py runserver
```
Server will be available at: `http://127.0.0.1:8000/`

### 2. Run All Tests
```bash
python manage.py test signX -v 2
```

---

## Manual Testing Scenarios

### Scenario 1: Patient Signup & Login

**Step 1: Signup as Patient**
1. Navigate to `http://127.0.0.1:8000/signup/`
2. Fill the form with:
   - User Type: **Patient**
   - First Name: `John`
   - Last Name: `Doe`
   - Username: `johndoe`
   - Email: `john@example.com`
   - Profile Picture: (optional - upload any image)
   - Address Line 1: `123 Main Street`
   - City: `New York`
   - State: `NY`
   - Pincode: `10001`
   - Password: `SecurePass123`
   - Confirm Password: `SecurePass123`
3. Click "Create Account"
4. **Expected Result**: Redirected to login page with success message

**Step 2: Login as Patient**
1. On login page, fill:
   - User Type: **Patient**
   - Username: `johndoe`
   - Password: `SecurePass123`
2. Click "Login"
3. **Expected Result**: Redirected to patient dashboard showing all entered information

---

### Scenario 2: Doctor Signup & Login

**Step 1: Signup as Doctor**
1. Navigate to `http://127.0.0.1:8000/signup/`
2. Fill the form with:
   - User Type: **Doctor**
   - First Name: `Jane`
   - Last Name: `Smith`
   - Username: `janesmith`
   - Email: `jane@example.com`
   - Profile Picture: (optional)
   - Address Line 1: `456 Medical Avenue`
   - City: `Los Angeles`
   - State: `CA`
   - Pincode: `90001`
   - Password: `DoctorPass123`
   - Confirm Password: `DoctorPass123`
3. Click "Create Account"
4. **Expected Result**: Redirected to login page with success message

**Step 2: Login as Doctor**
1. On login page, fill:
   - User Type: **Doctor**
   - Username: `janesmith`
   - Password: `DoctorPass123`
2. Click "Login"
3. **Expected Result**: Redirected to doctor dashboard showing all entered information

---

### Scenario 3: Validation Tests

**Test 3.1: Password Mismatch**
1. Go to signup page
2. Enter all fields correctly
3. Enter Password: `Pass123`
4. Enter Confirm Password: `Pass456` (different)
5. **Expected Result**: 
   - Red error message appears: "✗ Passwords do not match"
   - Form submission is blocked

**Test 3.2: Duplicate Username**
1. Signup with username `johndoe` (from Scenario 1)
2. Try to signup again with same username
3. **Expected Result**: Error message "Username already exists."

**Test 3.3: Duplicate Email**
1. Signup with email `john@example.com` (from Scenario 1)
2. Try to signup with different username but same email
3. **Expected Result**: Error message "Email already exists."

**Test 3.4: Invalid Login Credentials**
1. Go to login page
2. Enter username: `johndoe`
3. Enter password: `WrongPassword`
4. Select User Type: **Patient**
5. Click "Login"
6. **Expected Result**: Error message "Invalid username or password."

---

### Scenario 4: Cross-Type Access Prevention

**Test 4.1: Patient Cannot Access Doctor Dashboard**
1. Login as patient (from Scenario 1)
2. Manually navigate to `http://127.0.0.1:8000/doctor-dashboard/`
3. **Expected Result**: Redirected to login page

**Test 4.2: Doctor Cannot Access Patient Dashboard**
1. Login as doctor (from Scenario 2)
2. Manually navigate to `http://127.0.0.1:8000/patient-dashboard/`
3. **Expected Result**: Redirected to login page

**Test 4.3: Wrong User Type Login**
1. Go to login page
2. Enter patient credentials (johndoe / SecurePass123)
3. Select User Type: **Doctor** (wrong type)
4. Click "Login"
5. **Expected Result**: Error message "This account is not registered as a Doctor."

---

### Scenario 5: Logout

**Test 5.1: Logout Functionality**
1. Login as any user (patient or doctor)
2. Click "Logout" button in navigation bar
3. **Expected Result**: 
   - Redirected to home page
   - Success message "You have been logged out successfully."
   - Navigation bar shows "Login" and "Sign Up" links

---

### Scenario 6: Navigation & UI

**Test 6.1: Home Page**
1. Navigate to `http://127.0.0.1:8000/`
2. **Expected Result**: 
   - Welcome message displayed
   - Two cards for "For Doctors" and "For Patients"
   - Links to signup and login

**Test 6.2: Navigation Bar**
1. When logged out: Shows "Login" and "Sign Up" links
2. When logged in: Shows "Welcome, [Username]" and "Logout" link
3. Click logo to return to home page

**Test 6.3: Profile Picture Display**
1. Signup with a profile picture
2. Login and view dashboard
3. **Expected Result**: Profile picture is displayed in the dashboard

---

## Automated Test Results

### Running Tests
```bash
python manage.py test signX -v 2
```

### Expected Output
```
Found 25 test(s).
...
Ran 25 tests in ~30s

OK
```

### Test Categories
- ✅ Address Model Tests (2)
- ✅ Patient Model Tests (2)
- ✅ Doctor Model Tests (2)
- ✅ Signup View Tests (6)
- ✅ Login View Tests (5)
- ✅ Dashboard View Tests (6)
- ✅ Logout View Tests (2)

---

## Admin Panel Testing

### Access Admin Panel
1. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
2. Navigate to `http://127.0.0.1:8000/admin/`
3. Login with superuser credentials

### Admin Features
- View all Patients
- View all Doctors
- View all Addresses
- Add/Edit/Delete users and profiles
- Search by name, username, city, state

---

## Troubleshooting

### Issue: "No such table" error
**Solution**: Run migrations
```bash
python manage.py migrate
```

### Issue: Profile picture not showing
**Solution**: Ensure media files are configured in settings.py and server is running

### Issue: Static files not loading (CSS not working)
**Solution**: Collect static files
```bash
python manage.py collectstatic
```

### Issue: Tests fail
**Solution**: Ensure database is clean
```bash
python manage.py flush
python manage.py migrate
```

---

## Performance Notes

- All tests complete in ~30 seconds
- Database: SQLite3 (suitable for development)
- Media files stored in `media/` directory
- Static files served via CDN (Bootstrap)

---

## Security Checklist

✅ Passwords are hashed using Django's default hasher  
✅ CSRF tokens on all forms  
✅ Login required decorators on protected views  
✅ User type verification prevents unauthorized access  
✅ Unique constraints on username and email  
✅ SQL injection prevention via ORM  

---

**Happy Testing! 🎉**

