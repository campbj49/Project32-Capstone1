from app import app
from unittest import TestCase


class InventoryViewsTestCase(TestCase):
    #adapting example code from Flask Testing module to current project
    
    #Enable WTforms to be tested
    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False


    def test_landing_page(self):
        """Ensure root URL redirects successfully"""
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Register User', html, "Not redirecting to register user page.")

            
    def test_registration_page(self):
        """Checks that the registration page loads correctly"""
        with app.test_client() as client:
            resp = client.get('/register')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Register User', html)

            
    def test_logged_out_pages(self):
        """Checks that all the user specific pages throw errors when not logged in"""
        with app.test_client() as client:
            userPaths = (["/user/campbj49",
                          "/users/campbj49/character/add",
                          "/character/1/update",
                          "/character/1/delete",
                          "/character/1/inventory",
                          "/character/1/inventory/add"])
            for path in userPaths:
                resp = client.get(path, follow_redirects=True)
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200, f"{path} has an issue")
                self.assertIn('Restricted page access attempted. Login first', html, f"${path} does not throw an error when no user is logged in")

    def test_item_list(self):
        """Ensures the item list page is loading"""
        with app.test_client() as client:
            resp = client.get('/item')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Item List', html)
            

    def test_add_item(self):
        """Ensures the add/update/delete item pages function"""
        with app.test_client() as client:
            resp = client.post(
                '/item/add', data={
                    "name" :"testName",
                    "desc" : "testDescription",
                    "weight" : 3,
                    "image_url":"testUrl"
                },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testName', html, "Item updating not functioning")
            #get created item's id
            item_id = html[html.find("testUrl")+33:html.find("testUrl")+35]

            #test update path
            resp = client.get(
                f'/item/{item_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('testUpdateName', html, "Item deletion not functioning")

            #test delete path


    def test_login_page(self):
        """Make sure login in functions correctly"""
        with app.test_client() as client:
            resp = client.post(
                '/login', data={
                    'username':'test',
                    'password':'test'
                },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test&#39;s Characters", html,"Login not working")