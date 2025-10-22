from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Patient, Doctor, Address


class AddressModelTest(TestCase):
    """Test cases for Address model"""

    def setUp(self):
        self.address = Address.objects.create(
            line1='123 Main Street',
            city='New York',
            state='NY',
            pincode='10001'
        )

    def test_address_creation(self):
        """Test if address is created correctly"""
        self.assertEqual(self.address.line1, '123 Main Street')
        self.assertEqual(self.address.city, 'New York')
        self.assertEqual(self.address.state, 'NY')
        self.assertEqual(self.address.pincode, '10001')

    def test_address_str(self):
        """Test address string representation"""
        expected_str = '123 Main Street, New York, NY - 10001'
        self.assertEqual(str(self.address), expected_str)


class PatientModelTest(TestCase):
    """Test cases for Patient model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testpatient',
            email='patient@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.address = Address.objects.create(
            line1='123 Main Street',
            city='New York',
            state='NY',
            pincode='10001'
        )
        self.patient = Patient.objects.create(
            user=self.user,
            address=self.address
        )

    def test_patient_creation(self):
        """Test if patient is created correctly"""
        self.assertEqual(self.patient.user.username, 'testpatient')
        self.assertEqual(self.patient.user_type, 'patient')
        self.assertEqual(self.patient.address.city, 'New York')

    def test_patient_str(self):
        """Test patient string representation"""
        expected_str = 'Patient: John Doe'
        self.assertEqual(str(self.patient), expected_str)


class DoctorModelTest(TestCase):
    """Test cases for Doctor model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testdoctor',
            email='doctor@test.com',
            password='testpass123',
            first_name='Jane',
            last_name='Smith'
        )
        self.address = Address.objects.create(
            line1='456 Medical Ave',
            city='Los Angeles',
            state='CA',
            pincode='90001'
        )
        self.doctor = Doctor.objects.create(
            user=self.user,
            address=self.address
        )

    def test_doctor_creation(self):
        """Test if doctor is created correctly"""
        self.assertEqual(self.doctor.user.username, 'testdoctor')
        self.assertEqual(self.doctor.user_type, 'doctor')
        self.assertEqual(self.doctor.address.city, 'Los Angeles')

    def test_doctor_str(self):
        """Test doctor string representation"""
        expected_str = 'Doctor: Jane Smith'
        self.assertEqual(str(self.doctor), expected_str)


