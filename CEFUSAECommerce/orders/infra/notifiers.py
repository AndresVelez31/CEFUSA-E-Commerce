class MockNotifier:
    
    def notify(self, user_email: str, message: str) -> dict:
        print(f"[MOCK NOTIFICATION] To: {user_email}")
        print(f"[MOCK MESSAGE] {message}")
        return {
            'success': True,
            'method': 'mock',
            'recipient': user_email,
            'message': 'Notification simulated (development mode)'
        }


class EmailNotifier:
    
    def notify(self, user_email: str, message: str) -> dict:
        print(f"[REAL EMAIL] Sending to: {user_email}")
        print(f"[EMAIL CONTENT] {message}")
        
        return {
            'success': True,
            'method': 'email',
            'recipient': user_email,
            'message': 'Email sent successfully'
        }

