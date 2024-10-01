from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from accounts.decorators import admin_required, teacher_required, student_required

User = get_user_model()

class AdminRequiredDecoratorTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='password'
        )
        self.user = User.objects.create_user(
            username='user', email='user@example.com', password='password'
        )
        self.factory = RequestFactory()
    
    def admin_view(self, request):
        return HttpResponse("Admin View Content")

    def test_admin_required_decorator_redirects(self):
        decorated_view = admin_required(self.admin_view)
        
        request = self.factory.get("/restricted-view")
        request.user = self.user
        response = decorated_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")


    def test_admin_required_decorator_redirects_to_correct_path(self):
        decorated_view = admin_required(function=self.admin_view,redirect_to="/login/")
        
        request = self.factory.get("restricted-view")
        request.user = self.user
        response = decorated_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')
    
    def test_admin_required_decorator_does_not_redirect_superuser(self):
        decorated_view = admin_required(self.admin_view)
        
        request = self.factory.get("/restricted-view")
        request.user = self.superuser
        response = decorated_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Admin View Content")
    
    def test_admin_redirect_decorator_return_correct_response(self):
        decorated_view = admin_required(self.admin_view)
        
        request = self.factory.get("/restricted-view")
        request.user = self.superuser
        response = decorated_view(request)
        self.assertIsInstance(response, HttpResponse)


class teacherRequiredDecoratorTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher', email='teacher@example.com', password='password', is_teacher=True
        )
        self.user = User.objects.create_user(
            username='user', email='user@example.com', password='password'
        )
        self.factory = RequestFactory()

    def teacher_view(self, request):
        return HttpResponse("teacher View Content")

    def test_teacher_required_decorator_redirects(self):
        decorated_view = teacher_required(self.teacher_view)

        request = self.factory.get("/restricted-view")
        request.user = self.user

        response = decorated_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_teacher_required_decorator_redirects_to_correct_path(self):
        decorated_view = teacher_required(function=self.teacher_view, redirect_to="/login/")

        request = self.factory.get("/restricted-view")
        request.user = self.user

        response = decorated_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

    def test_teacher_required_decorator_does_not_redirect_teacher(self):
        decorated_view = teacher_required(self.teacher_view)

        request = self.factory.get("/restricted-view")
        request.user = self.teacher

        response = decorated_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"teacher View Content")

    def test_teacher_redirect_decorator_return_correct_response(self):
        decorated_view = teacher_required(self.teacher_view)

        request = self.factory.get("/restricted-view")
        request.user = self.teacher

        response = decorated_view(request)

        self.assertIsInstance(response, HttpResponse)

class StudentRequiredDecoratorTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username='student', email='student@example.com', password='password', is_student=True
        )
        self.user = User.objects.create_user(
            username='user', email='user@example.com', password='password'
        )
        self.factory = RequestFactory()

    def student_view(self, request):
        return HttpResponse("Student View Content")

    def test_student_required_decorator_redirects(self):
        decorated_view = student_required(self.student_view)

        request = self.factory.get("/restricted-view")
        request.user = self.user

        response = decorated_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_student_required_decorator_redirects_to_correct_path(self):
        decorated_view = student_required(function=self.student_view, redirect_to="/login/")

        request = self.factory.get("/restricted-view")
        request.user = self.user

        response = decorated_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

    def test_student_required_decorator_does_not_redirect_student(self):
        decorated_view = student_required(self.student_view)

        request = self.factory.get("/restricted-view")
        request.user = self.student

        response = decorated_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Student View Content")

    def test_student_redirect_decorator_return_correct_response(self):
        decorated_view = student_required(self.student_view)

        request = self.factory.get("/restricted-view")
        request.user = self.student

        response = decorated_view(request)

        self.assertIsInstance(response, HttpResponse)