class SignupViewTest(TestCase):
    """Test cases for signup view"""

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_signup_page_loads(self):
        """Test if signup page loads correctly"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_patient_signup_success(self):
        """Test successful patient signup"""
        data = {
            'user_type': 'patient',
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@test.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'address_line1': '123 Main Street',
            'city': 'New York',
            'state': 'NY',
            'pincode': '10001'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(User.objects.filter(username='johndoe').exists())
        self.assertTrue(Patient.objects.filter(user__username='johndoe').exists())

    def test_doctor_signup_success(self):
        """Test successful doctor signup"""
        data = {
            'user_type': 'doctor',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'username': 'janesmith',
            'email': 'jane@test.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'address_line1': '456 Medical Ave',
            'city': 'Los Angeles',
            'state': 'CA',
            'pincode': '90001'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(User.objects.filter(username='janesmith').exists())
        self.assertTrue(Doctor.objects.filter(user__username='janesmith').exists())

    def test_password_mismatch(self):
        """Test signup with mismatched passwords"""
        data = {
            'user_type': 'patient',
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@test.com',
            'password': 'testpass123',
            'confirm_password': 'wrongpass',
            'address_line1': '123 Main Street',
            'city': 'New York',
            'state': 'NY',
            'pincode': '10001'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)  # Stay on signup page
        self.assertFalse(User.objects.filter(username='johndoe').exists())

    def test_duplicate_username(self):
        """Test signup with duplicate username"""
        # Create first user
        User.objects.create_user(
            username='johndoe',
            email='john1@test.com',
            password='testpass123'
        )
        # Try to create another with same username
        data = {
            'user_type': 'patient',
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john2@test.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'address_line1': '123 Main Street',
            'city': 'New York',
            'state': 'NY',
            'pincode': '10001'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)  # Stay on signup page
        self.assertEqual(User.objects.filter(username='johndoe').count(), 1)

    def test_duplicate_email(self):
        """Test signup with duplicate email"""
        # Create first user
        User.objects.create_user(
            username='johndoe1',
            email='john@test.com',
            password='testpass123'
        )
        # Try to create another with same email
        data = {
            'user_type': 'patient',
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe2',
            'email': 'john@test.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'address_line1': '123 Main Street',
            'city': 'New York',
            'state': 'NY',
            'pincode': '10001'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)  # Stay on signup page
        self.assertEqual(User.objects.filter(email='john@test.com').count(), 1)


class LoginViewTest(TestCase):
    """Test cases for login view"""

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')

        # Create a patient user
        self.patient_user = User.objects.create_user(
            username='testpatient',
            email='patient@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.address = Address.objects.create(
            line1='123 Main Street',
            city='New York',
            state='NY',
            pincode='10001'
        )
        self.patient = Patient.objects.create(
            user=self.patient_user,
            address=self.address
        )

        # Create a doctor user
        self.doctor_user = User.objects.create_user(
            username='testdoctor',
            email='doctor@test.com',
            password='testpass123',
            first_name='Jane',
            last_name='Smith'
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            address=self.address
        )

    def test_login_page_loads(self):
        """Test if login page loads correctly"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_patient_login_success(self):
        """Test successful patient login"""
        data = {
            'username': 'testpatient',
            'password': 'testpass123',
            'user_type': 'patient'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
        self.assertRedirects(response, reverse('patient_dashboard'))

    def test_doctor_login_success(self):
        """Test successful doctor login"""
        data = {
            'username': 'testdoctor',
            'password': 'testpass123',
            'user_type': 'doctor'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
        self.assertRedirects(response, reverse('doctor_dashboard'))

    def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'username': 'testpatient',
            'password': 'wrongpass',
            'user_type': 'patient'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)  # Stay on login page

    def test_wrong_user_type(self):
        """Test login with wrong user type"""
        data = {
            'username': 'testpatient',
            'password': 'testpass123',
            'user_type': 'doctor'  # Patient trying to login as doctor
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)  # Stay on login page


class DashboardViewTest(TestCase):
    """Test cases for dashboard views"""

    def setUp(self):
        self.client = Client()

        # Create a patient user
        self.patient_user = User.objects.create_user(
            username='testpatient',
            email='patient@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.address = Address.objects.create(
            line1='123 Main Street',
            city='New York',
            state='NY',
            pincode='10001'
        )
        self.patient = Patient.objects.create(
            user=self.patient_user,
            address=self.address
        )

        # Create a doctor user
        self.doctor_user = User.objects.create_user(
            username='testdoctor',
            email='doctor@test.com',
            password='testpass123',
            first_name='Jane',
            last_name='Smith'
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            address=self.address
        )

    def test_patient_dashboard_requires_login(self):
        """Test that patient dashboard requires login"""
        response = self.client.get(reverse('patient_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_patient_dashboard_access(self):
        """Test patient can access their dashboard"""
        self.client.login(username='testpatient', password='testpass123')
        response = self.client.get(reverse('patient_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_dashboard.html')

    def test_doctor_dashboard_requires_login(self):
        """Test that doctor dashboard requires login"""
        response = self.client.get(reverse('doctor_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_doctor_dashboard_access(self):
        """Test doctor can access their dashboard"""
        self.client.login(username='testdoctor', password='testpass123')
        response = self.client.get(reverse('doctor_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor_dashboard.html')

    def test_patient_cannot_access_doctor_dashboard(self):
        """Test that patient cannot access doctor dashboard"""
        self.client.login(username='testpatient', password='testpass123')
        response = self.client.get(reverse('doctor_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect

    def test_doctor_cannot_access_patient_dashboard(self):
        """Test that doctor cannot access patient dashboard"""
        self.client.login(username='testdoctor', password='testpass123')
        response = self.client.get(reverse('patient_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect


class LogoutViewTest(TestCase):
    """Test cases for logout view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.address = Address.objects.create(
            line1='123 Main Street',
            city='New York',
            state='NY',
            pincode='10001'
        )
        Patient.objects.create(user=self.user, address=self.address)

    def test_logout_requires_login(self):
        """Test that logout requires login"""
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_logout_success(self):
        """Test successful logout"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertRedirects(response, reverse('home'))
