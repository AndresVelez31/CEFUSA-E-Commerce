from django.test import TestCase
from customers.models import Customer
from customers.services import CustomerService


class CustomerModelTest(TestCase):

    def test_crear_cliente(self):
        customer = Customer.objects.create(
            nombre='Juan',
            apellido='Pérez',
            email='juan@example.com',
            telefono='3001234567',
        )
        self.assertEqual(customer.nombre_completo, 'Juan Pérez')
        self.assertEqual(str(customer), 'Juan Pérez <juan@example.com>')

    def test_email_unico(self):
        Customer.objects.create(
            nombre='Ana', apellido='López',
            email='ana@example.com', telefono='3001111111',
        )
        with self.assertRaises(Exception):
            Customer.objects.create(
                nombre='Ana2', apellido='López2',
                email='ana@example.com', telefono='3002222222',
            )


class CustomerServiceTest(TestCase):

    def setUp(self):
        self.service = CustomerService()
        self.customer_data = {
            'nombre': 'Carlos', 'apellido': 'García',
            'email': 'carlos@example.com', 'telefono': '3009999999',
            'direccion': 'Calle 123',
        }

    def test_get_or_create_nuevo(self):
        customer = self.service.get_or_create_customer(
            self.customer_data['email'], self.customer_data
        )
        self.assertEqual(customer.nombre, 'Carlos')

    def test_get_or_create_existente(self):
        self.service.get_or_create_customer(self.customer_data['email'], self.customer_data)
        customer2 = self.service.get_or_create_customer(self.customer_data['email'], self.customer_data)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(customer2.nombre, 'Carlos')

    def test_create_customer_email_duplicado(self):
        self.service.create_customer(self.customer_data)
        result = self.service.create_customer(self.customer_data)
        self.assertFalse(result['success'])
